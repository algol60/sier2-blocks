import param
import pandas as pd
import panel as pn
from io import StringIO
from sier2 import InputBlock, Block, Connection
from sier2.panel import PanelDag



class ReadTableDataPanel(InputBlock):
    """ GUI import from csv/excel file.
    
    """

    # Unfortunately, file selection in Panel is dodgy.
    # We need to use a FileInput widget, which uploads the file as a bytes object.
    #
    in_file = param.Bytes(label='Input File', doc='Bytes object of the input file.')
    in_header_row = param.Integer(label='Header row', default=0)
    out_data = param.DataFrame()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.i_if = pn.widgets.FileInput.from_param(
            self.param.in_file,
            accept='.csv,.xlsx,.xls',
            multiple=False
        )
    
    def execute(self):
        pn.state.notifications.info('Reading csv', duration=5_000)
        
        try:
            if self.i_if.filename.endswith('.csv'):
                self.out_data = pd.read_csv(StringIO(self.in_file.decode('utf-8')), header=self.in_header_row)
            elif self.i_if.filename.endswith('.xlsx') or self.i_if.filename.endswith('.xls'):
                self.out_data = pd.read_excel(self.in_file, header=self.in_header_row)
                
        except Exception as e:
            pn.state.notifications.error('Error reading csv. Check logs for more information.', duration=10_000)
            self.logger.error(f'{e}')

    def __panel__(self):
        
        i_hr = pn.widgets.IntInput.from_param(
            self.param.in_header_row,
        )

        return pn.Column(self.i_if, i_hr)

class SimpleTable(Block):
    """ Simple Table Viewer
    """

    in_df = param.DataFrame(doc='A pandas dataframe')
    df_pane = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    def execute(self):
        if self.in_df is not None:
            self.df_pane.value = self.in_df
        else:
            self.df_pane.value = pd.DataFrame()

    def __panel__(self):
        return pn.Card(self.df_pane)


if __name__ == '__main__':
    table_data = ReadTableDataPanel()
    table = SimpleTable()
    
    dag = PanelDag(doc='Example csv reader', title='ReadTableDataPanel')
    dag.connect(csv_data, table, Connection('out_data', 'in_df'))
    dag.show()