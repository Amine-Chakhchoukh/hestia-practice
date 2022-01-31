import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal


def improve_format(path, terms_to_merge_on, out_name="output.csv"):
    """" This function will take a dataframe and improve its format
     terms_to_merge_on is an array of..
     extra_matches is a dictionary"""

    df = csv_to_df(path)

    columns_with_terms = get_columns_last_path_component(df, terms_to_merge_on)
    short_cols, long_cols = get_linked_columns(columns_with_terms)
    df_output = do_self_merge(df, short_cols, long_cols)

    df_to_csv(df_output, out_name)

    return df_output


def csv_to_df(path):
    df = pd.read_csv(path)
    df.replace({'-': np.nan}, inplace=True)

    return df


def get_columns_last_path_component(df, terms_to_merge_on):
    cols = []
    for col_name in df.columns:
        if any(term == col_name.split('.')[-1] for term in terms_to_merge_on):
            cols.append(col_name)

    return cols


def get_linked_columns(columns_with_terms):
    # First, find the 'basic/building blocks' column names, such as: cycle.@id
    build_blocks_cols = []
    for col_name in columns_with_terms:
        if len(col_name.split('.')) == 2 and col_name not in build_blocks_cols:
            build_blocks_cols.append(col_name)

    longer_cols = []
    to_remove = []
    for i in build_blocks_cols:
        not_found = True
        for j in columns_with_terms:
            if i != j and i.split('.')[-2] == j.split('.')[-2]:
                longer_cols.append(j)
                not_found = False
        if not_found:
            to_remove.append(i)

    build_blocks_cols = [col for col in build_blocks_cols if col not in to_remove]

    return build_blocks_cols, longer_cols


def do_self_merge(df, short_cols, long_cols):
    df_current = df

    for left_column, right_column in zip(short_cols, long_cols):

        if right_column not in df_current.columns:
            left_column, right_column = right_column, left_column

        df_current = pd.merge(df.dropna(subset=[left_column]), df_current,
                              left_on=left_column,
                              right_on=right_column,
                              how='inner').dropna(axis=1, how='all')

        # clean-up names of columns after the merge
        df_current.columns = df_current.columns.str.replace('_x', '')
        df_current.columns = df_current.columns.str.replace('_y', '')

    # get back the original order of the columns
    df_current = df_current[df.columns]

    # sort out dtypes: numerical & boolean
    df_current = df_current.apply(pd.to_numeric, errors='ignore')
    df_current.replace({'true': True, 'false': False}, inplace=True)

    return df_current


def df_to_csv(df, out_name):
    return df.to_csv(out_name)