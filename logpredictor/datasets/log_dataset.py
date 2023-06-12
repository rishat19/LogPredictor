import os

import numpy as np
import pandas as pd

from datasets.base_dataset import BaseDataset
from utils.enums import DataProcessTypes, SetTypes


class LogDataset(BaseDataset):
    def __init__(self, dataframe_path: str, preprocess_type, train_set_percent: float, valid_set_percent: float,
                 target: int = -1):
        super(LogDataset, self).__init__(train_set_percent, valid_set_percent)
        df = pd.read_csv(os.path.abspath('').replace('\\', '/').replace('datasets', 'tmp') + dataframe_path)

        if target != -1:
            # define properties
            self.inputs = np.asarray(pd.concat([df.iloc[:, 1:target], df.iloc[:, target + 1:32]], axis=1))
            self.targets = np.asarray(df[df.columns[target]])
            self.dimension = len(self.inputs[0])

            # divide into sets
            self.divide_into_sets()

            # preprocessing
            if preprocess_type == DataProcessTypes.standardization.value:
                self.mean, self.std = self.standardization()
            elif preprocess_type == DataProcessTypes.normalization.value:
                self.normalization()
            else:
                raise Exception('No such preprocessing function')
        else:
            self.inputs = np.asarray(df[df.columns[1:32]])
            self.targets = np.asarray(df[df.columns[1:32]])
            self.dimension = len(self.inputs[0])
            self.mean = np.mean(self.inputs, axis=0).reshape(self.inputs.shape[1], 1)
            self.std = np.std(self.inputs, axis=0).reshape(self.inputs.shape[1], 1)
            self.std[self.std == 0] = 1
            self.inputs = ((self.inputs.T - self.mean) / self.std).T
            self.last_timestamp = np.asarray(df[df.columns[0]])[self.inputs.shape[0] - 1]

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def targets(self):
        return self._targets

    @targets.setter
    def targets(self, value):
        self._targets = value

    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, value):
        self._dimension = value

    def __call__(self, set_type: SetTypes) -> dict:
        inputs, targets = getattr(self, f'inputs_{set_type.name}'), getattr(self, f'targets_{set_type.name}')
        return {'inputs': inputs,
                'targets': targets}
