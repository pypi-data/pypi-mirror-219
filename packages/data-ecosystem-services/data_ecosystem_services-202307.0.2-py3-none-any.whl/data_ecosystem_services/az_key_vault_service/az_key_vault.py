from azure.identity import ClientSecretCredential, DeviceCodeCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, AzureDeveloperCliCredential
from azure.mgmt.resource import ResourceManagementClient
import azure.keyvault.secrets
import os

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class AzKeyVault:
    """Wrapper class for Azure Key Vault to get secrets.

    This class authenticates with the Azure Key Vault using a service 
    principal and provides a method to retrieve secrets.
    """

    # Get the currently running file name
    NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
    # Get the parent folder name of the running file
    SERVICE_NAME = os.path.basename(__file__)

    def __init__(self, tenant_id, client_id, client_secret, key_vault_name, running_interactive):
        """Initializes the KeyVaultSecrets object.

        Args:
            tenant_id (str): The tenant_id of your Azure account. This is the directory ID.
            client_id (str): The client ID of the service principal.
            client_secret (str): The client secret of the service principal.
            key_vault_name (str): The name of your Azure Key Vault. You can get it from the Key Vault properties in the Azure portal.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("__init__"):

            self.vault_url = f"https://{key_vault_name}.vault.azure.net/"
            self.running_interactive = running_interactive
            self.client_id = client_id
            self.client_secret = client_secret
            self.tenant_id = tenant_id
            logger.info(f"vault_url:{self.vault_url}")
            logger.info(f"tenant_id:{self.tenant_id}")
            logger.info(f"client_id:{self.client_id}")
            logger.info(f"running_interactive:{str(self.running_interactive)}")

            # self.credential_default = DefaultAzureCredential()
            # self.credential_dev =  AzureDeveloperCliCredential(  tenant_id=tenant_id,additionally_allowed_tenants=['*'])
            # self.client_default = SecretClient(vault_url,credential= self.credential_default)
            # self.client_dev = SecretClient(vault_url, credential=self.credential_dev)

            # Create a KeyVaultTokenCallback object
            # callback_dev = azure.keyvault.secrets.KeyVaultTokenCallback(self.credential_dev)
            # Set the KeyVaultTokenCallback object on the SecretClient object
            # self.client_dev.authentication_callback = self.callback_dev

    @classmethod
    def cdc_authentication_callback(client, context):
        # Obtain an access token from a custom authentication mechanism

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("cdc_authentication_callback"):

            access_token = cls.get_access_token(context)

            # Return the access token
            return access_token

    def get_credential_device(self):
        """Gets the DeviceCodeCredential for interactive running mode."""

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_credential_device"):

            return DeviceCodeCredential(
                client_id=self.client_id, tenant_id=self.tenant_id, additionally_allowed_tenants=['*'])

    def get_credential(self):
        """Gets the ClientSecretCredential for non-interactive running mode."""

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_credential"):

            return ClientSecretCredential(
                client_id=self.client_id, tenant_id=self.tenant_id, client_secret=self.client_secret)

    def get_secret_client(self, credential):
        """Creates a SecretClient using a given credential."""

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span(f"get_secret_client: {credential}"):
            return SecretClient(vault_url=self.vault_url, credential=credential)

    def retrieve_secret(self, secret_client, secret_name):
        """Attempts to retrieve a secret from the Azure Key Vault using a given SecretClient."""

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span(f"retrieve_secret {secret_name}"):

            try:
                return secret_client.get_secret(secret_name).value
            except Exception as e:
                logger.error(f"Failed to retrieve secret: {e}")
                return None

    def get_secret(self, secret_name):
        """Retrieves a secret from the Azure Key Vault."""

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span(f"get_secret {secret_name}"):
            logger.info(f"vault_url:{self.vault_url}")
            logger.info(f"tenant_id:{self.tenant_id}")
            logger.info(f"client_id:{self.client_id}")
            logger.info(f"running_interactive:{str(self.running_interactive)}")
            logger.info(f"get_secret:{secret_name}")

            if self.running_interactive is True:
                self.credential_device = self.get_credential_device()
                self.client_device = self.get_secret_client(
                    self.credential_device)
                secret_value = self.retrieve_secret(
                    self.client_device, secret_name)

                if secret_value is None:
                    logger.error(
                        "Failed to retrieve secret using DeviceCodeCredential, falling back to ClientSecretCredential.")
                    self.credential = self.get_credential()
                    self.client = self.get_secret_client(self.credential)
                    secret_value = self.retrieve_secret(
                        self.client, secret_name)
            else:
                self.credential = self.get_credential()
                self.client = self.get_secret_client(self.credential)
                secret_value = self.retrieve_secret(self.client, secret_name)

                if secret_value is None:
                    logger.error(
                        "Failed to retrieve secret using ClientSecretCredential, falling back to DeviceCodeCredential.")
                    self.credential_device = self.get_credential_device()
                    self.client_device = self.get_secret_client(
                        self.credential_device)
                    secret_value = self.retrieve_secret(
                        self.client_device, secret_name)

                logger.info(
                    "Retrieve3d secret for key: {secret_name} with length: {len(secret_value)}")

            return secret_value
