# model.py - Storage access for app
# rcampbel@purdue.edu - 2020-07-14

import os
import csv
import glob
import sys
import pandas as pd

from nb.log import logger

DATA_DIR = 'data'
DATA_FILE = 'loti.csv'
DOWNLOAD_DATA_NAME = 'loti-download'
FLOAT_FORMAT = '0,.4f'

model = sys.modules[__name__]

# The models's "public" attributes are listed here, with type hints, for quick reference
data: pd.DataFrame
results: pd.DataFrame
res_count: int = 0
headers: list
ymin: int
ymax: int

pd.set_option('display.width', 1000)  # Prevent data desc line breaking


def start():
    """Read data and/or prepare to query data."""

    # Load data into memory from file
    model.data = pd.read_csv(os.path.join(DATA_DIR, DATA_FILE), escapechar='#')
    model.headers = list(data.columns.values)

    # Get values for data selection  TODO ennforce data selection limits
    model.ymin = min(data[data.columns[0]])
    model.ymax = max(data[data.columns[0]])

    logger.info('Data load completed')


def set_disp(data=None, limit=None, wide=False):
    """Prep Pandas to display specific number of data lines."""
    if not limit:
        limit = data.shape[0]

    pd.set_option('display.max_rows', limit + 1)

    if wide:
        pd.set_option('display.float_format', lambda x: format(x, FLOAT_FORMAT))


def clear_filter_results():
    """Reset results-tracking attributes."""
    model.results = None
    model.res_count = 0


def filter_data(from_year, to_year):
    '''Use provided values to filter data.'''
    model.results = data[(data[headers[0]] >= int(from_year)) & (data[headers[0]] <= int(to_year))]
    model.res_count = results.shape[0]
    logger.debug('Results: '+str(res_count))


def iterate_data():
    """Get iterator for data."""
    return model.data.itertuples()


def create_download_file(data, file_format_ext):
    """Prep data for export."""

    # First, to save space, delete existing download file(s)
    for filename in glob.glob(DOWNLOAD_DATA_NAME + '.*'):
        os.remove(filename)

    # Create new download file TODO Other download formats
    filename = DOWNLOAD_DATA_NAME + '.' + file_format_ext
    data.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)

    return filename
