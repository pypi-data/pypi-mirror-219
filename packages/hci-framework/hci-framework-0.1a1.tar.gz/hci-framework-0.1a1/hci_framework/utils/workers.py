import os
import random
import socket
import logging

from string import digits, ascii_letters
import docker
from hci_framework.utils.swarm import SwarmAdmin
from hci_framework.workers import select_worker

admin = SwarmAdmin()
WORKER_NAME = "worker-service-{}"


########################################################################
class AdminWorkers:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

    # ----------------------------------------------------------------------
    def gen_worker_name(self, length=8):
        """"""
        id_ = ''.join([random.choice(ascii_letters + digits)
                      for _ in range(length)])
        if not WORKER_NAME.format(id_) in admin.services:
            return WORKER_NAME.format(id_)
        return self.gen_worker_name(length)

    # ----------------------------------------------------------------------
    def get_open_port(self, ):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    # ----------------------------------------------------------------------
    def remove_all_workers(self):
        """"""
        for worker in admin.services:
            if worker.startswith(WORKER_NAME.format('')):
                admin.stop_service(worker)

    # ----------------------------------------------------------------------
    def create_hci_worker(self, hci_worker, port=None, run='main.py', restart=False):
        """"""
        service_name = 'main-service'
        worker_path = select_worker(hci_worker)

        if restart and (service_name in admin.services):
            admin.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in admin.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        if not os.path.isabs(worker_path):
            worker_path = os.path.abspath(worker_path)

        if port is None:
            port_radiant = self.get_open_port()

        service = admin.client.services.create(
            image="dunderlab/python311:latest",
            name=service_name,
            networks=admin.networks,
            command=["/bin/bash", "-c", f"python /app/worker/{run}"],
            endpoint_spec=docker.types.EndpointSpec(ports={port_radiant: port_radiant}),
            mounts=[
                docker.types.Mount(
                    type="bind",
                    source=worker_path,
                    target="/app/worker",
                    read_only=False
                )
            ],

            env={
                "RADIANT": port_radiant
            }
        )
        return port_radiant

    # ----------------------------------------------------------------------
    def create_worker(self, worker_path, name=None, port=None, run='main.py'):
        """"""
        if not os.path.isabs(worker_path):
            worker_path = os.path.abspath(worker_path)

        if port is None:
            port_stream = self.get_open_port()
            port_radiant = self.get_open_port()

        if name is None:
            name = self.gen_worker_name()

        service = admin.client.services.create(
            image="dunderlab/python311:latest",
            name=name,
            networks=admin.networks,
            command=["/bin/bash", "-c",
                     f"pip install --root-user-action=ignore -r /app/worker/requirements.txt && python /app/worker/{run}"],
            endpoint_spec=docker.types.EndpointSpec(ports={port_radiant: port_radiant,
                                                           port_stream: port_stream, }),
            mounts=[
                docker.types.Mount(
                    type="bind",
                    source=worker_path,
                    target="/app/worker",
                    read_only=False
                )
            ],

            env={
                "STREAM": port_stream,
                "RADIANT": port_radiant
            }

        )

        return port_radiant

