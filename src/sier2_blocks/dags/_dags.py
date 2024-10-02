from ..blocks._io import LoadDataFrame
from ..blocks._holoviews import HvPoints

from sier2 import Connection
from sier2.panel import PanelDag

DOC = '''# Points chart

Load a dataframe from a file and display a Points chart.
'''

def hv_points_dag():
    """Load a dataframe from a file and display a Points chart."""

    ldf = LoadDataFrame(name='Load DataFrame')
    hp = HvPoints(name='Plot Points')

    dag = PanelDag(doc=DOC, site='Chart', title='Points')
    dag.connect(ldf, hp,
        Connection('out_df', 'in_df'),
        Connection('out_kdims', 'in_kdims'),
        Connection('out_vdims', 'in_vdims'),
        Connection('out_opts', 'in_opts')
    )

    return dag
