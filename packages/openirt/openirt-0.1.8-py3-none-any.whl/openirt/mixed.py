import numpy as np
from item_models import PL1, PL2, PL3
from scipy.stats import norm
import scipy.integrate as integrate
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# mention: we assume there is some sort of location param.
# For graded models we must also assume icc is increasing, so we place bounds
class Mixed():
    def __init__(self, 
                 responses, 
                 categories,
                 models, 
                 prov_params=None,
                 param_bounds=None,
                 loc_param_idx=None,
                 loc_param_asc=None) -> None:
        # loc_param asc is a list of booleans, corresponding to each item. The boolean is 'True' if a higher location
        # corresponds to a more difficult item.
        self.responses = responses
        self.num_subjects, self.num_items = responses.shape
        self.categories = categories
        self.models = models
        self.grouped_resp, self.group_idxs, self.group_count= self._group_subjects(responses)
        self.set_loc_params(loc_param_idx)
        self.ability_distr = lambda ability: norm.pdf(ability)
        self.set_param_bounds(param_bounds)
        self.set_loc_param_asc(loc_param_asc)
        self.set_prov_params(prov_params)

        # print(self.condit_prob_of_indiv_resp(params=self.prov_params, item=0, resp=1, ability=0.4))
        
        
    def set_loc_params(self, loc_param):
        # if None, we assume all models either:
        # - are predefined (pl1-pl3, norm)
        # - only have one parameter
        # With this assumption we can construct this object
        # This can be given in the solve step instead of constructor..?
        if loc_param is None:
            self.loc_params = []
            for m in self.models:
                if m.loc_param is not None:
                    self.loc_params.append(m.loc_param)
                else:
                    self.loc_params.append(0)
        else:
            self.loc_params = loc_param
            
    def set_prov_params(self, prov_params):
        self.prov_params = []
        if prov_params is None:
            for i, m in enumerate(self.models):
                if m.prov_params:
                    self.prov_params.append(np.tile(m.prov_params, (self.categories[i]-1, 1)).T.astype(float))
                    
                    # distribute location parameters (assuming bounds exist)
                    lower_bound = self.param_bounds[i][self.loc_params[i]][0]
                    upper_bound = self.param_bounds[i][self.loc_params[i]][1]
                    if self.loc_param_asc[i]:
                        self.prov_params[i][self.loc_params[i]] = np.linspace(lower_bound, upper_bound, self.categories[i]+1)[1:-1]
                    else:
                        self.prov_params[i][self.loc_params[i]] = np.linspace(upper_bound, lower_bound, self.categories[i]+1)[1:-1]
                else:
                    raise ValueError('"prov_params" is None')
        else:
            for i, p in enumerate(prov_params):
                self.prov_params.append(np.tile(p, (self.categories[i]-1, 1)).T.astype(float))
                
    def set_param_bounds(self, param_bounds):
        # if none, we assume that all items have attribute, or we dont use bounds
        if param_bounds is None:
            self.param_bounds = []
            for m in self.models:
                if m.param_bounds is not None:
                    self.param_bounds.append(m.param_bounds)
                else:
                    self.param_bounds.append([None] * m.num_params)
        else:
            self.param_bounds = param_bounds

    def set_loc_param_asc(self, loc_param_asc):
        if loc_param_asc is None:
            self.loc_param_asc = []
            for m in self.models:
                if m.loc_param_asc is not None:
                    self.loc_param_asc.append(m.loc_param_asc)
                else: 
                    self.loc_param_asc.append(True)
        else:
            self.loc_param_asc = loc_param_asc
            

    def _group_subjects(self, responses):
        return np.unique(responses, axis=0, return_inverse=True, return_counts=True)

    # P*_{i,k}(\theta)
    # 1 when k = -1
    # 0 when k = m-1 ?
    def boundary_prob(self, params, item, resp, ability):
        # resp is single resp
        if resp == -1:
            return 1
        if resp == self.categories[item] - 1:
            return 0
        temp_params = params[item][:,resp].reshape(self.models[item].num_params, 1)
        return self.models[item].p([ability], temp_params)[0][0]
    
    # P(U_{li}|\theta) = P(U_{li} = k|\theta) = P_{ik}(\theta) = P*_{i,k-1}(\theta) - P*_{ik}(\theta)
    def condit_prob_of_indiv_resp(self, params, resp, item, ability):
        # resp is single resp
        return max(self.boundary_prob(params, item, resp - 1, ability) - self.boundary_prob(params, item, resp, ability), 1e-3)
    
    # P(U_l|\theta) = \prod_{i=1}^n P(U_{li}|\theta)
    def condit_prob_of_resp_vect(self, params, resp, ability):
        return np.prod([self.condit_prob_of_indiv_resp(params, u, i, ability) for i, u in enumerate(resp)])
    
    # P(U_l) = \int P(U_l|\theta) \pi(\theta) d\theta
    def marginal_prob_of_resp(self, params, resp):
        integrand = lambda ability: self.condit_prob_of_resp_vect(params, resp, ability) * self.ability_distr(ability)
        result, _ = integrate.quad(integrand, -7, 7, epsabs=1e-3, epsrel=1e-3)
        return result
    
    # L = \sum_{l=1}^{L} r_l \log{P(U_l)}
    def log_likelihood(self, params):
        marg_p = np.array([self.marginal_prob_of_resp(params, resp) for resp in self.grouped_resp])
        if np.any(marg_p <= 0):
            return -np.inf
        return np.sum(self.group_count * np.log(marg_p))
    
    def loc_param_bounds(self, params, item, param_type_idx, boundary_idx):
        tot_lower_bound = self.param_bounds[item][param_type_idx][0]
        tot_upper_bound = self.param_bounds[item][param_type_idx][1]
        if self.loc_param_asc[item]:
            # lower bound
            if boundary_idx == 0:
                lower = tot_lower_bound
            else:
                lower = params[item][param_type_idx][boundary_idx-1]
            # upper bound
            if boundary_idx == self.categories[item] - 2:
                upper = tot_upper_bound
            else:
                upper = params[item][param_type_idx][boundary_idx+1]
        else:
            # lower bound
            if boundary_idx == self.categories[item] - 2:
                lower = tot_lower_bound
            else:
                lower = params[item][param_type_idx][boundary_idx+1]
            # upper bound
            if boundary_idx == 0:
                upper = tot_upper_bound
            else:
                upper = params[item][param_type_idx][boundary_idx-1]
        return lower, upper
        
    def maximize_log_lik_loc(self, params, item, param_type_idx, boundary_idx):
        initial_guess = params[item][param_type_idx][boundary_idx]
        def obj_func(x):
            params[item][param_type_idx][boundary_idx] = x
            return -self.log_likelihood(params)
        result = minimize(obj_func,
                          initial_guess,
                          bounds=[self.loc_param_bounds(params, item, param_type_idx, boundary_idx)],
                          tol=1e-3)
        return result.x[0], -result.fun
            
    def maximize_log_lik(self, params, item, param_type_idx):
        initial_guess = params[item][param_type_idx][0]
        def obj_func(x):
            params[item][param_type_idx] = x
            return -self.log_likelihood(params)
        result = minimize(obj_func,
                          initial_guess,
                          bounds=[self.param_bounds[item][param_type_idx]],
                          tol=1e-3)
        return result.x[0], -result.fun

    def em_mmle(self, eps=0.01):
        params = self.prov_params.copy() 
        prev_log_L = -np.inf
        log_L = self.log_likelihood(params)
        while log_L - prev_log_L > eps:
            print(f'prev log L: {prev_log_L}')
            print(f'log L: {log_L}')
            prev_log_L = log_L
            for i in range(len(params)):
                # item_params are all parameters for item i
                for param_type_idx in range(self.models[i].num_params):
                    # param_type are the same type of parameters for i, e.g. all the betas
                    if param_type_idx == self.loc_params[i]:
                        # optimize all location params separately
                        for k in range(self.categories[i] - 1):
                            print(f'maximizing item {i}, {param_type_idx}th parameter, where k={k}')
                            new_param, log_L = self.maximize_log_lik_loc(params, i, param_type_idx, k)
                    else:
                        print(f'maximizing item {i}, {param_type_idx}th parameter, (all k)')
                        new_param, log_L = self.maximize_log_lik(params, i, param_type_idx)
        return params
    
    # \bar(\theta_l) = \frac{\int \theta P(U_l|\theta) \pi(\theta) d\theta}{P(U_l)}
    def estimate_ability_post_mean(self, params, group):
        integrand = lambda ability: self.condit_prob_of_resp_vect(params, self.grouped_resp[group], ability) * self.ability_distr(ability) * ability
        numer, _ = integrate.quad(integrand, -7, 7, epsabs=1e-3, epsrel=1e-3)
        denom = self.marginal_prob_of_resp(params, self.grouped_resp[group])
        return numer / denom
        
    def plot_boundaries(self, params, i):
        ability = np.linspace(-5, 5)
        for k, param in enumerate(params[i].T):
            prob = self.models[i].p(ability, param.reshape(models[i].num_params,1))
            plt.plot(ability, prob, label=f'P*_{k}')
        plt.legend()
        plt.show()
    
    def plot_irccc(self, params, i):
        ability = np.linspace(-5, 5)
        for k in range(categories[i]):
            prob = [self.condit_prob_of_indiv_resp(params, k, i, ab) for ab in ability]
            plt.plot(ability, prob, label=f'P_{k}')
        plt.legend()
        plt.show()

# important to clean data, eliminate options that arent chosen
responses = np.array([[0, 0],
                      [1, 3],
                      [2, 1],
                      [1, 2]])

categories = (3, 4)
models = (PL2(), PL1())

mixed = Mixed(responses, categories, models)


par = [np.array([[ 1.2990496 , -1.55895654],
       [ 1.32044104,  1.32044104]]), np.array([[ 1.17551977, -0.17228615, -1.37332456]])]
print(mixed.estimate_ability_post_mean(par, 2))

def p_category(i, ablility):
    # returns array with probability of each category
    pass


