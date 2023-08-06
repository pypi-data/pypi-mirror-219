from zenbitlib.zenproject import *

import datetime
import random
import inspect
import json
import os

from shutil import copyfile
import torch
import matplotlib.pyplot as plt
import numpy as np

class info(zenproject):
    def __init__(self, project_name) -> None:
        super().__init__()
        # Project name
        self.proj_name = project_name
        # Time record
        self.nowTime = self.nowtime()
        # Path record -- Note that: Working_path is the place where the .py file sits. 
        self.working_path = self.workingpath() 
        self.results_path = self.working_path + '/results/' + self.proj_name + '/'
        self.mod_path = self.working_path + '/results/' + self.proj_name + '/mod/'
        self.check_proj_path()
        
    # find current time
    def nowtime(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        return nowTime
    
    # find current file address for main script 
    '''NOT This lib's address!!'''
    def workingpath(self):
        # working_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        working_path = os.path.dirname(os.path.abspath(inspect.getmodule(inspect.currentframe().f_back).__file__))
        return working_path
    
    # check project's direction. Create the direction if not existed.
    def check_proj_path(self):
        os.makedirs(self.results_path, exist_ok=True)
        os.makedirs(self.mod_path, exist_ok=True)

    def zenrandomseed(self, SEED):
        torch.manual_seed(SEED)
        np.random.seed(SEED)
        random.seed(SEED)
        np.random.seed(SEED)
        torch.manual_seed(SEED)
        torch.cuda.manual_seed_all(SEED)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def setting_saver(self, filename):
        # 加载文件
        module = __import__(filename)
        dict = module.__dict__
        dict_str = {}
        for key in dict:
            try:
                dict_str[key] = str(dict[key])
                #dict_str.append({key: dict[key]})
            except:
                print("Something's wrong in reading __dict__'s keys!")
        #dict_str = str(dict_str)
        json_str = json.dumps(dict_str)
        with open(self.working_path + '/results/' + self.proj_name + '/_settings.json', 'w') as json_file:
            json_file.write(json_str)

    # Save the model
    def save_model(self, model):
        try:
            encoder = model.encoder
            decoder = model.decoder
        except:
            print("Make sure the model has 'encoder' and 'decoder'!")
        # Time record
        torch.save(encoder.state_dict(), self.mod_path + '_encoder.pth')
        torch.save(encoder.state_dict(), self.mod_path + self.nowTime + '_encoder.pth')
        torch.save(decoder.state_dict(), self.mod_path + '_decoder.pth')
        torch.save(decoder.state_dict(), self.mod_path + self.nowTime + '_decoder.pth')

    def reload_model(self, model_loaded):
        state_dict_encoder = torch.load(self.mod_path + '_encoder.pth')
        state_dict_decoder = torch.load(self.mod_path + '_decoder.pth')
        model_loaded.encoder.load_state_dict(state_dict_encoder)
        model_loaded.decoder.load_state_dict(state_dict_decoder)
        for param in model_loaded.parameters():
            param.requires_grad = False
        return model_loaded
    
    # Save the figures - from matplotlib    
    def save_fig(self, name_ext):
        plt.savefig(self.results_path + self.nowTime + name_ext) # for archive
        plt.savefig(self.results_path + name_ext) # for the last run

    # Save text to csv - usually for Loss record
    def save_loss(self, loss_record):
        np.savetxt(self.results_path + self.nowTime + '_loss.csv', loss_record, delimiter=',') # for archive
        np.savetxt(self.results_path + '_loss.csv', loss_record, delimiter=',') # for quick inspect

    # save models and other key parameters
    def backup_exp_info(self):
        copyfile(self.working_path + '/AE_Models.py', self.results_path + self.nowTime + '_Backup_AE_Models.py')
        copyfile(self.results_path + '_settings.json', self.results_path + self.nowTime + '_Backup_settings.json')

if __name__ == "__main__":
    info_ = info("test")
    print(info_.working_path)