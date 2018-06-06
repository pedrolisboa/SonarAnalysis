import os
from warnings import warn

from Functions.SystemIO import mkdir, exists
from Functions.TrainParameters import TrnParamsConvolutional


class _Path(object):
    MODEL_INFO_FILE_NAME = 'model_info.jbl'
    MODEL_STATE_FILE_NAME = 'model_state.h5'

    def __init__(self, home):
        # self.subfolders = dict()
        # self.subfolders['home'] = home
        pass

    def add(self, subfolder):
        # self.subfolders[subfolder] = self.home + '/' + sub-folder
        pass

    def createFolder(self):
        """Generate folders accordingly with the object structure"""
        raise NotImplementedError


class ConvolutionPaths(_Path):
    """Class with references to all sub-folders(models and results)
    required for the convolution models training and analysis"""
    results_path = './Analysis'

    def __init__(self, home):
        super(ConvolutionPaths, self).__init__(home)
        self.model_paths = self.getModelPaths(self.results_path)

    def getModelPaths(self, init_path):
        path_list = os.listdir(init_path)

        if self.MODEL_INFO_FILE_NAME in path_list:
            return init_path
        return np.array([self.getModelPaths(init_path + '/' + path) for path in path_list]).flatten()

    def iterModelPaths(self, paramsMask):
        """Generates model paths attending the desired conditions"""

        if not isinstance(paramsMask, TrnParamsConvolutional):
            raise ValueError('The parameters inserted must be an instance of TrnParamsConvolutional'
                             '%s of type %s was passed.'
                             % (paramsMask, type(paramsMask)))

        for model_path in self.models_paths:
            model_params = load(model_path)

            if model_params.fitMask(paramsMask):
                yield model_path


class ModelPaths(ConvolutionPaths):
    def __init__(self, trnParams, home):
        super(ModelPaths, self).__init__(home)
        if not isinstance(trnParams, TrnParamsConvolutional):
            raise ValueError('The parameters inserted must be an instance of TrnPararamsConvolutional'
                             '%s of type %s was passed.'
                             % (trnParams, type(trnParams)))

        self.model_path = self.results_path + '/' + self.genPathStr(trnParams)
        # self.model_date = "%s_%s_%s_%s"%(now.year,now.month,now.day,now.hour)

        self.model_info_file = self.model_path + '/' + 'model_info.jbl'
        self.model_info_file_txt = self.model_path + '/' + 'model_info.txt'
        self.model_file = None
        self.model_history = None
        self.model_predictions = None
        self.model_recovery_state = None
        self.model_recovery_folds = None

    def genPathStr(self, trnParams):
        warn('Test path implemented')

        return trnParams.getParamPath()

    def selectFoldConfig(self, n_folds):
        warn('Implement error handling')

        self.fold_path = self.model_path + '/' + '%i_folds' % n_folds

        self.model_file = self.fold_path + '/' + 'model_state.h5'
        self.model_history = self.fold_path + '/' + 'history.csv'
        self.model_predictions = self.fold_path + '/' + 'predictions'
        self.model_recovery_state = self.fold_path + '/' + '~rec_state.h5'
        self.model_recovery_folds = self.fold_path + '/' + '~rec_folds.jbl'

        if exists(self.model_file):
            return 'Trained'
        # elif exists(self.model_recovery_state):
        #   return 'Recovery'
        else:
            self.createFolders(self.model_path)
            return 'Untrained'

    def createFolders(self, *args):
        """Creates model folder structure from hyperparameters information"""
        for folder in args:
            print folder
            mkdir(folder)

    def purgeFolder(self, subfolder=''):
        raise NotImplementedError
