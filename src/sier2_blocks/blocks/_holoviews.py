from sier2 import Block, InputBlock
import param

import panel as pn
import numpy as np

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

class HvHist(Block):
    """Produce a Histogram of input data."""

    # Define params
    #
    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    column = param.ObjectSelector()
    bins = param.Integer(100, bounds=(0, None))
    integer_bins = param.Boolean(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')#'scale_both')

        # Make a widget to control the 
        self.bins_widget = pn.widgets.IntInput(name='Bins', start=0, value=self.bins)
        self.bins_widget.param.watch(lambda event: setattr(self, 'bins', event.new), 'value')
        
        self.hv_pane.object=self._produce_plot
        
    
    @param.depends('in_df', 'column', 'bins', 'integer_bins')
    def _produce_plot(self):        
        if self.integer_bins:
            self.bins_widget.disabled = True
        else:
            self.bins_widget.disabled = False
          
        if self.in_df is not None and self.column is not None :

            if self.integer_bins:
                col = self.in_df[self.column]
                self.bins = col.max() - col.min() + 1
                self.bins_widget.value = self.bins
                
                frequencies, edges = np.histogram(
                    col, 
                    np.arange(col.min()-0.5, col.max()+1.5, 1),
                )
            else:
                frequencies, edges = np.histogram(self.in_df[self.column], self.bins)

        else:
            frequencies, edges = [], []

        return hv.Histogram((edges, frequencies))

    # @param.depends('integer_bins')
    # def _switch_bin_type(self):
    #     print('Here')
        

    def execute(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        
        self.param['column'].objects = plottable_cols
        self.column = plottable_cols[0]

        self.out_df = self.in_df

    def __panel__(self):
        # return self.hv_pane
        return pn.Column(
            pn.Row(
                self.param['column'],
                self.bins_widget,
                self.param['integer_bins'],
            ),
            self.hv_pane
        )