from sier2 import Block, InputBlock
import param

import panel as pn

import holoviews as hv
hv.extension('bokeh', inline=True)

class HvPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')#'scale_both')
        self.hv_pane.object=self._produce_plot

    x_sel = param.ObjectSelector()
    y_sel = param.ObjectSelector()
    
    @param.depends('in_df', 'x_sel', 'y_sel')
    def _produce_plot(self):
        if self.in_df is not None and self.x_sel is not None and self.y_sel is not None:
            return hv.Points(self.in_df, kdims=[self.x_sel, self.y_sel])

        else:
            return hv.Points([])

    def execute(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        
        self.param['x_sel'].objects = plottable_cols
        self.param['y_sel'].objects = plottable_cols
        self.x_sel = plottable_cols[0]
        self.y_sel = plottable_cols[1]

        self.out_df = self.in_df

    def __panel__(self):
        # return self.hv_pane
        return pn.Column(
            pn.Row(
                self.param['x_sel'],
                self.param['y_sel']
            ),
            self.hv_pane
        )

class HvPointsSelect(InputBlock):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')#'scale_both')
        self.selection = hv.streams.Selection1D()
        self.hv_pane.object=self._produce_plot

    x_sel = param.ObjectSelector()
    y_sel = param.ObjectSelector()
    
    @param.depends('in_df', 'x_sel', 'y_sel')
    def _produce_plot(self):
        if self.in_df is not None and self.x_sel is not None and self.y_sel is not None:
            scatter = hv.Points(self.in_df, kdims=[self.x_sel, self.y_sel])

        else:
            scatter = hv.Points([])

        scatter = scatter.opts(tools=['box_select'])
        self.selection.source = scatter
        return scatter

    def prepare(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        
        self.param['x_sel'].objects = plottable_cols
        self.param['y_sel'].objects = plottable_cols
        self.x_sel = plottable_cols[0]
        self.y_sel = plottable_cols[1]

        print(self.param)

    def execute(self):
        self.out_df = self.in_df.loc[self.selection.index]

    def __panel__(self):
        # return self.hv_pane
        return pn.Column(
            pn.Row(
                self.param['x_sel'],
                self.param['y_sel']
            ),
            self.hv_pane
        )