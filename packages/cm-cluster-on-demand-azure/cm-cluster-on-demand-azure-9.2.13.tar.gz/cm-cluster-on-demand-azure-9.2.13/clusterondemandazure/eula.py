# Copyright 2004-2023 Bright Computing Holding BV
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

from __future__ import absolute_import

import logging
import sys

from clusterondemand.bcm_version import BcmVersion
from clusterondemandazure.azure_actions.terms import MarketplaceTerms
from clusterondemandconfig.command_context import Command
from clusterondemandconfig.configuration import CommandConfiguration

log = logging.getLogger("cluster-on-demand")


def check_azure_eula(command: Command, config: CommandConfiguration):
    if command.group.name != "cluster" or command.name != "create":
        log.debug(f"Skipping Azure terms check because command is {command.group.name} {command.name}")
        return  # no need to check acceptance unless images will be used
    elif config["version"] == "trunk":
        log.debug(f"Skipping Azure terms check because version is {config['version']}")
        return  # since it's trunk, we are the users here, so no need to accept terms
    elif BcmVersion(config["version"]) < BcmVersion("9.0"):
        log.debug(f"Skipping Azure terms check because version is {config['version']}")
        return  # no Azure images before 9.0

    azure_terms = MarketplaceTerms(config)

    if azure_terms.accepted:
        print("Terms for Azure VM images have already been accepted. Proceeding to the next step...")
    elif config["accept_azure_terms"]:
        log.debug("User accepted the Azure marketplace terms through the configuration.")
        azure_terms.accept()
        print("Terms accepted. Proceeding to the next step...")
    else:
        print("To use Azure VM images, you need to accept the following terms:")
        for (name, link) in azure_terms.terms.items():
            print(f"- {name}: {link}")

        if input("Accept (y/n)? ").lower().startswith("y"):
            azure_terms.accept()
            print("Terms accepted. Proceeding to the next step...")
        else:
            print("Terms not accepted. Exiting...")
            sys.exit(1)
