from model import Model
from typing import Union
import numpy as np


class PL2(Model):
    """
    2-parameter logistic model.
    p(\\theta) = 1 / (1 + e^{-(\\zeta + \\lambda\\theta)}
    """
    def __init__(self):
        super().__init__(
            PL2.pl2_p,
            num_params=2,
            multi=True,
            prov_params=[0, 1],
            loc_param=0,
            param_bounds=((-10, 10), (0, 5)),
            loc_param_asc=False,
        )

    @staticmethod
    def pl2_p(
        ability: Union[list, np.ndarray, float], params: Union[list, np.ndarray]
    ) -> np.ndarray:
        """
        Probability of a correct response given the ability and item
        parameters.

        Args:
            ability (np.ndarray): Array of abilities.
            params (np.ndarray): Item parameters. Item parameters. Each column
            is a different item, each row is a different parameter.

        Returns:
            np.ndarray: Array of probabilities. Each row is a different
            individual, each column is a different item.
        """
        items = np.array(params).shape[1]
        num_abilities = 1
        if np.array(ability).shape != ():
            num_abilities = np.array(ability).shape[0]
        ability = np.tile(np.array([ability]).transpose(), (1, items))

        params = np.tile(params, num_abilities).reshape((2, num_abilities, items))
        return 1 / (1 + np.exp(-params[0] - (params[1] * ability)))

    def estimate_ability_max_lik(
        self,
        params: Union[list, np.ndarray],
        results: Union[list, np.ndarray],
        end=0.00000001,
        eps=0.01,
        eps2=0.1,
    ) -> np.ndarray:
        """
        Estimate the ability of an individual given the item parameters and responses.

        Args:
            params: A list or numpy array representing the item parameters.
            results: A list or numpy array representing the item responses.
            end: The convergence threshold.
            eps: The threshold for detecting a near-singular matrix.

        Returns:
            A numpy array representing the estimated ability.
        """
        params = np.array(params)
        results = np.array(results)
        est = 0.5
        prev_est = 0
        while abs(est - prev_est) > end:
            P = self.p(est, params)[0]
            W = (1 - P) * P
            denom = np.sum(params[1] ** 2 * W)
            if abs(denom) < eps or np.any(np.abs(W) < eps2):
                break
            prev_est = est
            est = est + (np.sum(params[1] * W * ((results - P) / W)) / denom)
        return est

    def estimate_item_params_max_lik(
        self,
        ability: Union[list, np.ndarray],
        result: Union[list, np.ndarray],
        sigm_orig=-1,
        lamb_orig=1,
        end=0.00001,
        eps=0.1,
    ) -> np.ndarray:
        """
        Estimate the parameters of the model given the abilities and item responses.

        Args:
            ability: A list or numpy array containing the abilities of individuals.
            result: A list or numpy array representing the item responses.
            sigm_orig: The initial value for the parameter sigm.
            lamb_orig: The initial value for the parameter lamb.
            end: The convergence threshold.
            eps: The threshold for detecting a near-singular matrix.

        Returns:
            A numpy array representing the estimated parameters.
        """
        ability = np.array(ability)
        result = np.array(result)
        est = [sigm_orig, lamb_orig]
        prev_est = [0, 0]
        while abs(est[0] - prev_est[0]) > end or abs(est[1] - prev_est[1]) > end:
            P = self.p(ability, [[est[0]], [est[1]]]).transpose()[0]
            W = P * (1 - P)
            L11 = -np.sum(W)
            L12 = -np.sum(ability * W)
            L22 = -np.sum(ability**2 * W)
            L = np.array([[L11, L12], [L12, L22]])
            if abs(np.linalg.det(L)) < eps:
                break
            L_inv = np.linalg.inv(L)

            obs_mat = np.array([np.sum(result - P), np.sum((result - P) * ability)])
            prev_est = est
            est = est - np.matmul(L_inv, obs_mat)
        return est

    def convert_param_form(self, params):
        """
        Convert item parameters from one form to another.

        Args:
            params: A list or numpy array representing the item parameters.

        Returns:
            A numpy array representing the converted item parameters.
        """
        return np.array([-params[0] / params[1], 1 / params[1]])
