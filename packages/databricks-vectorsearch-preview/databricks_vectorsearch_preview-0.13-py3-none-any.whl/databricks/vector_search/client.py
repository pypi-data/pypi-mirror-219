import json
import logging
from typing import List

import requests
from google.protobuf.json_format import MessageToJson

from databricks.vector_search.proto.messages_pb2 import (
    CreateVectorSearchCatalogRequest,
    CreateVectorSearchIndexRequest,
    QueryVectorSearchIndexRequest,
    VectorSearchIndexPipelineSpec,
)

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("databricks.vector_search.client")
log.setLevel(logging.INFO)

import requests
from mlflow.utils import databricks_utils

# Assign the class VectorSearchIndexPipelineSpec.VectorIndex to VectorIndex
VectorIndex = VectorSearchIndexPipelineSpec.VectorIndex


class VectorSearchClient:
    """
    Client for interacting with the Vector Search API for Databricks.

    Example usage:

        client = VectorSearchClient(workspace_url="https://myworkspace.com", token="mytoken")
        response = client.create_catalog("my_catalog")
        print(response)
    """

    def __init__(self, workspace_url=None, token=None):
        """
        Initializes a VectorSearchClient instance.

        :param workspace_url: Workspace URL of Databricks
        :param token: Token for authentication.
        """
        self._workspace_url = workspace_url
        if self._workspace_url is None:
            host_creds = databricks_utils.get_databricks_host_creds()
            self._workspace_url = host_creds.host

        self._token = token
        if self._token is None:
            host_creds = databricks_utils.get_databricks_host_creds()
            self._token = host_creds.token

    def _call_endpoint(self, endpoint, method, params=None, json=None):
        headers = dict()
        headers["Authorization"] = f"Bearer {self._token}"
        cleaned_hostname = (
            self._workspace_url[:-1]
            if self._workspace_url.endswith("/")
            else self._workspace_url
        )
        url = f"{cleaned_hostname}{endpoint}"
        response = requests.request(
            url=url, headers=headers, method=method, params=params, json=json
        )
        log.info(response.text)
        return response.json()

    ### This method will create an vector search catalog in UC
    ### catalog will take 10 to 15 mins to get provisioned.
    ### before that any operation on the cluster will fail except get_cluster
    # catalog_name is the vector search catalog name to be created
    def create_catalog(self, catalog_name):
        """
        Creates a Vector Search catalog.

        :param catalog_name: The name of the vector search catalog to be created.

        :return: The response from the API call.
        """
        catalog_request = CreateVectorSearchCatalogRequest()
        catalog_request.name = catalog_name
        return self._call_endpoint(
            "/api/2.0/vector-search/catalog",
            "POST",
            json=json.loads(
                MessageToJson(catalog_request, preserving_proto_field_name=True)
            ),
        )

    ### This method will delete the vector search catalog in UC
    # catalog_name is the vector search catalog name to be deleted
    def delete_catalog(self, catalog_name):
        """
        Deletes the specified Vector Search catalog.

        :param catalog_name: The name of the vector search catalog to be deleted.

        :return: The response from the API call.
        """
        # TODO: do we need to check if catalog already exists
        return self._call_endpoint(
            f"/api/2.0/vector-search/catalog/{catalog_name}", "DELETE"
        )

    ### This method will get the vector search catalog in UC
    # catalog_name is the vector search catalog name
    def get_catalog(self, catalog_name):
        """
        Retrieves the specified Vector Search catalog.

        :param catalog_name: The name of the catalog to be retrieved.

        :return: The response from the API call.
        """
        return self._call_endpoint(
            f"/api/2.0/vector-search/catalog/{catalog_name}", "GET"
        )

    ### Ingestion time can vary a lot depending on a few important factors, like: embedding model, document length, number of docs, etc
    # source_table_name is the offline Delta table name, must be a UC table and in the format of <catalog>.<schema>.<table>
    # dest_index_name is the index name to be created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    # primary_key the single primary key of the column
    # index_column indicates the column that will do the embedding
    def create_index(
        self,
        source_table_name,
        dest_index_name,
        primary_key,
        index_column,
        embedding_model_endpoint_name,
    ):
        """
        Creates an index

        :param source_table_name: The source delta table where the pre-chunked document texts are located. Must be an Unity Catalog table in the form of <catalog>.<schema>.<table>
        :param dest_index_name: The name of the index to be created under the online catalog. must be in the format of <catalog>.<schema>.<table>
        :param primary_key: Column that represents a non-nullable unqiue identifier of the documents to be stored in the index.
        :param index_column: Column that will be embedded as vectors and persisted in the index
        :param embedding_model_endpoint_name: Embedding model endpoint to use

        :return: The response from the API call.

        Example usage:

        client = VectorSearchClient(workspace_url="https://myworkspace.com", token="mytoken")
        vector_index = VectorIndex()
        vector_index.column = "text"
        vector_index.embedding_model_endpoint_name = "e5-large-v2"
        response = client.create_index(
            source_table_name="my_catalog.schema1.table1",
            dest_index_name="vector.schema1.table1_index",
            primary_key="doc_id",
            index_column="text",
            embedding_model_endpoint_name="e5-large-v2")
        print(response)
        """
        index_request = CreateVectorSearchIndexRequest()

        vector_index_column = VectorIndex()
        vector_index_column.column = index_column
        vector_index_column.embedding_model_endpoint_name = (
            embedding_model_endpoint_name
        )

        index_request.index_pipeline_spec.src_table = source_table_name
        index_request.index_pipeline_spec.dest_index = dest_index_name
        index_request.index_pipeline_spec.primary_key = primary_key
        index_request.index_pipeline_spec.vector_index.MergeFrom(vector_index_column)
        index_request.index_pipeline_spec.continuous.SetInParent()

        json_str = MessageToJson(index_request, preserving_proto_field_name=True)

        log.info(json_str)

        return self._call_endpoint(
            "/api/2.0/vector-search/index", "POST", json=json.loads(json_str)
        )

    ### This method will get the index definition
    # index_name is the index name created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    def get_index(self, index_name):
        """
        Retrieves the specified index.

        :param index_name: The name of the index.

        :return: The response from the API call.
        """
        return self._call_endpoint(f"/api/2.0/vector-search/index/{index_name}", "GET")

    ### This method will perform a vector similarity search on an index
    # index_name is the index name created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    # query_text is the query text
    # filters_json is a json string
    # k is the number of documents to be returned
    def similarity_search(
        self, index_name, query_text, filters_json, columns, num_results
    ):
        """
        Performs a vector similarity search on the specified index.

        :param index_name: The name of the index.
        :param query_text: The query text for the search.
        :param filters_json: The JSON string of filters for the search.
        :param columns: The columns to be returned in the search results.
        :param num_results: The number of documents to be returned.

        :return: The response from the API call.

        Example usage:

        client = VectorSearchClient(workspace_url="https://myworkspace.com", token="mytoken")
        response = client.similarity_search("vector.schema1.table1_index", "What is spark connect?", {"id NOT": ("10", "1")}, ["text", "source"], 3)
        print(response)
        """
        query_request = QueryVectorSearchIndexRequest()
        query_request.query = query_text
        query_request.filters_json = json.dumps(filters_json)
        query_request.columns.extend(columns)
        query_request.num_results = num_results

        json_str = MessageToJson(query_request, preserving_proto_field_name=True)

        log.info(json_str)

        return self._call_endpoint(
            f"/api/2.0/vector-search/index/{index_name}/query",
            "GET",
            json=json.loads(json_str),
        )

    # index_name is the index name created under the online catalog, this must be in the format of <vector search catalog>.<schema>.<table>
    def delete_index(self, index_name):
        """
        Deletes the specified index in the Vector Search cluster.

        :param index_name: The name of the index to be deleted.

        :return: The response from the API call.
        """
        return self._call_endpoint(
            f"/api/2.0/vector-search/index/{index_name}", "DELETE"
        )

    ### This method will list all the existing indexes created under the catalog
    # catalog_name is the vector search catalog name
    def list_indexes(self, catalog_name):
        """
        Lists all existing indexes created under the specified catalog.

        :param catalog_name: The name of the catalog.

        :return: The response from the API call.
        """
        return self._call_endpoint(
            f"/api/2.0/vector-search/index/{catalog_name}", "GET"
        )
