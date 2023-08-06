import pandas as pd

from warpzone.blobstorage.client import WarpzoneBlobClient
from warpzone.tablestorage.db import base_client
from warpzone.tablestorage.tables.client_async import WarpzoneTableClientAsync


class WarpzoneDatabaseClientAsync:
    """Class to interact with Azure Table Storage for database queries
    asyncronously (using Azure Blob Service underneath)
    """

    def __init__(
        self, table_client: WarpzoneTableClientAsync, blob_client: WarpzoneBlobClient
    ):
        self._table_client = table_client
        self._blob_client = blob_client

    @classmethod
    def from_connection_string(cls, conn_str: str):
        table_client = WarpzoneTableClientAsync.from_connection_string(conn_str)
        blob_client = WarpzoneBlobClient.from_connection_string(conn_str)
        return cls(table_client, blob_client)

    async def query(self, table_name: str, time_interval: pd.Interval = None):

        query = base_client.generate_query_string(time_interval)

        records = await self._table_client.query(table_name, query)

        return base_client.generate_dataframe_from_records(records, self._blob_client)
