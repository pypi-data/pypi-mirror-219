from google.cloud import bigquery
from typing import List
from google.oauth2 import service_account

from .config import Config
from .exceptions import TooManyTables
from .cli import Colors
from .auth import SA


class Base:
    def __init__(self, id: str, credential_path: str = ""):
        self.config: Config = Config(id=id)
        self.credentials: service_account.Credentials = SA.credentials(
            path=credential_path
        )
        self.bq_client: bigquery.Client = self._client()

    def _client(self) -> bigquery.Client:
        return bigquery.Client(
            project=self.config.project,
            credentials=self.credentials,
            client_options={"scopes": self.config.BQ_CLIENT_SCOPE},
        )


class Table(Base):
    def __init__(self, id: str, credential_path: str = ""):
        super().__init__(id, credential_path)

    @property
    def schema(self):
        table_ref = self.bq_client.dataset(self.config.dataset).table(self.config.table)
        table = self.bq_client.get_table(table_ref)
        return table.schema


class SchemaCompareMixin:
    def difference(self):
        table1 = set(self.resources[0].schema)
        table2 = set(self.resources[1].schema)
        self.diff = table1.symmetric_difference(table2)


class SchemaReprMixin:
    def to_terminal(self):
        repr = [field.to_api_repr() for field in self.diff]
        for i in repr:
            print(
                f"{Colors.OKGREEN}{i['name']}{Colors.ENDC} {Colors.BOLD}- {Colors.ENDC}{Colors.OKCYAN}{i['mode']} {Colors.OKGREEN}{i['type']}{Colors.ENDC}"
            )


class Delta(SchemaReprMixin, SchemaCompareMixin):
    def __init__(self, resources: List[Table]):
        self._resources = self._validate_resources(resources)
        self.difference()

    @property
    def resources(self):
        return self._resources

    def _validate_resources(self, resources: List):
        if len(resources) != 2:
            raise TooManyTables(len(resources))
        return resources


class MakeMigration(Base):
    def __init__(self, config: Config):
        super().__init__(config)
