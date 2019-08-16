import numpy as np
import pandas as pd


class WriteInExcel:

    def __init__(self, classes={}, file_name='UML_Spreadsheet.xlsx'):
        self.classes = classes
        self.file_name = file_name
        self.writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')

    def create_pandas_dataframe(self, base_class, children=[]):
        number_of_rows = 1+len(children)
        df = pd.DataFrame(index=np.arange(0, number_of_rows),
                          columns=['Parent', 'Children'])
        df.loc[0] = [base_class, '']
        if number_of_rows == 1:
            return df
        for i in range(1, number_of_rows):
            df.loc[i] = ['', children[-1]]
            del children[-1]
        return df

    def form_uml_sheet_for_classes(self):
        for key, value in self.classes.items():
            base_class = key
            children = value
            class_df = self.create_pandas_dataframe(base_class, children)
            self.write_df_to_excel(class_df, base_class)
        self.writer.save()
        self.writer.close()

    def write_df_to_excel(self, df, sheet_name):
        df.to_excel(self.writer, sheet_name=sheet_name,
                    header=True, index=False, )
        print("{} done!".format(sheet_name))
