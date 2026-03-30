import docker
import datetime


class ContainerKiller:
    """
    Injects a container failure by stopping a named Docker container.
    """
    def __init__(self, container_name: str):
        """
        Args:
            container_name: the exact name of the Docker container to target
        """
        self.client = docker.from_env()
        self.container_name = container_name
        self.killed_at = None


    def inject(self):
        """
        Stops the target container to simulate a failure.
        Records the timestamp of when the container was killed.
        """
        try:
            container = self.client.containers.get(self.container_name) 
            container.stop()
            self.killed_at = datetime.datetime.now()
            print(f"[{self.killed_at}] INJECTED: stopped '{self.container_name}'")
        except docker.errors.NotFound:
            print(f"ERROR: container '{self.container_name}' not found")

    def recover(self):
        """
        Restarts the target container and records the recovery timestamp.
        """
        try:
            container = self.client.containers.get(self.container_name)
            container.start()
            recovered_at = datetime.datetime.now()
            print(f"[{recovered_at}] RECOVERED: started '{self.container_name}'")
        except docker.errors.NotFound:
            print(f"ERROR: container '{self.container_name}' not found")
            