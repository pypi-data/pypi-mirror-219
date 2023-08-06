import inspect
from typing import Any
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability.components.commons import Commons
from ds_capability.intent.feature_build_model_intent import FeatureBuildModelIntent


class FeatureBuildCorrelateIntent(FeatureBuildModelIntent):

    def correlate_number(self, canonical: pa.Array, choice: [int, float, str]=None, choice_header: str=None,
                         precision: int=None, jitter: [int, float, str]=None, offset: [int, float, str]=None,
                         code_str: Any=None, lower: [int, float]=None, upper: [int, float]=None, keep_zero: bool=None,
                         seed: int=None, save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                         replace_intent: bool=None, remove_duplicates: bool=None) -> list:
        """ correlate a list of continuous values adjusting those values, or a subset of those values, with a
        normalised jitter (std from the value) along with a value offset. ``choice``, ``jitter`` and ``offset``
        can accept environment variable string names starting with ``${`` and ending with ``}``.

        If the choice is an int, it represents the number of rows to choose. If the choice is a float it must be
        between 1 and 0 and represent a percentage of rows to choose.

        :param canonical:
        :param choice: (optional) The number of values to choose to apply the change to. Can be an environment variable.
        :param choice_header: (optional) those not chosen are given the values of the given header
        :param precision: (optional) to what precision the return values should be
        :param offset: (optional) a fixed value to offset or if str an operation to perform using @ as the header value.
        :param code_str: (optional) passing a str lambda function. e.g. 'lambda x: (x - 3) / 2''
        :param jitter: (optional) a perturbation of the value where the jitter is a random normally distributed std
        :param precision: (optional) how many decimal places. default to 3
        :param seed: (optional) the random seed. defaults to current datetime
        :param keep_zero: (optional) if True then zeros passed remain zero despite a change, Default is False
        :param lower: a minimum value not to go below
        :param upper: a max value not to go above
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: an equal length list of correlated values
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        s_values = canonical.to_pandas()
        s_others = s_values.copy()
        other_size = s_others.size
        seed = self._seed() if seed is None else seed
        offset = self._extract_value(offset)
        keep_zero = keep_zero if isinstance(keep_zero, bool) else False
        precision = precision if isinstance(precision, int) else 3
        lower = lower if isinstance(lower, (int, float)) else float('-inf')
        upper = upper if isinstance(upper, (int, float)) else float('inf')
        # mark the zeros and nulls
        null_idx = s_values[s_values.isna()].index
        zero_idx = s_values.where(s_values == 0).dropna().index if keep_zero else []
        # choose the items to jitter
        if isinstance(choice, (str, int, float)):
            size = s_values.size
            choice = self._extract_value(choice)
            choice = int(choice * size) if isinstance(choice, float) and 0 <= choice <= 1 else int(choice)
            choice = choice if 0 <= choice < size else size
            gen = np.random.default_rng(seed=seed)
            choice_idx = gen.choice(s_values.index, size=choice, replace=False)
            choice_idx = [choice_idx] if isinstance(choice_idx, int) else choice_idx
            s_values = s_values.iloc[choice_idx]
        if isinstance(jitter, (str, int, float)) and s_values.size > 0:
            jitter = self._extract_value(jitter)
            size = s_values.size
            gen = np.random.default_rng(seed)
            results = gen.normal(loc=0, scale=jitter, size=size)
            s_values = s_values.add(results)
        # set code_str
        if isinstance(code_str, str) and s_values.size > 0:
            if code_str.startswith('lambda'):
                s_values = s_values.transform(eval(code_str))
            else:
                code_str = code_str.replace("@", 'x')
                s_values = s_values.transform(lambda x: eval(code_str))
        # set offset for all values
        if isinstance(offset, (int, float)) and offset != 0 and s_values.size > 0:
            s_values = s_values.add(offset)
        # set the changed values
        if other_size == s_values.size:
            s_others = s_values
        else:
            s_others.iloc[s_values.index] = s_values
        # max and min caps
        s_others = pd.Series([upper if x > upper else x for x in s_others])
        s_others = pd.Series([lower if x < lower else x for x in s_others])
        if isinstance(keep_zero, bool) and keep_zero:
            if other_size == zero_idx.size:
                s_others = 0 * zero_idx.size
            else:
                s_others.iloc[zero_idx] = 0
        if other_size == null_idx.size:
            s_others = np.nan * null_idx.size
        else:
            s_others.iloc[null_idx] = np.nan
        s_others = s_others.round(precision)
        if precision == 0 and not s_others.isnull().any():
            s_others = s_others.astype(int)
        rtn_list = s_others.to_list()
        rtn_arr = pa.NumericArray.from_pandas(rtn_list)
        if rtn_arr.type.equals('double'):
            try:
                rtn_arr = pa.array(rtn_arr, pa.int64())
            except pa.lib.ArrowInvalid:
                pass
        column_name = column_name if isinstance(column_name, str) else next(self.label_gen)
        return pa.table([rtn_arr], names=[column_name])

