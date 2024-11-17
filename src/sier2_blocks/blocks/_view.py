import param
import pandas as pd
import panel as pn
from sier2 import InputBlock, Block

class SimpleTable(InputBlock):
    """ Simple Table Viewer

    Make a tabulator to display an input table.
    Can pass on selections as an output.
    """

    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, continue_label='Push Selection', **kwargs)
        self.tabulator = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    def prepare(self):
        """
        Run before the button is clicked, load the table.
        """
        if self.in_df is not None:
            self.tabulator.value = self.in_df
        else:
            self.tabulator.value = pd.DataFrame()
    
    def execute(self):
        self.out_df = self.tabulator.selected_dataframe

    def __panel__(self):
        return self.tabulator