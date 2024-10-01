from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info(f'{__package__}._blocks.io.LoadDataFrame')
    ]

def dags() -> list[Info]:
    return []
