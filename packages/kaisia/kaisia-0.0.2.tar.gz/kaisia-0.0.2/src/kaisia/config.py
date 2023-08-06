from .exceptions import MissingConfig, IncorrectID


class Config:
    BQ_CLIENT_SCOPE = ("https://www.googleapis.com/auth/bigquery",)
    _DOT_DELIMITER = "."
    _DATASET_EXCEPTION_CHARS = ["-" "&", "@", "%"]

    def __init__(self, id: str = ""):
        self._gbq_project: str = ""
        self._gbq_dataset: str = ""
        self._gbq_table: str = ""
        self._parse_and_validate_id(id=id)

    @property
    def project(self):
        if not self._gbq_project:
            raise MissingConfig("project")
        return self._gbq_project

    @property
    def dataset(self):
        if not self._gbq_dataset:
            raise MissingConfig("dataset")
        return self._gbq_dataset

    @property
    def table(self):
        if not self._gbq_table:
            raise MissingConfig("table")
        return self._gbq_table

    def _parse_and_validate_id(self, id: str):
        try:
            project, dataset, table = id.split(self._DOT_DELIMITER)
        except ValueError:
            raise IncorrectID(id, "incorrect id delimiter")

        if len(project) > 31:
            raise IncorrectID(project, "incorrect project name lenght")

        if len(dataset) > 1024:
            raise IncorrectID(project, "incorrect dataset name lenght")

        if any(ch in dataset for ch in self._DATASET_EXCEPTION_CHARS):
            raise IncorrectID(project, "invalid dataset name")

        if len(table) > 1024:
            raise IncorrectID(project, "incorrect table name lenght")

        self._gbq_project: str = project
        self._gbq_dataset: str = dataset
        self._gbq_table: str = table
