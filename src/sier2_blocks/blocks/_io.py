#

# Various I/O blocks.
#

import os
import param

import pandas as pd
import panel as pn

from sier2 import InputBlock
from pathlib import Path
from io import StringIO, BytesIO

class LoadDataFrame(InputBlock):
    """ GUI import from csv/excel file.
    
    """

    # Unfortunately, file selection in Panel is dodgy.
    # We need to use a FileInput widget, which uploads the file as a bytes object.
    #
    in_file = param.Bytes(label='Input File', doc='Bytes object of the input file.')
    in_header_row = param.Integer(label='Header row', default=0)
    out_df = param.DataFrame()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.i_if = pn.widgets.FileInput.from_param(
            self.param.in_file,
            accept='.csv,.xlsx,.xls',
            multiple=False
        )
    
    def execute(self):
        pn.state.notifications.info('Reading file', duration=5_000)
        
        try:
            if self.i_if.filename.endswith('.csv'):
                self.out_df = pd.read_csv(StringIO(self.in_file.decode('utf-8')), header=self.in_header_row)
            elif self.i_if.filename.endswith('.xlsx') or self.i_if.filename.endswith('.xls'):
                self.out_df = pd.read_excel(BytesIO(self.in_file), header=self.in_header_row)
                
        except Exception as e:
            pn.state.notifications.error('Error reading csv. Check logs for more information.', duration=10_000)
            self.logger.error(f'{e}')

    def __panel__(self):
        
        i_hr = pn.widgets.IntInput.from_param(
            self.param.in_header_row,
        )

        return pn.Column(self.i_if, i_hr)


class StaticDataFrame(InputBlock):
    """ Static import.
    
    """

    out_df = param.DataFrame()
    
    def execute(self):
        self.out_df = pd.DataFrame(data = {
            "calories": [420, 380, 390],
            "duration": [50, 40, 45]
        })