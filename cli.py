import typer
from runner import run_experiment
from report import generate_report

app = typer.Typer()

@app.command()
def run(config: str = typer.Option(..., help="Path to experiment YAML config file")):
    """
    Runs a failure experiment from a YAML config file.
    """
    run_experiment(config)
    
@app.command()
def report(experiment_name: str = typer.Option(..., help="Name of the experiment to report on")):
    """
    Generates a markdown resilience report for a given experiment.
    """
    generate_report(experiment_name)
    
if __name__ == "__main__":
    app()