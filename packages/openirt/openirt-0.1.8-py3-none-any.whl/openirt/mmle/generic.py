import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.integrate as integrate
from scipy.optimize import minimize

class Generic():
    def __init__(self, model) -> None:
        self.p = model.p
        self.num_params = model.num_params
        self.ability_prior = lambda ability: norm.pdf(ability)

    # eq 6.2
    def resp_prob(self, item_responses, ability, params):
        ''' Probability of the subject's item response vector conditional 
            on the examinee's ability and item parameters'''
        P = self.p(ability, params)
        Q = 1 - P
        return np.prod(P ** item_responses * Q ** (1 - item_responses), axis=1)

    # integrand of denominator of eq 6.1
    def marg_resp_prob_integrand(self, item_responses, ability, params):
        return self.ability_prior(ability) * self.resp_prob(item_responses, ability, params)

    # denominator of eq 6.1
    # consider other methods of integration, and how the user can specify the integration parameters
    def marg_resp_prob(self, item_responses, params):
        ''' Marginal probability of the item response vector with respect 
            to the item parameters and the population ability density, i.e. 
            integrate marg_resp_prob_integrand w.r.t. ability'''
        integrand = lambda x: self.marg_resp_prob_integrand(item_responses, x, params)
        result, _ = integrate.quad(integrand, -6, 6, epsabs=1e-1, epsrel=1e-1)
        return result

    # Eq 6.4. log likelihood func to be maximized
    def marg_log_liklihood(self, data, params):
        ret = 0
        for item_response in data:
            ret += np.log(self.marg_resp_prob(item_response, params))
        return ret

    # get param value that maximizes marg_log_liklihood
    # consider other methods of optimization, and how the user can specify the optimization parameters
    # show error if optimization failed
    def maximize_log_likelihood_for_param(self, data, params, item_idx, param_idx, bounds):
        initial_guess = params[param_idx][item_idx]
        params = params.copy()
        def objective_func(x):
            params[param_idx][item_idx] = x
            return -self.marg_log_liklihood(data, params)
        result = minimize(objective_func, initial_guess, bounds=[bounds], tol=1e-1, method='Nelder-Mead')
        return result.x[0], -result.fun

    def em1(self, data, prov_params, bounds, eps=1e-6):
        data = np.array(data)
        subjects, items = data.shape
        params = np.tile(np.array(prov_params, dtype=float), items).reshape(items, self.num_params).T
        
        prev_log_L = -np.inf
        log_L = self.marg_log_liklihood(data, params)
        while log_L - prev_log_L > eps:
            print(f'prev log L: {prev_log_L}')
            print(f'log L: {log_L}')
            prev_log_L = log_L
            new_params = np.zeros((self.num_params, items), dtype=float)
            for item_idx in range(items):
                print(f'Item:{item_idx}')
                for param_idx in range(self.num_params):
                    new_param, _ = self.maximize_log_likelihood_for_param(data, params, item_idx, param_idx, bounds[param_idx])
                    new_params[param_idx][item_idx] = new_param
            
            params = new_params
            log_L = self.marg_log_liklihood(data, params)
        return params

    # preferred # add params to constructor?
    def em2(self, data, prov_params, bounds, eps=1):
        data = np.array(data)
        subjects, items = data.shape
        params = np.tile(np.array(prov_params, dtype=float), items).reshape(items, self.num_params).T
        
        prev_log_L = -np.inf
        log_L = self.marg_log_liklihood(data, params)
        while log_L - prev_log_L > eps:
            print(f'prev log L: {prev_log_L}')
            print(f'log L: {log_L}')
            prev_log_L = log_L
            for item_idx in range(items):
                print(f'Item:{item_idx}')
                for param_idx in range(self.num_params):
                    new_param, _ = self.maximize_log_likelihood_for_param(data, params, item_idx, param_idx, bounds[param_idx])
                    params[param_idx][item_idx] = new_param
            log_L = self.marg_log_liklihood(data, params) # unnecessary, returned by maximize_log_likelihood_for_param
        return params

    def em(self, data, prov_params, bounds, eps=1e-6):
        data = np.array(data)
        _, items = data.shape
        params = np.tile(np.array(prov_params, dtype=float), items).reshape(items, self.num_params).T
        
        prev_log_L = -np.inf
        log_L = self.marg_log_liklihood(data, params)
        while log_L - prev_log_L > eps:
            print(f'prev log L: {prev_log_L}')
            print(f'log L: {log_L}')
            prev_log_L = log_L
            new_params = np.zeros((self.num_params, items), dtype=float)
            for item_idx in range(items):
                print(f'Item:{item_idx}')
                new_params = np.zeros(self.num_params, dtype=float)
                for param_idx in range(self.num_params):
                    new_param, _ = self.maximize_log_likelihood_for_param(data, params, item_idx, param_idx, bounds[param_idx])
                    new_params[param_idx] = new_param
                
                for param_idx in range(self.num_params):
                    params[param_idx][item_idx] = new_params[param_idx]
                    
            log_L = self.marg_log_liklihood(data, params)
        