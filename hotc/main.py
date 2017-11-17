from pathlib import Path
import os
import datetime as dt
from functools import partial

from requests_futures.sessions import FuturesSession
import pandas as pd


_ROOT = Path(os.path.abspath(os.path.dirname(__file__)))
_DATA_DIR = _ROOT/'data'
COUNTERS = pd.read_csv(_DATA_DIR/'hotc_counters.csv')

DATE_FORMAT = '%Y-%m-%d'
MAX_WORKERS = 30

def to_df(hotc_data):
    """
    Given a dictionary of the form output by the function
    :func:`parse_hotc` with ``as_df=False``,
    convert it into a DataFrame and return the result.
    """
    frames = []
    period = hotc_data['period']
    records = hotc_data['records']
    for r in records:
        f = pd.DataFrame(r['periodValues'])
        f['datetime'] = f['label'].map(pd.to_datetime)
        f['location_code'] = r['code']
        f['location_name'] = r['title']
        f[period + '_total'] = r['total']
        f[period + '_total_last_year'] = r['totalLastYear']
        f[period + '_total_average'] = r['totalAverage']
        frames.append(f)
    g = pd.concat(frames)

    # Rename some
    del g['label']
    g = g.rename(columns={
        'totalAverage': 'total_average',
        'totalLastYear': 'total_last_year',
    })

    return g

def parse_hotc(period, response, as_df=True):
    """
    Given a period (string; one of 'day', 'week', 'month', or 'year')
    and a successful Heart of the City API GET response,
    return a dictionary with the keys and values

    - ``'period'``: ``period``
    - ``'records'``: response.json()

    if not ``as_df``.
    If ``as_df``, then return instead the same data in the form of
    a DataFrame output by the function :func:`to_df`.
    """
    result = {'period': period, 'records': response.json()}
    if as_df:
        result = to_df(result)

    return result

def get_hotc(dates, period, date_format=DATE_FORMAT, as_df=True):
    """
    Issue asynchronous GET requests to the Heart of the City API to get
    walking counts for the given list of dates (date strings in the
    format ``date_format``) and period (one of ``'day'``, ``'week'``,
    ``'month'``, or ``'year'``).
    Return a dictionary of the form date -> parsed response, only
    including dates for which a valid response was received.

    If ``as_df``, then the parsed response is a DataFrame of the
    form output by the function :func:`to_df`.
    Otherwise, the parsed response is the dictionary
    {'period': ``period``, 'records': response as JSON}.

    NOTES:

    - A Heart of the City day runs from 06:00:00 on a given date to
      05:59:59 on the following date.
    """
    periods = ['day', 'week', 'month', 'year']
    if period not in periods:
        raise ValueError('Period must lie in {!s}'.format(periods))

    session = FuturesSession(max_workers=MAX_WORKERS)
    url = 'http://www.heartofthecity.co.nz/pedestrian-count//api/reveal'

    def format_date(date):
        """Format date for HOTC API to read"""
        return dt.datetime.strptime(date, date_format).strftime(
          '%m/%d/%Y')

    def parse(date, session, response):
        if response.status_code == 200:
            data = (date, parse_hotc(period, response, as_df))
        else:
            data = None
        response.data = data

    futures = (session.get(url,
      params={'method': period, 'date': format_date(date)},
      background_callback=partial(parse, date))
      for date in dates)

    return dict([f.result().data for f in futures if f.result().data])
