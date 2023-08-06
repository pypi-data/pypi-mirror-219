import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
DataLoader()
# This section, we develop a data loader for tseries learning

# Suppose we have features X and labels y with same length

# we use 60% for training, 20% for validation, 20% for testing

# and then, move the training window to the next.

N = 10000
batch_number = 7

# 我们需要移动6次, 也就是 batch_size + 6 * 0.2 * batch_size = N

# suppose Now, we have the dataset, that is, we can access the data using __getitem__

# now we create a data loader


class TSDataLoader0(object):
    def __init__(self, dataset, batch_size=7, step_ratio=0.2):
        self.dataset = dataset
        self.batch_size = batch_size
        self.step_ratio = step_ratio

        self.len_batch = len(dataset) // (1 + step_ratio)
        self.current_index = self.len_batch
        self.step_size = self.len_batch * step_ratio

    # def _get_iterator(self):
    #     pass

    def __iter__(self):
        return self

    def __next__(self):
        train_batch = self.dataset[: self.current_index - 2 * self.step_size]
        validation_batch = self.dataset[self.current_index - 2 * self.step_size: self.current_index - self.step_size]
        test_batch = self.dataset[self.current_index - self.step_size: self.current_index]

        self.current_index += self.step_size
        if self.current_index > len(self.dataset):
            raise StopIteration

        return train_batch, validation_batch, test_batch


class TSDataLoader1(object):
    def __init__(self, dataset, batch_size=7, step_ratio=0.2):
        self.dataset = dataset
        self.batch_size = batch_size
        self.step_ratio = step_ratio

        self.len_batch = len(dataset) // (1 + step_ratio)
        self.current_index = self.len_batch
        self.step_size = self.len_batch * step_ratio

    # def _get_iterator(self):
    #     pass

    def __iter__(self):
        return self

    def __next__(self):
        train_batch = self.dataset[self.current_index-self.len_batch: self.current_index - 2 * self.step_size]
        validation_batch = self.dataset[self.current_index - 2 * self.step_size: self.current_index - self.step_size]
        test_batch = self.dataset[self.current_index - self.step_size: self.current_index]

        self.current_index += self.step_size
        if self.current_index > len(self.dataset):
            raise StopIteration

        return train_batch, validation_batch, test_batch


