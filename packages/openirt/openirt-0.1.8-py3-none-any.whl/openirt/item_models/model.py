import numpy as np
import matplotlib.pyplot as plt


class Model:
    """
    Class for item response theory models, e.g. Pl1.

    Attributes
    ----------
    p : callable
        Function that calculates the probability of a correct response given
        the ability and item parameters. For example, see pl1_p in pl1.py.
    num_params : int
        Number of item parameters. For example the 
        ref:`PL3 <openirt.models.PL3>` models uses 3 parameters: a, b, and c.
    prov_params : list
        Provisional item parameters, used when EM algorithm is initiated.
    loc_param : int
        Index of location parameter. For example, for the PL3 model with item
        parameters (a,b,c), b is the location parameter, so ``loc_param=1``.
    param_bounds : list
        Minimum and maximum values for each item, for example 
        ``[(0,1), (-5, 5)]``
        for some model with ``num_params=2``.
    loc_param_asc : bool
        True if a higher value for the location parameter results in an overall
        smaller probability of success.
        
    Methods
    -------
    
    """

    def __init__(
        self,
        p: callable,
        num_params: int,
        multi: bool = False,
        prov_params: list = None,
        loc_param: int = None,
        param_bounds: list = None,
        loc_param_asc: bool = True,
    ) -> None:
        """
        Initialize model.

        Parameters
        ----------
            p : callable
                Function that calculates the probability of a correct response
                given the ability and item parameters. For example,
                see pl1_p in pl1.py.
            num_params : int
                Number of item parameters. For example the PL3 models uses 3
                parameters: a, b, and c.
            multi : bool, optional
                True if p accepts an array of parameters, false if it accepts a
                single ability and parameters for a single item. Defaults to
                False.
            prov_params : list, optional
                Provisional item parameters, used when EM algorithm is
                initiated. Defaults to None.
            loc_param : int, optional
                Index of location parameter. For example, for the PL3 model
                with item parameters (a,b,c),
                b is the location parameter, so loc_param=1. Defaults to None.
            param_bounds : list, optional
                Minimum and maximum values for each item, for example
                [(0,1), (-5, 5)] for some model with num_params=2.
                Defaults to None.
            loc_param_asc : bool, optional
                True if a higher value for the location parameter results in an
                overall smaller probability of success. Defaults to True.
        """
        if multi:
            self.p = p
        else:
            self.p = lambda abilities, params: np.array(
                [[p(ability, param) for param in params.T] for ability in abilities]
            )
        self.num_params = num_params
        self.prov_params = prov_params
        self.loc_param = loc_param
        self.param_bounds = param_bounds
        self.loc_param_asc = loc_param_asc

    def plot_icc(self, params: np.ndarray):
        """
        Plot item characteristic curve for each item.

        Args:
            params : np.ndarray
                Item parameters. Each column is a different item, each row is a
                different parameter.
        """
        ability = np.linspace(-5, 5, 100)
        for i in range(params.shape[1]):
            plt.plot(
                ability,
                self.p(ability, params[:, i].reshape(params.shape[0], 1)),
                label=f"Question{i+1}",
            )
        plt.legend()
        plt.show()

    def estimate_ability_max_lik(
        self,
        params: np.ndarray,
        results: np.ndarray,
    ) -> np.ndarray:
        raise NotImplementedError(
            "Generic models cannot estimate ability using maximum liklihood estimation."
        )

    def estimate_item_params_max_lik(
        self, ability: np.ndarray, result: np.ndarray
    ) -> np.ndarray:
        raise NotImplementedError(
            "Generic models cannot estimate parameters using maximum liklihood estimation."
        )

    def jmle_em(
        self, responses: np.ndarray, eps: float, max_iterations: int = 1000
    ) -> tuple:
        """
        Estimate abilities and item parameters using the EM algorithm with
        joint maximum liklihood estimation.

        Args:
            responses : np.ndarray
                Responses to items. Each row is a different subject, each
                column is a different item.
            eps : float
                Convergence threshold.
            max_iterations : int, optional
                Maximum number of iterations. Defaults to 1000.

        Returns:
            tuple: Estimated abilities and item parameters.
        """
        responses = np.array(responses)
        subjects, items = responses.shape
        abilities = np.zeros(subjects)
        prev_abilities = abilities + 2 * eps
        iteration = 0
        while (
            np.any(np.abs(abilities - prev_abilities) > eps)
            and iteration < max_iterations
        ):
            params = np.array(
                [
                    self.estimate_item_params_max_lik(abilities, responses[:, i])
                    for i in range(items)
                ]
            ).T
            prev_abilities = abilities
            abilities = np.array(
                [
                    self.estimate_ability_max_lik(params, responses[i])
                    for i in range(subjects)
                ]
            )
            iteration += 1
        return abilities, params

    def simulated_responses(
        self, abilities: np.ndarray, params: np.ndarray
    ) -> np.ndarray:
        """Randomly generate responses given abilities and item parameters.

        Args:
            abilities (np.ndarray): Array of abilities.
            params (np.ndarray): Item parameters. Each column is a different item, each row is a different parameter.

        Returns:
            np.ndarray: Simulated responses. Each row is a different subject, each column is a different item.
        """
        prob = self.p(abilities, params)
        return (np.random.rand(prob.shape[0], prob.shape[1]) < prob).astype(int)
