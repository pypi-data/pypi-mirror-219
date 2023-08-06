import numpy as np
from typing import Union
from scipy import integrate
import matplotlib.pyplot as plt

# use alpha, b, c
def prob(ability: Union[list, np.ndarray, float], 
         params: Union[list, np.ndarray])  -> np.ndarray:
        items = np.array(params).shape[1]
        num_abilities = 1
        if np.array(ability).shape != ():
            num_abilities = np.array(ability).shape[0]
        ability = np.tile(np.array([ability]).T, (1, items))

        params = np.tile(params, num_abilities).reshape(
            (3, num_abilities, items))
        return params[2] + (1 - params[2]) *  (np.exp(np.exp(params[0]) * (ability - params[1])) / (1 + np.exp(np.exp(params[0]) * (ability - params[1]))))

def prob2PM(ability: Union[list, np.ndarray, float],
            params: Union[list, np.ndarray]) -> np.ndarray:
    items = np.array(params).shape[1]
    num_abilities = 1
    if np.array(ability).shape != ():
        num_abilities = np.array(ability).shape[0]
    ability = np.tile(np.array([ability]).T, (1, items))

    params = np.tile(params, num_abilities).reshape(
        (3, num_abilities, items))
    return np.exp(np.exp(params[0]) * (ability - params[1])) / (1 + np.exp(np.exp(params[0]) * (ability - params[1])))

def plot_item_curve(p):
    ability = np.linspace(-10, 10, 100)
    for i in range(p.shape[1]):
        plt.plot(ability, prob(ability, p[:,i].reshape(p.shape[0], 1)), label=f'Question{i+1}')        
    plt.legend()
    plt.show()





# function params
num_nodes = 4
quads_range = 8
data = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],] # rows are subjects, columns are items

NALT = 5 # number of alternatives, pg 188. or use p instead of 1/nalt
priori_weight_c = 20

integr_range = 10 # use

# priors
alpha_mean = 0
alpha_var = np.sqrt(0.5) # page 187
b_mean = 0
b_var = 1
ALP = priori_weight_c * (1 / NALT) + 1
BET =  priori_weight_c * (1 - 1 / NALT) + 1
orig_params = np.array([0, 0, 1/NALT])

data = np.array(data)
subjects, items = data.shape
params = np.tile(orig_params, items).reshape((items, 3)).T

i = 0
# # for iteration in range(1):
# #     for i in range(items):


# intergal over likelihood of ability for each subject
# denominator in eq 7.14
integ_likelihood = []
for j in range(subjects):
    likelihood = lambda ability: np.prod(prob(ability, params)[0] ** data[j]) * np.prod((1 - prob(ability, params)[0]) ** (1 - data[j]))
    ability = -10
    print(prob(ability, params)[0] ** data[j])
    print((1 - prob(ability, params)[0]) ** (1 - data[j]))
    print(prob(ability, params)[0] ** data[j] * (1 - prob(ability, params)[0]) ** (1 - data[j]))
    print()
    x = np.linspace(-100, 100, 100)
    y = [likelihood(x_i) for x_i in x]
    plt.plot(x, y)
    plt.show()
    # integ_likelihood.append(integrate.quad(likelihood, -10, 10)[0])
integ_likelihood = np.array(integ_likelihood)
quit()

# def likelihood(j, ability):
#     P = prob(ability, params)[0]
#     return np.prod(P ** data[j] * (1 - P) ** (1 - data[j]))

# px_given_u = lambda ability: np.array([likelihood(j, ability) for j in range(subjects)]) / integ_likelihood
# f = lambda ability: np.sum(px_given_u(ability))
# r = lambda i, ability: np.sum(px_given_u(ability) * data[:,i])

# W = lambda i, ability: (prob2PM(ability, params[:,i].reshape(3,1))[0][0] * (1 - prob2PM(ability, params[:,i].reshape(3,1))[0][0])) / \
# (prob(ability, params[:,i].reshape(3,1))[0][0] * (1 - prob(ability, params[:,i].reshape(3,1))[0][0]))


# L1_integrand = lambda ability: (r(i, ability) - f(ability) * prob(ability, params[:,i].reshape(3,1))[0][0]) * W(i, ability) * (ability - params[1][i])
# L1 = np.exp(params[0][i]) * (1 - params[2][i]) * integrate.quad(L1_integrand, -10, 10)[0] - (params[0][i] - alpha_mean) / alpha_var

