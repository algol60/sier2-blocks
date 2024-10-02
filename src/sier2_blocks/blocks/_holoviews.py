from sier2 import Block
import param

import panel as pn

import holoviews as hv
hv.extension('bokeh', inline=True)

class HvPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    in_kdims = param.List(item_type=str, bounds=(2,2), doc='Column names of kdims for hv.Points', default=['x', 'y'])
    in_vdims = param.List(item_type=str, doc='Column names of vdims for hv.Points')
    in_opts = param.Dict(doc='Opts for hv.Points')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')

    def execute(self):
        if self.in_df is not None:
            p = hv.Points(self.in_df, kdims=self.in_kdims, vdims=self.in_vdims)
            if self.in_opts is not None:
                p = p.opts(**self.in_opts)
        else:
            p = hv.Points([])

        self.hv_pane.object = p

    def __panel__(self):
        return self.hv_pane