import pandas as pd

from warpzone.blobstorage.client import WarpzoneBlobClient
from warpzone.healthchecks import HealthCheckResult, check_health_of
from warpzone.tablestorage.db import base_client
from warpzone.tablestorage.tables.client import WarpzoneTableClient


class WarpzoneDatabaseClient:
    """Class to interact with Azure Table Storage for database queries
    (using Azure Blob Service underneath)
    """

    def __init__(
        self, table_client: WarpzoneTableClient, blob_client: WarpzoneBlobClient
    ):
        self._table_client = table_client
        self._blob_client = blob_client

    @classmethod
    def from_connection_string(cls, conn_str: str):
        table_client = WarpzoneTableClient.from_connection_string(conn_str)
        blob_client = WarpzoneBlobClient.from_connection_string(conn_str)
        return cls(table_client, blob_client)

    def query(self, table_name: str, time_interval: pd.Interval = None):

        query = base_client.generate_query_string(time_interval)

        records = self._table_client.query(table_name, query)

        return base_client.generate_dataframe_from_records(records, self._blob_client)

    def check_health(self) -> HealthCheckResult:
        """
        Pings the connections to the client's associated storage
        ressources in Azure.
        """

        health_check = check_health_of(self._table_client)

        return health_check