# L2_integrand = lambda ability: (r(i, ability) - f(ability) * prob(ability, params[:,i].reshape(3,1))[0][0]) * W(i, ability)
# L2 = -np.exp(params[0][i]) * (1 - params[2][i]) * integrate.quad(L2_integrand, -10, 10)[0]  - (params[1][i] - b_mean) / b_var

# L3_integrand = lambda ability: (r(i, ability) - f(ability) * prob(ability, params[:,i].reshape(3,1))[0][0]) / prob(ability, params[:,i].reshape(3,1))[0][0]
# L3 = 1 / (1 - params[2][i]) * integrate.quad(L3_integrand, -10, 10)[0] + (ALP - 2) / params[2][i] - (BET - 2) / (1 - params[2][i])

# # optimize all of this. P is often reused, for example
# # might also be more readible if we add more lambda functions
# lamb11_integrand = lambda ability: f(i, ability) * (ability - params[1][i]) ** 2 * ((prob(ability, params[:,i].reshape(3,1))[0][0] - params[2][i]) / (1 - params[2][i])) ** 2 * ((1 - prob(ability, params[:,i].reshape(3,1))[0][0]) / (prob(ability, params[:,i].reshape(3,1))[0][0]))
# lamb11 = -np.exp(params[0][i]) ** 2 * integrate.quad(lamb11_integrand, -10, 10)[0] - 1 / alpha_var

# lamb22_integrand = lambda ability: f(i, ability) * ((prob(ability, params[:,i].reshape(3,1))[0][0] - params[2][i]) / (1 - params[2][i])) ** 2 * ((1 - prob(ability, params[:,i].reshape(3,1))[0][0]) / (prob(ability, params[:,i].reshape(3,1))[0][0]))
# lamb22 = -np.exp(params[0][i]) ** 2 * integrate.quad(lamb22_integrand, -10, 10)[0] - 1 / b_var

# lamb33_integrand = lambda ability: f(i, ability) * (1 / prob(ability, params[:,i].reshape(3,1))[0][0] - 1) ** 2 * ((1 - prob(ability, params[:,i].reshape(3,1))[0][0]) / (prob(ability, params[:,i].reshape(3,1))[0][0])) 
# lamb33 = -1 * integrate.quad(lamb33_integrand, -10, 10)[0] - (ALP - 2) / params[2][i] ** 2 - (BET - 2) / (1 - params[2][i]) ** 2

# lamb12_integrand = lambda ability: f(i, ability) * (ability - params[1][i]) * ((prob(ability, params[:,i].reshape(3,1))[0][0] - params[2][i]) / (1 - params[2][i])) ** 2 * ((1 - prob(ability, params[:,i].reshape(3,1))[0][0]) / (prob(ability, params[:,i].reshape(3,1))[0][0]))
# lamb12 = np.exp(params[0][i]) ** 2 * integrate.quad(lamb12_integrand, -10, 10)[0]

# lamb13_integrand = lambda ability: f(i, ability) * (ability - params[1][i]) * ((prob(ability, params[:,i].reshape(3,1))[0][0] - params[2][i]) / (1 - params[2][i])**2) * ((1 - prob(ability, params[:,i].reshape(3,1))[0][0]) / (prob(ability, params[:,i].reshape(3,1))[0][0]))
# lamb13 = -np.exp(params[0][i]) ** 2 * integrate.quad(lamb13_integrand, -10, 10)[0]

# lamb23_integrand = lambda ability: f(i, ability) * ((prob(ability, params[:,i].reshape(3,1))[0][0] - params[2][i]) / (1 - params[2][i])**2) * ((1 - prob(ability, params[:,i].reshape(3,1))[0][0]) / (prob(ability, params[:,i].reshape(3,1))[0][0]))
# lamb23 = np.exp(params[0][i]) * integrate.quad(lamb13_integrand, -10, 10)[0]

# cross_deriv_mat = np.array([[lamb11, lamb12, lamb13], [lamb12, lamb22, lamb23], [lamb13, lamb23, lamb33]])
# deriv_mat = np.array([[L1], [L2], [L3]])

# mat_inv = np.linalg.inv(cross_deriv_mat)
# # est = est - np.matmul(mat_inv, deriv_mat)
        