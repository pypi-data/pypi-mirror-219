import pandas as pd

from featurefuse.base import Feature


class NaiveFeature1(Feature):
    def create_feature(
        self,
        air_passengers_data: pd.DataFrame,
        shift_b_from: int,
        shift_b_to: int,
        **kwargs,
    ) -> pd.DataFrame:

        # Copy only using columns for NaiveFeature1
        fe = air_passengers_data[["Month", "#Passengers"]].copy(deep=True)

        # Lag feature: num of passengers from past {shift_b_from} months to {shift_b_to} months
        self.create_description(
            f"#Passengers_b{shift_b_from} ~ #Passengers_b{shift_b_to}",
            f"num of passengers from past {shift_b_from} months to {shift_b_to} months",
        )
        for i in range(shift_b_from, shift_b_to + 1):
            fe[f"#Passengers_b{i}"] = fe["#Passengers"].shift(i)

        fe = fe.drop("#Passengers", axis="columns")

        return fe


class NaiveFeature2(Feature):
    def create_feature(
        self,
        air_passengers_data_1000: pd.DataFrame,
        rolling_min: int,
        rolling_max: int,
        rolling_mean: int,
        rolling_median: int,
        **kwargs,
    ) -> pd.DataFrame:

        # Copy only using columns for NaiveFeature2
        fe = air_passengers_data_1000[["Month", "#Passengers"]].copy(deep=True)

        # Roll feature: num of passengers from past {shift_b_from} months to {shift_b_to} months
        self.create_description(
            f"#Passengers_min_b{rolling_min}",
            f"min of passenges in the last {rolling_min} month",
        )
        self.create_description(
            f"#Passengers_max_b{rolling_max}",
            f"max of passenges in the last {rolling_max} month",
        )
        self.create_description(
            f"#Passengers_mean_b{rolling_mean}",
            f"mean of passenges in the last {rolling_mean} month",
        )
        self.create_description(
            f"#Passengers_median_b{rolling_median}",
            f"median of passenges in the last {rolling_median} month",
        )

        # min of passengers i month ago
        fe[f"#Passengers_min{rolling_min}"] = fe["#Passengers"].rolling(rolling_min).min()
        # max of passengers i month ago
        fe[f"#Passengers_max{rolling_max}"] = fe["#Passengers"].rolling(rolling_max).max()
        # mean of passengers i month ago
        fe[f"#Passengers_mean{rolling_mean}"] = fe["#Passengers"].rolling(rolling_mean).mean()
        # median of passengers i month ago
        fe[f"#Passengers_median{rolling_median}"] = fe["#Passengers"].rolling(rolling_median).median()

        fe = fe.drop("#Passengers", axis="columns")

        return fe


class NaiveFeature3(Feature):
    def create_feature(self, air_passengers_data: pd.DataFrame, **kwargs) -> pd.DataFrame:

        # Copy only using columns for NaiveFeature3
        fe = air_passengers_data[["Month", "#Passengers"]].copy(deep=True)

        tmp = fe.copy(deep=True)
        for i in range(25):
            tmp[f"#Passengers_b{i}"] = fe["#Passengers"].shift(i)

        # mean of passengers in the same month in the past
        self.create_description(
            "#Passengers_ma",
            "mean of passengers in the same month in the past",
        )
        fe["#Passengers_ma"] = (tmp["#Passengers"] + tmp["#Passengers_b12"] + tmp["#Passengers_b24"]) / 3

        fe = fe.drop("#Passengers", axis="columns")

        return fe


class NaiveFeature4(Feature):
    def create_feature(self, air_passengers_data: pd.DataFrame, **kwargs) -> pd.DataFrame:

        # Copy only using columns for NaiveFeature4
        fe = air_passengers_data[["Month", "#Passengers"]].copy(deep=True)

        # Random feature
        self.create_description("aaa", "bbb")
        fe["aaa"] = 1000

        fe = fe.drop("#Passengers", axis="columns")

        return fe


class NaiveFeature5(Feature):
    def create_feature(self, air_passengers_data: pd.DataFrame, **kwargs) -> pd.DataFrame:

        # Copy only using columns for NaiveFeature5
        fe = air_passengers_data[["Month", "#Passengers"]].copy(deep=True)

        # Random feature
        self.create_description("aaa", "test for existing same name column")
        fe["aaa"] = 1000

        fe = fe.drop("#Passengers", axis="columns")

        return fe
