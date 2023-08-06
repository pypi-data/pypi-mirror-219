import docker
import logging


########################################################################
class SwarmAdmin:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, base_url='unix://var/run/docker.sock'):
        """Constructor"""
        self.client = docker.DockerClient(base_url=base_url)
        self.create_networks()

    # ----------------------------------------------------------------------
    def create_networks(self):
        """"""
        self.networks = ['hci_network']
        for network in self.networks:
            if network not in [n.name for n in self.client.networks.list()]:
                self.client.networks.create(network, driver="overlay")
                logging.warning(f"Created network '{network}'")

    # ----------------------------------------------------------------------
    @property
    def services(self):
        """"""
        return [service.name for service in self.client.services.list()]

    # ----------------------------------------------------------------------
    def stop_service(self, service_name):
        """"""
        service = self.client.services.get(service_name)
        service.remove()

    # ----------------------------------------------------------------------
    def stop_all_services(self):
        """"""
        for service in self.services:
            self.stop_service(service)

    # ----------------------------------------------------------------------
    def create_mainservice(self, service_name="main-service", port=4444):
        """"""
        if service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        service = self.client.services.create(
            image="dunderlab/python311:latest",
            name=service_name,
            networks=self.networks,
            command=["hci_framework"],
            endpoint_spec=docker.types.EndpointSpec(ports={4444: port}),
            mounts=[
                docker.types.Mount(
                    type='bind',
                    source='/var/run/docker.sock',
                    target='/var/run/docker.sock'
                ),
            ]
        )
        return service_name in self.services

    # ----------------------------------------------------------------------
    def create_jupyter(self, service_name="jupyterlab-service", port=8888, restart=False):
        """"""
        if restart:
            self.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        service = self.client.services.create(
            image="dunderlab/python311:latest",
            name=service_name,
            networks=self.networks,
            command=["jupyter", "lab",
                     "--ip=0.0.0.0", "--port=8888",
                     "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"],
            endpoint_spec=docker.types.EndpointSpec(ports={8888: port}),
            mounts=[
                docker.types.Mount(
                    type='bind',
                    source='/var/run/docker.sock',
                    target='/var/run/docker.sock'
                ),
            ]
        )
        return service_name in self.services

    # ----------------------------------------------------------------------
    def create_kafka(self, kafka_service_name="kafka-service", zookeeper_service_name="zookeeper-service", kafka_port=9092, zookeeper_port=2181):
        """"""
        if not kafka_service_name in self.services:
            kafka_service = self.client.services.create(
                image="dunderlab/kafka:latest",
                name=kafka_service_name,
                networks=self.networks,
                endpoint_spec=docker.types.EndpointSpec(
                    ports={9092: kafka_port})
            )
        else:
            logging.warning(f"Service '{kafka_service_name}' already exist")

        if not zookeeper_service_name in self.services:
            zookeeper_service = self.client.services.create(
                image="dunderlab/zookeeper:latest",
                name=zookeeper_service_name,
                networks=self.networks,
                endpoint_spec=docker.types.EndpointSpec(
                    ports={2181: zookeeper_port})
            )
        else:
            logging.warning(
                f"Service '{zookeeper_service_name}' already exist")

        return kafka_service_name in self.services, zookeeper_service_name in self.services

    # ----------------------------------------------------------------------
    def create_timescaledb(self, service_name="timescaledb-service", port=5432):
        """"""
        if service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        timescaledb_service = self.client.services.create(
            image="timescale/timescaledb:latest-pg15",
            name=service_name,
            networks=self.networks,
            env=[
                "POSTGRES_PASSWORD=password",
                # "POSTGRES_USER=myuser",
                "POSTGRES_DB=timescaledb",
                "POSTGRES_MAX_CONNECTIONS=500"
            ],
            endpoint_spec=docker.types.EndpointSpec(ports={5432: port})
        )
        return service_name in self.services

