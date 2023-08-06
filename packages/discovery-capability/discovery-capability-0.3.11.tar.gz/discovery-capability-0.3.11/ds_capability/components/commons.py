from typing import Any
import pandas as pd
from ds_core.components.core_commons import CoreCommons


class Commons(CoreCommons):

    @staticmethod
    def date2value(dates: Any, day_first: bool = True, year_first: bool = False) -> list:
        """ converts a date to a number represented by to number of microseconds to the epoch"""
        values = pd.Series(pd.to_datetime(dates, errors='coerce', dayfirst=day_first, yearfirst=year_first))
        v_native = values.dt.tz_convert(None) if values.dt.tz else values
        null_idx = values[values.isna()].index
        values.iloc[null_idx] = pd.to_datetime(0)
        result =  ((v_native - pd.Timestamp("1970-01-01")) / pd.Timedelta(microseconds=1)).astype(int).to_list()
        values.iloc[null_idx] = None
        return result

    @staticmethod
    def value2date(values: Any, dt_tz: Any=None, date_format: str=None) -> list:
        """ converts an integer into a datetime. The integer should represent time in microseconds since the epoch"""
        if dt_tz:
            dates = pd.Series(pd.to_datetime(values, unit='us', utc=True)).map(lambda x: x.tz_convert(dt_tz))
        else:
            dates = pd.Series(pd.to_datetime(values, unit='us'))
        if isinstance(date_format, str):
            dates = dates.dt.strftime(date_format)
        return dates.to_list()

