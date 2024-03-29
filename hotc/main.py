from __future__ import annotations
from pathlib import Path
import os
import datetime as dt
from typing import Literal

import requests as rq
import pandas as pd


_ROOT = Path(os.path.abspath(os.path.dirname(__file__)))
COUNTERS = pd.read_csv(_ROOT / "data" / "counters.csv")
DATE_FORMAT = "%Y%m%d"


def to_df(hotc_data: dict) -> pd.DataFrame:
    """
    Given a dictionary of the form output by the function
    :func:`parse_hotc` with ``as_df=False``,
    convert it into a DataFrame with the columns

    - ``'datetime'``
    - ``'counter_id'``
    - ``'counter_name'``
    - ``'total'``
    - ``'total_last_year'``
    - ``'total_average'``
    - ``'<period>_total'``
    - ``'<period>_total_last_year'``
    - ``'<period>_total_average'``,

    where <period> is 'day', 'week', 'month', or 'year',
    depending on the API call issued.
    Drop rows with NA counter name.
    """
    frames = []
    period = hotc_data["period"]
    records = hotc_data["records"]
    for r in records:
        f = pd.DataFrame(r["periodValues"])
        f["datetime"] = f["label"].map(pd.to_datetime)
        f["counter_id"] = r["code"]
        f["counter_name"] = r["title"]
        f[period + "_total"] = r["total"]
        f[period + "_total_last_year"] = r["totalLastYear"]
        f[period + "_total_average"] = r["totalAverage"]
        frames.append(f)

    # Rename some
    return (
        pd.concat(frames)
        .rename(
            columns={
                "totalAverage": "total_average",
                "totalLastYear": "total_last_year",
            }
        )
        .drop("label", axis=1)
        .dropna(subset="counter_name")
        .filter(
            ["datetime", "counter_id", "counter_name"]
            + [c for c in f.columns if "total" in c or "year" in c or "average" in c]
        )
    )


def parse_hotc(
    period: Literal["day", "week", "month", "year"],
    response: rq.Response,
    *,
    as_df: bool = True,
) -> dict | pd.DataFrame:
    """
    Given a period (string; one of "day", "week", "month", or "year")
    and a successful Heart of the City API GET response,
    return a dictionary with the keys and values

    - ``"period"``: ``period``
    - ``"records"``: response.json()

    if not ``as_df``.
    If ``as_df``, then return instead the same data in the form of
    a DataFrame output by the function :func:`to_df`.
    """
    result = {"period": period, "records": response.json()}
    if as_df:
        result = to_df(result)

    return result


def format_date(date: str, date_format: str = DATE_FORMAT) -> str:
    """Format date for HOTC API to read"""
    return dt.datetime.strptime(date, date_format).strftime("%m/%d/%Y")


def get_hotc(
    date: str,
    period: Literal["day", "week", "month", "year"],
    date_format=DATE_FORMAT,
    *,
    as_df=True,
) -> dict | pd.DataFrame:
    """
    Issue a GET request to the Heart of the City API to get
    walking counts for the given date (date string in the
    format ``date_format``) and period (one of ``"day"``, ``"week"``,
    ``"month"``, or ``"year"``).
    Return the resulting JSON response (dictionary) or None if no response.

    If ``as_df``, then the parse the response as a DataFrame of the
    form output by the function :func:`to_df`.

    NOTES:

    - A Heart of the City day runs from 06:00:00 on a given date to
      05:59:59 on the following date.
    """
    url = "https://www.heartofthecity.co.nz/pedestrian-count/api/reveal"

    def parse(response):
        if response.status_code == 200 and response.json():
            result = parse_hotc(period, response, as_df=as_df)
        else:
            result = None
        return result

    return parse(
        rq.get(
            url,
            params={"method": period, "date": format_date(date, date_format)},
        )
    )
