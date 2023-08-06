import os
import pandas as pd


def check_missing_exif(df, column):
    """
    Filter data frame for null values in column.

    Args:
        df (DataFrame): Data frame of EXIF data
        column (str): Name of column to filter for null values

    Returns:
        DataFrame
    """
    df = df[df[column].isnull()]
    return df


def count_images_by_columns(df, columns, sort=None):
    """
    Group images by column(s) and count images

    Args:
        df (DataFrame): Data frame of EXIF data
        columns (list): List of columns to group by

    Returns:
        DataFrame
    """

    # group and count
    df = df.groupby(columns).size().reset_index()
    df = df.rename(columns={0: 'count'})

    # (optional) sort
    if sort is not None:
        df = df.sort_values(by=sort).reset_index(drop=True)

    return df


def get_column(df, column):
    """Extract column from data frame as list"""
    return df[column].to_list()


def filename2columns(df, filename_col, columns):
    """
    Split the filename column into individual columns.

    Args:
        df (DataFrame): Data frame of EXIF data
        filename_col (str): Name of column in data frame that contains the filenames of images
        columns (list): The filename_col will be split into individual columns using the OS file separator. List the
        names you would like to assign to each column from right to left in the filename. You do not need to assign a
        name to every column. Columns that aren't given names won't be added to the output data frame. For example,
        if the first filename in the filenames_col is
        '~/Documents/Samsung_phones/s20/s20_2/natural/wide/20230417_183817.jpg' and columns=['image', 'camera',
        'scene_type', 'phone', 'model'], an image column will be created with the first entry '20230417_183817.jpg',
        the first entry of the camera column will be 'wide', the first entry of the scene_type column will be
        'natural', the first entry of the phone column will be 's20_2', and the first entry of the model column will
        be 's20'. No columns will be created for 'Documents' or 'Samsung_phones'.

    Returns:
        DataFrame
    """

    for i in range(1, len(columns)+1):
        column = columns.pop()
        df.insert(0, column, df[filename_col].str.split(os.path.sep).str[-i])

    return df


def read_exif(path, filename_col, encoding='utf-8'):
    # read csv
    df = pd.read_csv(path, encoding=encoding)

    # drop file names that start with '.'
    files = get_column(df=df, column=filename_col)
    images = pd.Series([s.split('/')[-1].strip() for s in files])
    df = df[~images.str.startswith('.')]

    return df
