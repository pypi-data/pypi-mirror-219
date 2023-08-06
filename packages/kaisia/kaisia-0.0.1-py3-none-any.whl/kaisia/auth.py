from google.oauth2 import service_account
import os


class SA:
    @classmethod
    def credentials(self, path: str = "") -> service_account.Credentials:
        try:
            return service_account.Credentials.from_service_account_file(path)
        except (FileNotFoundError, TypeError):
            return service_account.Credentials.from_service_account_file(
                os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            )
