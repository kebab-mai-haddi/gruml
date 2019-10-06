import numpy as np
import pandas as pd


class WriteInExcel:

    def __init__(self, file_name='UML_Spreadsheet.xlsx'):
        self.file_name = file_name
        self.writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')

    # def create_pandas_dataframe(self, base_class, children=[]):
    #     number_of_rows = 1+len(children)
    #     df = pd.DataFrame(index=np.arange(0, number_of_rows),
    #                       columns=['Parent', 'Children'])
    #     df.loc[0] = [base_class, '']
    #     if number_of_rows == 1:
    #         return df
    #     for i in range(1, number_of_rows):
    #         df.loc[i] = ['', children[-1]]
    #         del children[-1]
    #     return df

    def get_number_of_rows_in_df(self, agg_data):
        number_of_rows = 0
        for class_dict in agg_data:
            number_of_rows += 1 + \
                len(class_dict['Methods']) + len(class_dict['Children'])
        return number_of_rows

    def create_pandas_dataframe(self, agg_data):
        number_of_rows = self.get_number_of_rows_in_df(agg_data)
        df = pd.DataFrame(
            index=np.arange(0, number_of_rows),
            columns=['Dependents', 'Parent', 'Methods/Children']
        )
        row_counter = 0
        prev_class_row_counter = 0
        for class_data in agg_data:
            base_class = class_data['Class']
            methods = class_data['Methods']
            children = class_data['Children']
            dependents = class_data['Dependents']
            df.loc[row_counter] = ['', base_class, '']
            row_counter += 1
            for method in methods:
                df.at[row_counter, 'Methods/Children'] = method
                row_counter += 1
            for child in children:
                df.at[row_counter, 'Methods/Children'] = child
                row_counter += 1
            for dependent in dependents:
                df.at[prev_class_row_counter+1, 'Dependents'] = dependent
                prev_class_row_counter += 1
                row_counter += 1
            prev_class_row_counter = row_counter
        # convert all NaN to None.
        df = df.replace(np.nan, '', regex=True)
        print("Create DF was called.")
        print(df)
        return df

    # def form_uml_sheet_for_classes(self):
    #     for key, value in self.classes.items():
    #         base_class = key
    #         children = value
    #         class_df = self.create_pandas_dataframe(base_class, children)
    #         self.write_df_to_excel(class_df, base_class)
    #     self.writer.save()
    #     self.writer.close()

    def write_df_to_excel(self, df, sheet_name):
        df.to_excel(self.writer, sheet_name=sheet_name,
                    header=True, index=False, )
        self.writer.save()
        self.writer.close()
        print("{} done!".format(sheet_name))