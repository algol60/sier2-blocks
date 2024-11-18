from sier2 import Block
import param

import panel as pn

import holoviews as hv
hv.extension('bokeh', inline=True)

class HvPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hv_pane = pn.Row(pn.pane.HoloViews(sizing_mode='stretch_width'), sizing_mode='stretch_width')

    def make_plot(self, x_dim, y_dim):
        return hv.Points(self.in_df, kdims=[x_dim, y_dim])

    def execute(self):
        if self.in_df is not None:
            # Work out which columns can be plotted:
            # The meaning of iuf: i int (signed), u unsigned int, f float
            #
            plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
                        
            dmap = hv.DynamicMap(
                self.make_plot, 
                kdims=['X_dim', 'Y_dim'],
            ).redim.values(
                X_dim=list(plottable_cols), 
                Y_dim=list(plottable_cols),
            )

            # self.hv_pane[0] = pn.pane.HoloViews(
            #     dmap
            # )

            # Add index as an option?
            #
            self.hv_pane[0] = pn.pane.HoloViews(
                dmap, 
                widgets={
                    'X_dim': pn.widgets.Select(name='X_dim', options=list(plottable_cols), value=plottable_cols[0]),
                    'Y_dim': pn.widgets.Select(name='Y_dim', options=list(plottable_cols), value=plottable_cols[1]),
                },
                sizing_mode='stretch_width',
            ).layout
            
            # p = hv.Points(self.in_df, kdims=self.in_kdims, vdims=self.in_vdims)
            # if self.in_opts is not None:
            #     p = p.opts(**self.in_opts)
        

    def __panel__(self):
        return self.hv_pane


# def load_symbol(symbol, variable, **kwargs):
#     df = pd.DataFrame(getattr(stocks, symbol))
#     df['date'] = df.date.astype('datetime64[ns]')
#     return hv.Curve(df, ('date', 'Date'), variable).opts(framewise=True)

# stock_symbols = ['AAPL', 'IBM', 'FB', 'GOOG', 'MSFT']
# variables = ['open', 'high', 'low', 'close', 'volume', 'adj_close']
# dmap = hv.DynamicMap(load_symbol, kdims=['Symbol','Variable'])
# dmap = dmap.redim.values(Symbol=stock_symbols, Variable=variables)