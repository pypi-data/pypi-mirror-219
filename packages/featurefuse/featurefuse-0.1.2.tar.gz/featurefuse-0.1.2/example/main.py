import argparse
from pathlib import Path

import pandas as pd
import yaml

from featurefuse.generator import run


def _parse_args():
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--feature_config",
        dest="feature_config",
        help="path to config which specify use feature.",
        default="./config/feature.yaml",
        type=str,
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    with open(args.feature_config, mode="r") as f:
        use_feature_config = yaml.safe_load(f)

    data_url = (
        "https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv"
    )
    air_passengers_data = pd.read_csv(data_url)
    print(air_passengers_data)

    air_passengers_data_1000 = air_passengers_data
    air_passengers_data_1000["#Passengers"] = air_passengers_data_1000["#Passengers"] + 1000
    print(air_passengers_data_1000)

    # Make feature
    feature, description = run(
        use_feature_config,
        join_key="Month",  # key column to join each feature DataFrame
        air_passengers_data=air_passengers_data,
        air_passengers_data_1000=air_passengers_data_1000,
    )
    print(feature)
    print(description)

    output_dir = Path("./outputs/")
    output_dir.mkdir(exist_ok=True)

    output_feature = output_dir / "feature.csv"
    feature.to_csv(output_feature, index=False, compression="bz2")

    output_description = output_dir / "description.csv"
    description.to_csv(output_description, index=False)

    # Input to model or something
    # model.train(feature)


if __name__ == "__main__":
    main()
