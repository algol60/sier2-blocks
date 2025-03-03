#

# Various I/O blocks.
#

import os
from pathlib import Path
from io import StringIO, BytesIO

import param
import panel as pn
import pandas as pd

from sier2 import InputBlock, Block


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
            pn.state.notifications.error(f'Error reading {self.i_if.filename}. Check sidebar logs for more information.', duration=10_000)
            # Noting that it might be handy to include a bit more info in the logged message
            self.logger.error(str(e)) # or pass directly to logger 
            #TODO: add feature to logger to send logs to Dag developer
            #TODO: remind Peter of the above

    def __panel__(self):
        i_hr = pn.widgets.IntInput.from_param(
            self.param.in_header_row,
        )
        # Dario prefers the alternative way of declaring specific widgets for variables
        # layout = pn.Param(
        #     self,
        #     parameters=['in_header_row', 'another_param', 'another_one'],
        #     widgets={
        #         'in_header_row': pn.widgets.IntInput
        #     }
        # )
        return pn.Column(self.i_if, i_hr)

# TODO: Faker block to generate testing values
# Consider storing these blocks in a different dir
class StaticDataFrame(InputBlock):
    """ Import static data frame for testing dags.
    
    """

    out_df = param.DataFrame()
    
    def execute(self):
        self.out_df = pd.DataFrame(data = {
            "calories": [420, 380, 390],
            "duration": [50, 40, 45],
            "Latitude": [0, 45, 70],
            "Longitude": [15, 30, 60],
            "Name": ['a', 'b', 'c'],
        })
#class SaveDataFrame(Block):
# Consider adding an option to download a subset or head or sample of data.
class ExportDataFrame(Block):
    """ Save a dataframe to a csv or xlsx.   
    """

    in_df = param.DataFrame()
    in_file_name = param.String()
    # Preferred to use default_filename=None and then set a default value like default_filename = '' if not default_filename else default_filename
    def __init__(self, *args, default_filename='', **kwargs):
        super().__init__(*args, **kwargs)

        self.size_msg = pn.widgets.StaticText(
            value=''
        )#? what is this about
        
        self.i_fn = pn.widgets.TextInput.from_param(
            self.param.in_file_name,
            placeholder='Output file name',
            value=default_filename,
            name='Output file name (without extension)'
        )
        
        self.csvdl = pn.widgets.FileDownload(
            callback=self.download_csv,
            button_type='success', 
            filename='',
            label='Download .csv'
        )
        
        self.xlsxdl = pn.widgets.FileDownload(
            callback=self.download_xlsx,
            button_type='success', 
            filename='',
            label='Download .xlsx'
        )
        
        self.csvdl.disabled = True
        self.xlsxdl.disabled = True

        # Hook up the filename widget to the download widget.
        # Make sure to watch value_input, which is updated live as the user edits the TextInput.
        # 'value' is only updated if the user hits enter.
        #
        def update_name(event):
            if self.i_fn.value_input:
                self.xlsxdl.disabled = False
                self.xlsxdl.filename = f'{self.i_fn.value_input}.xlsx'
                self.csvdl.disabled = False
                self.csvdl.filename = f'{self.i_fn.value_input}.csv'
            else:
                self.xlsxdl.disabled = True
                self.csvdl.disabled = True
        
        self.i_fn.param.watch(update_name, 'value_input')

    def download_csv(self):
        buf = StringIO()
        self.in_df.to_csv(buf)
        buf.seek(0)
        return buf

    def download_xlsx(self):
        buf = BytesIO()
        writer = pd.ExcelWriter(buf, engine='xlsxwriter')
        self.in_df.to_excel(writer)
        writer.close()
        buf.seek(0)
        return buf

    def execute(self):
        # Maybe this should be a pn global alert and also only trigger for files of unusually large size?
        self.size_msg.value = f'Saving data frame of size {self.in_df.shape}. Large files may cause issues.'

        # Only allow file download if we've set an input.
        #
        if self.i_fn.value_input:
            self.csvdl.disabled = False
            self.xlsxdl.disabled = False
        
    def __panel__(self):    
        return pn.Column(
            self.size_msg,
            self.i_fn,
            pn.Row(self.csvdl, self.xlsxdl),
        )

    