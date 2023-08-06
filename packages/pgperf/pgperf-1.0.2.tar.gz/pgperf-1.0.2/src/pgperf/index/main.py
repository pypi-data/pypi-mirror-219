from pgperf import console, config
from pgperf.db import Db
import typer

app = typer.Typer()

state = {"conf": config['prod'], "path": "index/"}


@app.callback()
def main(verbose: bool = False, debug: bool = False, conf: str = ""):
    """
    Index Informations 
    """
    if conf:
        state['conf'] = config[conf]


@app.command()
def duplicate():
    """
    Show multiple indexes that have the same set of columns, same opclass, expression and predicate.
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'duplicate_indexes')
    console.print(result.to_markdown(), justify="left")


@app.command()
def cache_hit():
    """
    Calculates your cache hit rate for reading indexes
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'index_cache_hit')
    console.print(result.to_markdown(), justify="left")


@app.command()
def scans():
    """
    Number of scans performed on indexes
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'index_scans')
    console.print(result.to_markdown(), justify="left")


@app.command()
def size():
    """
    The size of indexes, descending by size, in MB.
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'index_size')
    console.print(result.to_markdown(), justify="left")


@app.command()
def usage():
    """
    Index hit rate (effective databases are at 99% and up)
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'index_usage')
    console.print(result.to_markdown(), justify="left")


@app.command()
def null():
    """
    Find indexes with a high ratio of NULL values
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'null_indexes')
    console.print(result.to_markdown(), justify="left")


@app.command()
def total_size():
    """
    Total size of all indexes in MB
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'total_index_size')
    console.print(result.to_markdown(), justify="left")


@app.command()
def unused():
    """
    Unused and almost unused indexes. Ordered by their size relative to the number of index scans.
    Exclude indexes of very small tables (less than 5 pages), where the planner will almost invariably select a sequential scan,
    but may not in the future as the table grows
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'unused_indexes')
    console.print(result.to_markdown(), justify="left")


@app.command()
def all():
    """
    List all the indexes with their corresponding tables and columns.
    """
    db = Db(state['conf'])
    result = db.get_from_path(state['path'], 'indexes')
    console.print(result.to_markdown(), justify="left")


if __name__ == "__main__":
    app()
