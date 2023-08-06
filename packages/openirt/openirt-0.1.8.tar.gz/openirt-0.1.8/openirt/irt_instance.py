
import os
import pandas as pd
# from pl1 import PL1
from pl2 import PL2
# from pl3 import PL3
from norm_model import NormModel

class IRTInstance():
    def __init__(self, 
             results_file: str,
             model: str,
             labeled: bool = True,
             item_params_file: str = None,
             ability_file: str = None,
             row: str = None,
             col: str = None) -> None:
        
        # Read the results file
        self.results = self.read_file(results_file, labeled, labeled)
        if not self.isDichotomous(self.results):
            raise ValueError('Results file must be a binary table.')
        self.setDimensions(row, col)
        
        # Read the item parameters file
        if item_params_file:
            self.item_params = self.read_file(item_params_file, rowLabel=False, colLable=labeled)
        else:
            self.item_params = None
        self.check_item_params()
            
        # Read the ability file
        if ability_file:
            self.abilities = self.read_file(ability_file, rowLabel=False, colLable=labeled)
        else:
            self.abilities = None
        self.check_subjects()
        
        self.set_model(model)
        
    def set_model(self, model: str) -> None:
        if model == '1pl':
            self.model = PL1()
        elif model == '2pl':
            self.model = PL2()
        elif model == '3pl':
            self.model = PL3()
        elif model == 'norm':
            self.model = NormModel()
        else:
            raise ValueError('Model must be one of 1pl, 2pl, 3pl, or norm.')
        
    def read_file(self, file_name: str, rowLabel: bool, colLable: bool):
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"{file_name} not found")
        
        frmat = file_name.split(".")[-1]
        if frmat == "csv":
            if rowLabel:
                index_col = 0
            else:
                index_col = None
            if colLable:
                header = 0
            else:
                header = None
            return pd.read_csv(file_name, index_col=index_col, header=header)
        elif frmat == "json":
            data = self.read_json(file_name)
        elif frmat == "xlsx":
            data = self.read_xlsx(file_name)
        else:
            raise ValueError('Incorrect file format. Only csv, json, and xlsx files are allowed.')
                
    def isDichotomous(self, data) -> bool:
        # Check if any value in the table is not 0 or 1
        invalid_values = (data != 0) & (data != 1)
        return not invalid_values.any().any()
        
    def setDimensions(self, row: str, col: str) -> None:
        if row == 'item' or col == 'subject':
            self.items = self.results.index
            self.subjects = self.results.columns
        else:
            self.items = self.results.columns
            self.subjects = self.results.index
            
    def check_subjects(self):
        if self.abilities is not None:
            if not self.subjects.equals(self.abilities.columns):
                raise ValueError('Subjects in results file and ability file must be the same.')
            
    def check_item_params(self):
        if self.item_params is not None:
            if not self.items.equals(self.item_params.columns):
                raise ValueError('Items in results file and item parameters file must be the same.')
    
    def train_model(self):
        # print(self.results)
        abilities, params = self.model.train_em_mle(self.results)
        
        # self.model.plot_item_curve(params)
        pass
    
    def estimate_item_params(self):
        pass
    
    def estimate_abilities(self):
        pass
    
    def save_item_params(self, dir: str = './'):
        pass
    
    def save_abilities(self, dir: str = './'):
        pass
        
    def saveICC(self, dir: str):
        pass
    