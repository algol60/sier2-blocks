import param
import pandas as pd
import panel as pn
from sier2 import InputBlock, Block

class SimpleTable(Block):
    """ Simple Table Viewer
    """

    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe')
    
    df_pane = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    @param.depends('df_pane.selection', watch=True)
    def set_output(self):
        print(self.df_pane.selected_dataframe)
        self.out_df = self.df_pane.selected_dataframe

    def execute(self):
        if self.in_df is not None:
            self.df_pane.value = self.in_df
        else:
            self.df_pane.value = pd.DataFrame()

    def __panel__(self):
        return pn.Card(self.df_pane)

class SimpleTable2(Block):
    """ Simple Table Viewer
    """

    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe')
    
    df_pane = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    @param.depends('df_pane.selection', watch=True)
    def set_output(self):
        print((self, self.df_pane.selected_dataframe))
        self.out_df = self.df_pane.selected_dataframe

    def execute(self):
        if self.in_df is not None:
            self.df_pane.value = self.in_df
        else:
            self.df_pane.value = pd.DataFrame()

    def __panel__(self):
        return pn.Card(self.df_pane)