import logging
import textwrap
from importlib.util import module_from_spec, spec_from_file_location
from typing import Union

import pandas as pd

log = logging.getLogger(__name__)


def run(
    feature_config: dict,
    join_key: str,
    **kwargs,
) -> Union[pd.DataFrame, pd.DataFrame]:
    """
    Make features which are specified in feature_config.

    Args:
        feature_config (dict): feature info (making feature list and feature params) which you want to make
        # TODO: Can I use just feature_config?
        fe_dict (dict): List of implemented features. Here you must instantiate each feature class.
                        You can only specify feature from this listed feature in config.

    Returns:
        Union[pd.DataFrame, pd.DataFrame]: Made feature DataFrame and made feature description.
    """

    use_feature = feature_config["use_feature"]

    if "feature_params" in feature_config:
        feature_params = feature_config["feature_params"]
    else:
        feature_params = dict()

    joined_df = pd.DataFrame([])
    descriptions = []

    for fe in use_feature:
        # Import and instantiate only use_feature class written in feature config.
        #   https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        #   https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
        fe_splitted = fe.split(".")
        filepath, fe_clsname = ".".join(fe_splitted[:-1]), fe_splitted[-1]
        module_path = f".{filepath.replace('.', '/')}.py"
        spec = spec_from_file_location(module_path, module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        fe_cls = getattr(module, fe_clsname)()

        if fe_clsname in feature_params and feature_params[fe_clsname] is not None:
            df, description = fe_cls.run(**kwargs, **feature_params[fe_clsname])
        else:
            df, description = fe_cls.run(**kwargs)

        description = pd.DataFrame.from_dict(description)
        descriptions.append(description)
        if joined_df.empty:
            joined_df = df
        else:
            joined_df = pd.merge(
                joined_df,
                df,
                how="left",
                on=join_key,
                suffixes=["", "_duplicated_columns"],
            )
            joined_df = joined_df.filter(regex="^(?!.*_duplicated_columns$)", axis="columns")
            dropped_cols = joined_df.filter(regex="(?!.*_duplicated_columns$)", axis="columns").columns
            message = f"dropped columns because of duplicated column name : {dropped_cols}"
            log.info(message)

        if len(joined_df) != len(df):
            error_msg = textwrap.indent(
                textwrap.dedent(
                    f"""
            Inavalid numbers of rows.
            Output: {len(df)}
            Expected: {len(joined_df)}
            """
                ),
                " " * 3,
            )
            raise ValueError(error_msg)

    descriptions = pd.concat(descriptions, axis="rows", ignore_index=True)

    return joined_df, descriptions
