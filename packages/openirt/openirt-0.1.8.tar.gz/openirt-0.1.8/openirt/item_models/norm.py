from model import Model
import numpy as np
from scipy.stats import norm
from typing import Union

class Norm(Model):
    def __init__(self):
        super().__init__(Norm.norm_p, 2, True)
    
    @staticmethod
    def norm_p(self, ability: Union[list, np.ndarray, float], params: Union[list, np.ndarray]) -> np.ndarray:
        """_summary_
        takes array of a abilities (n*1) and array of params (2*m) and returns prob (n*m)

        Args:
            ability (Union[list, np.ndarray, float]): _description_
            params (Union[list, np.ndarray]): _description_

        Returns:
            np.ndarray: _description_
        """
        ability = np.array(ability)
        params = np.array(params)
        z = np.matmul(ability[:, np.newaxis], [params[1]])
        z += np.tile(params[0], (len(ability), 1))
        return norm.cdf(z)
    
    @staticmethod
    def __norm_density(self, ability: Union[list, np.ndarray, float], params: Union[list, np.ndarray]) -> np.ndarray:
        ability = np.array(ability)
        params = np.array(params)
        z = np.matmul(ability[:, np.newaxis], [params[1]])
        z += np.tile(params[0], (len(ability), 1))
        return norm.pdf(z)
    
    @staticmethod
    def convert_param_form(self, params):
        return np.array([-params[0] / params[1], 1 / params[1]])
    
    def estimate_ability_max_lik(self, params: Union[list, np.ndarray], 
                         results: Union[list, np.ndarray],
                         end=0.00000001,
                         eps=0.01) -> np.ndarray:
        est = 0.5
        prev_est = 0
        while abs(est - prev_est) > end:
            P = self.prob(est, params)[0]
            W = (1 - P) * P
            h = self.norm_density(est, params)[0]
            prev_est = est
            denom = np.sum(params[1]**2 * W)
            if denom < eps or np.any(W < eps):
                break
            est = est + (np.sum(params[1] * W  * ((results - P)/ h)) / denom)
        return est
    
    def estimate_item_params_max_lik(self, 
                            ability: Union[list, np.ndarray], 
                            result: Union[list, np.ndarray], 
                            sigm_orig=0,
                            lamb_orig=1, 
                            end=0.0000001,  
                            eps=0.1) -> np.ndarray:
        ability = np.array(ability)
        result = np.array(result)
        est = [sigm_orig, lamb_orig]
        prev_est = [0, 0]
        while abs(est[0] - prev_est[0]) > end or abs(est[1] - prev_est[1]) > end:
            P = self.prob(
                ability, [[est[0]], [est[1]]]).transpose()[0]
            h = self.norm_density(ability, [[est[0]], [est[1]]]).transpose()[0]
            W = h**2 / (P * (1 - P))
            L11 = -np.sum(W)
            L12 = -np.sum(ability * W)
            L22 = -np.sum(ability**2 * W)
            L = np.array([[L11, L12], [L12, L22]])

            if abs(np.linalg.det(L)) < eps:
                break
            L_inv = np.linalg.inv(L)

            v = (result - P) / h
            obs_mat = np.array([np.sum(W * v), np.sum(W * v * ability)])
            prev_est = est
            est = est - np.matmul(L_inv, obs_mat)
        return est