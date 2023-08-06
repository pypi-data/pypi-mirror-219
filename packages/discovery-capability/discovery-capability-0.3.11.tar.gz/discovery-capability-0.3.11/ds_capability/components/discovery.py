import pyarrow as pa
import pyarrow.compute as pc

class DataDiscovery(object):


    @staticmethod
    def data_dictionary(canonical: pa.Table, stylise: bool=None):
        """ returns a DataFrame of a data dictionary showing 'Attribute', 'Type', '% Nulls', 'Count',
        'Unique', 'Observations' where attribute is the column names in the df
        Note that the subject_matter, if used, should be in the form:
            { subject_ref, { column_name : text_str}}
        the subject reference will be the header of the column and the text_str put in next to each attribute row

        :param canonical: (optional) the Table to get the dictionary from
        :return: a pandas.DataFrame
        """
        record = []
        labels = [f'Attributes ({len(canonical.columns)})', 'DataType', 'Nulls', 'Dominate', 'Valid', 'Unique',
                  'Observations']
        for c in canonical.column_names:
            col = canonical.column(c)
            line = [c,
                    # data type
                    'Category' if pc.starts_with(str(col.type), 'dict').as_py() else str(col.type),
                    # null percentage
                    round(col.null_count / canonical.num_rows * 100, 1)
                    ]
            # dominant percentage
            arr_vc = col.value_counts()
            value = arr_vc.filter(pc.equal(arr_vc.field(1), pc.max(arr_vc.field(1)))).field(1)[0].as_py()
            line.append(round(value / canonical.num_rows * 100, 1))
            # valid
            line.append(pc.sum(col.is_valid()).as_py())
            # unique
            line.append(pc.count(col.unique()).as_py())
            # observations
            if pa.types.is_dictionary(col.type):
                pass


            record.append(line)


        return record
        #     # Predominant Difference
        #     if len(col.dropna()) > 0:
        #         result = (col.apply(str).value_counts() /
        #                   np.float64(len(col.apply(str).dropna()))).sort_values(ascending=False).values
        #         line.append(round(result[0], 3))
        #         if len(result) > 1:
        #             line.append(round(result[1], 3))
        #         else:
        #             line.append(0)
        #     else:
        #         line.append(0)
        #         line.append(0)
        #     # value count
        #     line.append(col.apply(str).notnull().sum())
        #     # unique
        #     line.append(col.apply(str).nunique())
        #     # Observations
        #     if col.dtype.name == 'category' or col.dtype.name == 'object' or col.dtype.name == 'string':
        #         value_set = list(col.dropna().apply(str).value_counts().index)
        #         if len(value_set) > 0:
        #             sample_num = 5 if len(value_set) >= 5 else len(value_set)
        #             sample = str(' | '.join(value_set[:sample_num]))
        #         else:
        #             sample = 'Null Values'
        #         line_str = 'Sample: {}'.format(sample)
        #         line.append('{}...'.format(line_str[:100]) if len(line_str) > 100 else line_str)
        #     elif col.dtype.name == 'bool':
        #         line.append(str(' | '.join(col.map({True: 'True', False: 'False'}).unique())))
        #     elif col.dtype.name.startswith('int') \
        #             or col.dtype.name.startswith('float') \
        #             or col.dtype.name.startswith('date'):
        #         my_str = 'max=' + str(col.max()) + ' | min=' + str(col.min())
        #         if col.dtype.name.startswith('date'):
        #             my_str += ' | yr mean= ' + str(round(col.dt.year.mean(), 0)).partition('.')[0]
        #         else:
        #             my_str += ' | mean=' + str(round(col.mean(), 2))
        #             dominant = col.mode(dropna=True).to_list()[:2]
        #             if len(dominant) == 1:
        #                 dominant = dominant[0]
        #             my_str += ' | dominant=' + str(dominant)
        #         line.append(my_str)
        #     else:
        #         line.append('')
        #     file.append(line)
        # df_dd = pd.DataFrame(file, columns=labels)
        # report_header = labels[0] if report_header == 'Attributes' else report_header
        # if isinstance(report_header, str) and report_header in labels and isinstance(condition, str):
        #     report_header = labels[0] if report_header == 'Attributes' else report_header
        #     str_value = f"df_dd['{report_header}']{condition}"
        #     try:
        #         df_dd = df_dd.where(eval(str_value)).dropna()
        #     except(SyntaxError, ValueError):
        #         pass
        # df_dd['Count'] = df_dd['Count'].astype('int')
        # df_dd['Unique'] = df_dd['Unique'].astype('int')
        # if not inc_next_dom:
        #     df_dd.drop('%_Nxt', axis='columns', inplace=True)
        # if stylise:
        #     df_style = df_dd.style.set_table_styles(style)
        #     _ = df_style.applymap(DataDiscovery._highlight_null_dom, subset=['%_Null', '%_Dom'])
        #     _ = df_style.applymap(lambda x: 'color: white' if x > 0.98 else 'color: black', subset=['%_Null', '%_Dom'])
        #     _ = df_style.applymap(DataDiscovery._dtype_color, subset=['dType'])
        #     _ = df_style.applymap(DataDiscovery._color_unique, subset=['Unique'])
        #     _ = df_style.applymap(lambda x: 'color: white' if x < 2 else 'color: black', subset=['Unique'])
        #     _ = df_style.format({'%_Null': "{:.1%}", '%_Dom': '{:.1%}'})
        #     _ = df_style.set_caption('%_Dom: The % most dominant element ')
        #     _ = df_style.set_properties(subset=[f'Attributes ({len(df.columns)})'],  **{'font-weight': 'bold',
        #                                                                                 'font-size': "120%"})
        #     if inc_next_dom:
        #         _ = df_style.applymap(DataDiscovery._highlight_next, subset=['%_Nxt'])
        #         _ = df_style.applymap(lambda x: 'color: white' if x < 0.02 else 'color: black', subset=['%_Nxt'])
        #         _ = df_style.format({'%_Null': "{:.1%}", '%_Dom': '{:.1%}', '%_Nxt': '{:.1%}'})
        #         _ = df_style.set_caption('%_Dom: The % most dominant element - %_Nxt: The % next most dominant element')
        #     return df_style
        # return df_dd
