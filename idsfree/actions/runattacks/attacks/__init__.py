# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, Tuple

from .web import *
from .network import *

ATTACKS = {
    'net': run_all_net,
    'web': run_all_web
}


def build_attack_command(attack_type: str,
                         network_name: str,
                         ports_to_attack: set,
                         attacked_app: str,
                         service_name: str = "",
                         *,
                         host_base_path_results: str = "/swarm/volumes") -> \
        Dict[str, Tuple[str, str]]:
    """
    This functions build and returns the command for attack and the result
    file path

    :return: tuple as format: (command string, results file path)
    :rtype: tuple(str, str)
    """

    BASE_DOCKER_COMMAND = (
        "sudo docker service create --network={netname} "
        "--name ##SERVICE_NAME## "
        "--restart-condition none "
        "--mount type=bind,source={base_host_path}/,target=/tmp "). \
        format(netname=network_name,
               base_host_path=host_base_path_results)

    commands = {}

    for tool_name, (command, results_file) in ATTACKS[attack_type](
            ports_to_attack,
            attacked_app,
            service_or_app_name=service_name).items():

        commands.update({
            tool_name: (
                "{docker_part} {tool_part}".format(
                    docker_part=BASE_DOCKER_COMMAND,
                    tool_part=command
                ),
                results_file
            )
        })

    return commands


__all__ = ("build_attack_command", )
