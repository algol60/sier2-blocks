from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks.blocks:LoadDataFrame', 'Load a dataframe from a file'),
        Info('sier2_blocks.blocks:SimpleTable', 'Display a simple table'),
        Info('sier2_blocks.blocks:HvPoints', 'A Holoviews Points chart')
    ]

def dags() -> list[Info]:
    return [
        Info('sier2_blocks.dags:hv_points_dag', 'Load and plot a dataframe as points'),
        Info('sier2_blocks.dags:table_view_dag', 'Load a dataframe from file and display in a panel table'),
    ]
