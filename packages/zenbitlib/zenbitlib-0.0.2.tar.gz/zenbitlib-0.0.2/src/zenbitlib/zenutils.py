from zenbitlib.zenproject import *

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
        working_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        # working_path = os.path.dirname(__file__)
        return working_path
    
    # check project's direction. Create the direction if not existed.
    def check_proj_path(self):
        folder_path = self.workingpath()+ '/results/' + self.proj_name + '/'
        mod_path = self.workingpath()+ '/results/' + self.proj_name + '/mod/'
        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(mod_path, exist_ok=True)

    def zenrandomseed(self, SEED):
        torch.manual_seed(SEED)
        np.random.seed(SEED)
        random.seed(SEED)
        np.random.seed(SEED)
        torch.manual_seed(SEED)
        torch.cuda.manual_seed_all(SEED)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False