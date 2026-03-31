from config import load_config
from injectors import ContainerKiller
from health import poll_health
from storage import init_db, save_results

def run_experiment(config_path: str):
    """
    Coordinates a full experiment lifecycle.
    Loads config, injects failure, polls health, saves results, and recovers.
    
    Args:
        config_path: path to the YAML experiment config file
    """
    
    config = load_config(config_path)
    init_db()
    print(f"Starting experiment: {config.name}")
    
    killer = ContainerKiller(config.target)
    killer.inject()
    
    results = poll_health(config.health_check, config.duration_seconds)
    save_results(config.name, results)
    
    killer.recover()
    print(f"Experiment '{config.name}' complete. Results saved to results.db")