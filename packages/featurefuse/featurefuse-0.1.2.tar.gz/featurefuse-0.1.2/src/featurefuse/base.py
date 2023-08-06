import logging
import time
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from typing import Union

import pandas as pd

log = logging.getLogger(__name__)


@contextmanager
def timer(name):
    t0 = time.time()
    log.info(f"[{name}] start")
    yield
    log.info(f"[{name}] done in {time.time() - t0:.0f} s")


class Feature(metaclass=ABCMeta):
    """
    Feature abstract class. If you inherit Feature class, you can choose inherited Feature class using yaml.
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self.descriptions = {
            "feature_class_name": [],
            "feature_column_name": [],
            "description": [],
        }

    @abstractmethod
    def create_feature(self, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def run(self, **kwargs) -> Union[pd.DataFrame, dict]:
        """
        Making features specified in yaml

        Returns:
            Union[pd.DataFrame, dict]: Made feature in DataFrame and made feature's desciption
        """
        with timer(self.name):
            fe = self.create_feature(**kwargs)
        return fe, self.descriptions

    def create_description(self, col_name: str, description: str) -> None:
        """
        Add feature's description to instance variables

        Args:
            col_name (str): column name which add descripion
            description (str): col_name's description
        """
        existed_cols = self.descriptions["feature_column_name"]
        if col_name in existed_cols:
            return

        self.descriptions["feature_class_name"].append(self.name)
        self.descriptions["feature_column_name"].append(col_name)
        self.descriptions["description"].append(description)
