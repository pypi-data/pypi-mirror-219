import pytest
from openirt import item_models
import numpy as np

# ---GENERIC---

def test_prob_gen():
    params = np.array([[0.45, 0.6], [0.1, 0.15]])
    abilities = np.array([0.55, 1.2])
    def p(ab, params):
        if ab > params[0]:
            return 1
        else:
            return params[1]
    model = item_models.Model(p, num_params=2)
    prob = model.p(abilities, params)
    assert prob.shape == (2,2)
    assert prob[0][0] == 1
    assert prob[0][1] == 0.15
        
# def test_em_mmle_gen():
#     assert False
    
# def test_estimate_ability_gen():
#     assert False

# -----1PL-----

# def test_prob_pl1():
#     params = np.array([[-1.5, 0, 1.5]])
#     abilities = np.array([-1.2, 1.2])
#     pl1 = item_models.PL1()
#     prob = pl1.pl1_p(abilities, params)
#     assert prob.shape == (2,3)
#     assert abs(prob[1][2] - 0.37754) < 0.001
    
# # add simulated_results() to model class
# def test_estimate_item_params_pl1():
#     num_abilities = 100
#     rand_ability = np.random.normal(size=3)
#     pl1 = item_models.PL1()
#     params = np.array([[-1.2, 2]])
#     result = (pl1.pl1_p(rand_ability, params) < np.random.rand(3,2)).astype(int).T
#     est_param = np.array([pl1.estimate_item_params_max_lik(rand_ability, r) for r in result])
#     assert False
#     # assert abs(est_ability- 
    
# # def test_estimate_ability_pl1():
# #     assert False

# # def test_jmle_pl1():
# #     assert False
    
# # -----2PL-----
    
# def test_prob_pl2():
#     assert False

# def test_estimate_item_params_pl2():
#     assert False

# def test_estimate_ability_pl2():
#     assert False

# def test_jmle_pl2():
#     assert False

# # -----3PL-----
    
# def test_prob_pl3():
#     assert False

# def test_estimate_item_params_pl3():
#     assert False

# def test_estimate_ability_pl3():
#     assert False

# def test_jmle_pl3():
#     assert False
    
# # -----Norm-----
    
# def test_prob_norm():
#     assert False

# def test_estimate_item_params_norm():
#     assert False

# def test_estimate_ability_norm():
#     assert False

# def test_jmle_norm():
#     assert False
    
# # ----Graded----

# def test_simulated_response_graded():
#     assert False

# # replace with any method of estimating item parameters
# def test_em_mmle_graded():
#     '''EM/MMLE algorithm for the same 1 parameter model for all items'''
#     assert False
    
# def test_estimate_ability_graded():
#     assert False