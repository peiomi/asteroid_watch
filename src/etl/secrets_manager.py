import os
from google.cloud import secretmanager
from google.api_core.exceptions import (
    PermissionDenied,
    NotFound,
    ServiceUnavailable,
    InternalServerError,
    DeadlineExceeded,
)
from google.auth.exceptions import DefaultCredentialsError


class SecretsManager:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv("GCP_PROJECT")

    def get_secret(self, secret_name):
        if not self.project_id:
            raise Exception("Project ID not found")

        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        return self._error_handling(name)

    def _error_handling(self, name):
        try:
            response = self.client.access_secret_version(name=name)
        except PermissionDenied as error:
            raise Exception(error)
        except NotFound as error:
            raise Exception(error)
        except ServiceUnavailable as error:
            raise Exception(error)
        except InternalServerError as error:
            raise Exception(error)
        except DeadlineExceeded as error:
            raise Exception(error)
        except DefaultCredentialsError as error:
            raise Exception(error)

        return response.payload.data.decode("utf-8")
