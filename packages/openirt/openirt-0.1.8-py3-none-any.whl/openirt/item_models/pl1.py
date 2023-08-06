from model import Model
import numpy as np
from pl2 import PL2


class PL1(Model):
    """
    1-parameter logistic model (Rasch model).
    p(\\theta) = 1 / (1 + e^{-(\\zeta + \\theta)}
    """
    def __init__(self):
        super().__init__(
            PL1.pl1_p,
            num_params=1,
            multi=True,
            prov_params=[0],
            loc_param=0,
            param_bounds=[(-7, 7)],
            loc_param_asc=False,
        )

    @staticmethod
    def pl1_p(
        ability: np.ndarray, 
        params: np.ndarray
    ) -> np.ndarray:
        """
        Probability of a correct response given the ability and item 
        parameters.

        Args:
            ability : np.ndarray 
                Array of abilities.
            params : np.ndarray
                Item parameters. Item parameters. Each column is a different
                item, each row is a different parameter.

        Returns:
            np.ndarray: Array of probabilities. Each row is a different
            individual, each column is a different item.
        """
        return PL2().pl2_p(ability, [params[0], np.ones(len(params[0]))])

    def estimate_ability_max_lik(
        self,
        params: Union[list, np.ndarray],
        results: Union[list, np.ndarray],
        end=0.00000001,
        eps=0.01,
        eps2=0.000001,
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
        return PL2().estimate_ability_max_lik(
            [params[0], np.ones(len(params[0]))], results, end, eps, eps2
        )

    def estimate_item_params_max_lik(
        self,
        ability: Union[list, np.ndarray],
        result: Union[list, np.ndarray],
        sigm_orig=0,
        end=0.0000001,
        eps=0.0001,
    ) -> np.ndarray:
        """
        Estimate the parameters of the model given the abilities and item responses.

        Args:
            ability: A list or numpy array containing the abilities of individuals.
            result: A list or numpy array representing the item responses.
            sigm_orig: The initial value for the parameter sigm.
            end: The convergence threshold.
            eps: The threshold for detecting a near-singular matrix.

        Returns:
            A numpy array representing the estimated parameters.
        """
        ability = np.array(ability)
        result = np.array(result)
        est = sigm_orig
        prev_est = est + 2 * end
        while abs(est - prev_est) > end:
            P = self.pl1_p(ability, [[est]]).transpose()[0]
            L1 = np.sum(result - P)
            L2 = -np.sum(P * (1 - P))

            if abs(L2) < eps:
                break

            prev_est = est
            est = est - L1 / L2
        return np.array([est])
