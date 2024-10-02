#

# Various I/O blocks.
#

from sier2 import Block
import os
import pandas as pd
from pathlib import Path
import param

import panel as pn

class LoadDataFrame(Block):
    """Load a pandas DataFrame from a csv file or Excel spreadsheet."""

    out_df = param.DataFrame(doc='A pandas dataframe')
    out_kdims = param.List(['x', 'y'], item_type=str, bounds=(2,2), doc='Column names of kdims for hv.Points')
    out_vdims = param.List(item_type=str, doc='Column names of vdims for hv.Points')
    out_opts = param.Dict(doc='Opts for hv.Points')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, user_input=True, **kwargs)

    def __panel__(self):
        self.fs = None
        fs_row = pn.Row()
        txt = pn.widgets.StaticText(name='Information', align='end')

        def on_load(_event):
            fnams = self.fs.value
            print(f'loading {fnams}')
            if len(fnams)!=1:
                txt.value = 'Specify one file'
            else:
                p = Path(fnams[0])
                suffix = p.suffix.lower()
                if suffix=='.csv':
                    self.out_df = pd.read_csv(p)
                    txt.value = f'Loaded CSV file  {p}'
                elif suffix=='.xlsx':
                    self.out_df = pd.read_excel(p)
                    txt.value = f'Loaded Excel spreadsheet {p}'
                else:
                    txt.value = 'Unrecognised file type'
                    return

            self.out_kdims = ['x', 'y']
            self.out_vdims = ['name']
            self.out_opts = {
                'color': 'name',
                'cmap': 'glasbey_light',
                'size': 4,
                'show_legend': False,
                'tools': ['hover']
            }

        def on_drive(_event):
            print(_event, type(_event))
            self.fs = pn.widgets.FileSelector(
                name='Select a data file',
                only_files=True,
                directory=_event
            )
            fs_row[:] = [self.fs]

        drives = [str(Path.home())] + [d for d in os.listdrives() if d!='C:\\']
        on_drive(drives[0])
        drive_select = pn.widgets.Select(name='Drive', options=drives)
        pn.bind(on_drive, drive_select.param.value, watch=True)

        b = pn.widgets.Button(
            name='Load',
            button_type='primary',
            align='end'
        )
        b.on_click(on_load)

        return pn.Column(
            pn.Row(drive_select, txt),
            fs_row,
            pn.Row(pn.HSpacer(), b)
        )

if __name__=='__main__':
    pn.Column(LoadDataFrame()).show()
