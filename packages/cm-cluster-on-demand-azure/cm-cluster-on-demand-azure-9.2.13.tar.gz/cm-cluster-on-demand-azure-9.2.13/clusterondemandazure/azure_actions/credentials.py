#
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

import logging
import typing
from functools import lru_cache

import requests.exceptions  # requests is a dependency of azure
import tenacity
from azure.core.exceptions import HttpResponseError
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.marketplaceordering import MarketplaceOrderingAgreements
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.subscription import SubscriptionClient
from msrest.exceptions import AuthenticationError
from msrestazure.azure_exceptions import CloudError

log = logging.getLogger("cluster-on-demand")


class AzureApiHelper:
    def __init__(self, client_id, client_secret, tenant_id, subscription_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.subscription_id = str(subscription_id)

        self._silence_http_logs()

    @staticmethod
    @lru_cache()
    def _silence_http_logs():
        logging.getLogger("msrest").setLevel(logging.WARNING)
        logging.getLogger("azure.mgmt").setLevel(logging.WARNING)
        logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)

    @classmethod
    def from_config(cls, config):
        return cls(
            client_id=config["azure_client_id"],
            client_secret=config["azure_client_secret"],
            tenant_id=config["azure_tenant_id"],
            subscription_id=config["azure_subscription_id"],
        )

    @property
    @lru_cache()
    def storage_client(self):
        return StorageManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def network_client(self):
        return NetworkManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def resource_client(self):
        return ResourceManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def compute_client(self):
        return ComputeManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def subscription_client(self):
        return SubscriptionClient(
            self.get_credential(),
        )

    @property
    @lru_cache()
    def agreements_client(self):
        return MarketplaceOrderingAgreements(
            self.get_credential(),
            self.subscription_id
        )

    @lru_cache()
    @tenacity.retry(
        wait=tenacity.wait_exponential(),
        stop=tenacity.stop_after_delay(60),
        retry=tenacity.retry_if_exception(
            lambda e: (
                isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.SSLError))
                or (
                    isinstance(e, AuthenticationError)
                    and isinstance(e.inner_exception, requests.exceptions.ConnectionError)  # pylint: disable=no-member
                )
            )
        ),
        reraise=True,
        before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
    )
    def get_credential(self):
        return ClientSecretCredential(
            client_id=self.client_id,
            client_secret=self.client_secret,
            tenant_id=self.tenant_id,
        )

    def log_deployment_error(self, azure_ex, resource_group, deployment_name):
        details_found = False
        if "DeploymentFailed" in str(azure_ex) and resource_group and deployment_name:
            try:
                for operation in self.resource_client.deployment_operations.list(
                    resource_group_name=resource_group, deployment_name=deployment_name
                ):
                    if operation.properties.status_code.upper() != "OK":
                        resource_name = operation.properties.target_resource.resource_name
                        error_code = operation.properties.status_message.error.code
                        error_message = operation.properties.status_message.error.message
                        log.error(f"Deployment error for resource {resource_name}: ({error_code}) {error_message}")
                        details_found = True
            except Exception as ex:
                log.error(f"Error while diagnosing deployment failure: {ex}")
        return details_found

    @staticmethod
    def log_error_details(
        azure_ex: typing.Union[CloudError, HttpResponseError],
        *,
        azure_api=None,
        resource_group=None,
        deployment_name=None,
    ):
        if azure_api and azure_api.log_deployment_error(azure_ex, resource_group, deployment_name):
            return  # We've successfully logged interesting details, so no need for extra debug logging

        details = None
        if isinstance(azure_ex, CloudError):
            details = azure_ex.error.details if azure_ex.error else None
        elif isinstance(azure_ex, HttpResponseError):
            details = azure_ex.error.message_details() if azure_ex.error else None
        if details:
            log.debug(f"Error details: {details}")
