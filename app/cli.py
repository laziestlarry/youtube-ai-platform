import click
from app.full_pipeline import run_pipeline

@click.group()
def cli():
    pass

@cli.command()
@click.option('--advanced', is_flag=True, help='Use motion footage and advanced editing.')
def autoproduce(advanced):
    """Run the full YouTube video automation pipeline."""
    run_pipeline(advanced=advanced)

if __name__ == "__main__":
    cli() 