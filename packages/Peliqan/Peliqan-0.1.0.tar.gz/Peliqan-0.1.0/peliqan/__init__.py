__version__ = "0.1.0"
__author__ = 'Peliqan.io'
__credits__ = 'Peliqan.io'

# import necessary modules
import logging

import pandas
import pandas as pd
import requests
import os

__all__ = [
    "BasePeliqanClient", "Peliqan"
]

PELIQAN_URL = os.environ.get("PELIQAN_URL", "https://app.eu.peliqan.io")
"""
The Peliqan environment's url that the client will connect to.
"""

# get logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

# get log handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

# set log format
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s %(message)s")

# set format to log handler
sh.setFormatter(formatter)

# add handler to logger
logger.addHandler(sh)


class PeliqanClientException(Exception):
    pass


class BaseClient:

    def __init__(self, jwt, backend_url):
        self.JWT = jwt
        self.BACKEND_URL = backend_url

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "JWT %s" % self.JWT
        }

    def call_backend(self, method, url, expected_status_code=200, **kwargs):
        if not kwargs.get('headers'):
            headers = self.get_headers()
            kwargs.update(headers=headers)

        response = requests.request(method, url, **kwargs)
        try:
            response_dict = response.json()
        except ValueError:
            response_dict = {}

        # handle error responses
        if response.status_code != expected_status_code:
            error_message = f"Server responded with status code {response.status_code}"
            if response_dict:
                error_message += f" and error details \n{response_dict}"
            raise PeliqanClientException(error_message)

        return response_dict


class WritebackClient(BaseClient):
    def __init__(self, connection, jwt, backend_url):
        super(WritebackClient, self).__init__(jwt, backend_url)
        self.connection = connection

    def request_endpoint_via_proxy(self, object_name, action, **kwargs):
        # send to proxy: self.connection, objectName, action, kwargs
        payload = {
            "connection": self.connection,
            "objectName": object_name,
            "action": action,
            "kwargs": kwargs
        }

        url = f"{self.BACKEND_URL}/api/proxy/"
        return self.call_backend('post', url, json=payload)

    def get(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'get', **kwargs)
        if "detail" in response_dict:
            return response_dict["detail"]
        else:
            return response_dict

    def findone(self, object_name, **kwargs):
        if "searchfield" not in kwargs or "searchterm" not in kwargs:
            raise PeliqanClientException(f"Parameters searchfield and searchfield are required for function 'findone'.")
        response_dict = self.request_endpoint_via_proxy(object_name, 'findone', **kwargs)
        if "detail" in response_dict:
            return response_dict["detail"]
        else:
            return response_dict

    def list(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'list', **kwargs)
        return response_dict

    def add(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'add', **kwargs)
        return response_dict

    def update(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'update', **kwargs)
        return response_dict

    def upsert(self, object_name, **kwargs):
        response_dict_findone = self.request_endpoint_via_proxy(object_name, 'findone',
                                                                searchfield=kwargs["searchfield"],
                                                                searchterm=kwargs["searchterm"])
        kwargs.pop('searchfield', None)
        kwargs.pop('searchterm', None)
        if "detail" in response_dict_findone and "id" in response_dict_findone["detail"]:
            kwargs["id"] = response_dict_findone["detail"]["id"]
            response_dict = self.request_endpoint_via_proxy(object_name, 'update', **kwargs)
        else:
            response_dict = self.request_endpoint_via_proxy(object_name, 'add', **kwargs)
        return response_dict

    def delete(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'delete', **kwargs)
        return response_dict

    def copy(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'copy', **kwargs)
        return response_dict

    def rename(self, object_name, **kwargs):
        response_dict = self.request_endpoint_via_proxy(object_name, 'rename', **kwargs)
        return response_dict


class BackendServiceClient(BaseClient):
    def __init__(self, jwt, backend_url):
        super(BackendServiceClient, self).__init__(jwt, backend_url)
        self._cache = {
            'connection': {},
            'database': {},
            'table': {}
        }

    def get_cached_results(self, resource_type, resource_id_or_name, property_name):
        try:
            resource_id_or_name = resource_id_or_name.lower()
        except AttributeError:
            pass

        resource_type = resource_type.lower()
        property_name = property_name.lower()
        return self._cache.get(resource_type, {}).get(resource_id_or_name, {}).get(property_name)

    def _cache_connection_data(self, data):
        connection_name = data.get('connection_name', '')
        if connection_name:
            connection_name = connection_name.lower()
            connection_id = data['connection_id']
            if connection_id:
                data_to_cache = {
                    connection_id: {
                        'connection_name': connection_name
                    },
                    connection_name: {
                        'connection_id': connection_id
                    }
                }
                self._cache['connection'].update(data_to_cache)

    def _cache_database_data(self, data):
        database_name = data.get('database_name', '')
        if database_name:
            database_name = database_name.lower()
            database_id = data['database_id']
            if database_id:
                data_to_cache = {
                    database_id: {
                        'database_name': database_name
                    },
                    database_name: {
                        'database_id': database_id
                    }
                }
                self._cache['database'].update(data_to_cache)

    def _cache_table_and_field_data(self, data):
        table_name = data.get('table_name', '')
        if table_name:
            table_name = table_name.lower()
            table_id = data['table_id']
            if table_id:
                data_to_cache = {
                    table_name: {
                        'table_id': table_id,
                    },
                    table_id: {
                        'table_name': table_name
                    }
                }
                self._cache['table'].update(data_to_cache)

                # cache field
                field_name = data.get('field_name', '')
                if field_name:
                    field_name = field_name.lower()
                    field_physical_name = data['field_physical_name']
                    if field_physical_name:
                        data_to_cache[table_name].update({field_name: field_physical_name})
                        data_to_cache[table_id].update({field_name: field_physical_name})

    def _update_cache(self, data):
        self._cache_connection_data(data)
        self._cache_database_data(data)
        self._cache_table_and_field_data(data)

    def find_connection(self, connection_id=None, connection_name=None):
        """

        :param connection_id:
        :param connection_name:
        :return:
        """
        url = f"{self.BACKEND_URL}/api/database/resource/lookup/connection/"
        data = {
            'connection_id': connection_id,
            'connection_name': connection_name,
        }
        data = self.call_backend("get", url, json=data)

        self._update_cache(data)
        return data

    def find_database(self, connection_id=None, connection_name=None, database_id=None, database_name=None):
        """

        :param connection_id:
        :param connection_name:
        :param database_id:
        :param database_name:
        :return:
        """
        url = f"{self.BACKEND_URL}/api/database/resource/lookup/database/"
        data = {
            'connection_id': connection_id,
            'connection_name': connection_name,
            'database_id': database_id,
            'database_name': database_name,
        }
        data = self.call_backend("get", url, json=data)

        self._update_cache(data)
        return data

    def find_table_or_field(self, connection_id=None, connection_name=None, database_id=None, database_name=None,
                            table_id=None, table_name=None, field_id=None, field_name=None):
        """
        Find the table information by passing in a table_id or table_name.
        Optionally pass in a field_id or field_name to retrieve that fields info.

        We can also pass in the optional connection_id/connection_name and optional database_id/database_name
        if we want to restrict the search.

        :param connection_id: (Optional) id of the connection the table belongs to.
        :param connection_name: (Optional) name of the connection the table belongs to.
        :param database_id: (Optional) name of the database the table belongs to.
        :param database_name: (Optional) name of the database the table belongs to.
        :param table_id: id of the table to find.
        :param table_name: name of the table to find.
        :param field_id: (Optional) id of the field to find.
        :param field_name: (Optional) name of the field to find.
        :return:
        """
        url = f"{self.BACKEND_URL}/api/database/resource/lookup/table/"
        data = {
            'connection_id': connection_id,
            'connection_name': connection_name,
            'database_id': database_id,
            'database_name': database_name,
            'table_id': table_id,
            'table_name': table_name,
            'field_id': field_id,
            'field_name': field_name
        }
        data = self.call_backend("get", url, json=data)

        self._update_cache(data)
        return data

    def find_resource(self, resource_type, resource_id=None, resource_name=None, **kwargs):

        if resource_type not in ['connection', 'database', 'table']:
            raise PeliqanClientException(f"{resource_type} is not valid. "
                                         f"Allowed resource types are 'connection', 'database', 'table'.")

        if not resource_id and not resource_name:
            raise PeliqanClientException("resource_id or resource_name must be provided as kwargs.")

        if resource_type.lower() == 'connection':
            data = {
                'connection_id': resource_id,
                'connection_name': resource_name
            }
            # find connection
            return self.find_connection(**data)
        elif resource_type.lower() == 'database':
            data = {
                'database_id': resource_id,
                'database_name': resource_name,
            }
            # find database
            return self.find_database(**data, **kwargs)
        elif resource_type.lower() == 'table':
            data = {
                'table_id': resource_id,
                'table_name': resource_name
            }
            return self.find_table_or_field(**data, **kwargs)
        else:
            raise PeliqanClientException(f"{resource_type} is not valid. "
                                         f"Allowed resource types are 'connection', 'database', 'table'.")

    def refresh_resource(self, resource_type, refresh_baseurl, resource_name=None, resource_id=None, **kwargs):

        if resource_type not in ['connection', 'database', 'table']:
            raise PeliqanClientException(f"{resource_type} is not valid. "
                                         f"Allowed resource types are 'connection', 'database', 'table'.")

        if not resource_id and not resource_name:
            raise PeliqanClientException(f"{resource_type}_id or {resource_type}_name must be provided as kwargs.")

        elif not resource_id and resource_name:
            resource_id = self.get_cached_results(resource_type, resource_name, f'{resource_type}_id')

        if not resource_id:
            lookup_data = self.find_resource(resource_type=resource_type, resource_name=resource_name, **kwargs)
            resource_id = lookup_data[f'{resource_type}_id']

        url = refresh_baseurl % resource_id
        # call sync url
        return self.call_backend("get", url, expected_status_code=204)

    def get_records(self, url_suffix):
        # Fetch Trino catalog and SQL query with all CDC changes applied
        url = f"{self.BACKEND_URL}/api/database/resource/trino/records/" + url_suffix
        response_dict = self.call_backend("get", url)
        return response_dict

    def push_cdclog(self, url, data):
        return self.call_backend("patch", url, json=data)

    def get_cdclogs(self, table_id, writeback_status, change_type, latest_changes_first=False):
        url = f"{self.BACKEND_URL}/api/database/cdclogs/table/{table_id}/?latest_changes_first={latest_changes_first}"

        if writeback_status or change_type:
            url += "&"
            if writeback_status:
                url += f"writeback_status={writeback_status}&"

            if change_type:
                url += f"change_type={change_type}"

        response_dict = self.call_backend("get", url)
        return response_dict

    def update_writeback_status(self, table_id, change_id, writeback_status):
        url = f"{self.BACKEND_URL}/api/database/cdclogs/table/{table_id}/changes/{change_id}/writeback_status/"

        data = {
            "change_id": change_id,
            "writeback_status": writeback_status
        }

        response_dict = self.call_backend("patch", url, json=data)
        return response_dict

    def get_databases(self):
        url = f"{self.BACKEND_URL}/api/applications"
        response_dict = self.call_backend("get", url)
        return response_dict

    def update_table(self, id, name=None, table_type=None, query=None, external=None, pk_field=None, settings=None):
        url = f"{self.BACKEND_URL}/api/database/tables/%s/" % id
        data = {}
        if name:
            data["name"] = name
        if table_type:
            data["table_type"] = table_type
        if query:
            data["query"] = query
        if external:
            data["external"] = external
        if pk_field:
            data["pk_field"] = pk_field
        if settings:
            data["settings"] = settings
        response_dict = self.call_backend("patch", url, json=data)
        return response_dict

    def update_database_metadata(self, id, description=None, tags=None):
        url = f"{self.BACKEND_URL}/api/applications/%s/data-catalog/" % id
        data = {}
        if description:
            data["description"] = description
        if tags:
            data["tags"] = tags
        response_dict = self.call_backend("patch", url, json=data)
        return response_dict

    def update_table_metadata(self, id, description=None, tags=None):
        url = f"{self.BACKEND_URL}/api/database/tables/%s/data-catalog/" % id
        data = {}
        if description:
            data["description"] = description
        if tags:
            data["tags"] = tags
        response_dict = self.call_backend("patch", url, json=data)
        return response_dict

    def update_field_metadata(self, id, description=None, tags=None):
        url = f"{self.BACKEND_URL}/api/database/fields/%s/data-catalog/" % id
        data = {}
        if description:
            data["description"] = description
        if tags:
            data["tags"] = tags
        response_dict = self.call_backend("patch", url, json=data)
        return response_dict


class BasePeliqanClient:
    """
    This base class wraps all operations we want to expose to our internal and external clients.
    """

    def __init__(self, jwt, backend_url):
        self.JWT = jwt
        self.BACKEND_URL = backend_url
        self.__service_client__ = BackendServiceClient(jwt, backend_url)

    def find_resource(self, resource_type, resource_id=None, resource_name=None, **kwargs):
        """

           :param resource_type: can be connection/database/table.
           :param resource_id: id of the resource.
           :param resource_name: name of the resource.
           :param kwargs: additional kwargs can also be passed.
           :return: resource details as a dict.
        """
        return self.__service_client__.find_resource(resource_type, resource_id, resource_name, **kwargs)

    # todo allow user to set a PK column for the query (or update the guessed PK)
    # todo accept database id and table id as inputs too
    def load_table(self, table_name='', query='', table_id=None, fillna_with=''):
        """
        Return the records in a table.

        :param table_name: The name of a table.
        :param query: A valid Trino sql query.
        :param table_id: An integer value that uniquely identifies a table.
        :param fillna_with: Replace empty value with a default placeholder.
        Pass None if empty values should not be replaced.
        :return:
        """

        # table_id will return the raw table data.
        # This causes multiple select and single select to be returned as json objects

        # query and table_name will return the data as if the queried table is a prepended statement.
        # This causes multiple select and single select to be returned as strings instead of a json object

        if query:
            url_suffix = f"?query={query}"
        elif table_id:
            url_suffix = f"?table_id={table_id}"
        elif table_name:
            url_suffix = f"?table_name={table_name}"
        else:
            raise PeliqanClientException("Input 'table_name' (table or view name), 'query' or 'table_id' must be set.")

        json_response = self.__service_client__.get_records(url_suffix)

        error = json_response['error']
        if error:
            raise PeliqanClientException(f"Client encountered a error while fetching records,\n{error}")

        records = json_response['records']
        columns = json_response['columns']

        # Create dataframe
        df = pd.DataFrame(records, columns=columns)
        if fillna_with is not None:
            # replace Na/NaN
            df.fillna(fillna_with, inplace=True)
            # replace NaT
            df.replace({pandas.NaT: fillna_with}, inplace=True)
        return df

    # todo: make it easier to find table & field ids in UI
    def update_cell(self, row_pk, value, table_id=None, table_name=None, field_id=None, field_name=None):
        if not row_pk:
            raise PeliqanClientException("row_pk must be provided.")

        # BACKEND_URL and JWT are prepended to the generated script,
        # see create_script() --> transform_script() in peliqan/convert_raw_script.py
        base_url = f"{self.BACKEND_URL}/api/database/rows/table/%s/row/"

        if not table_id and not table_name:
            raise PeliqanClientException("table_id or table_name must be provided as kwargs")
        elif not table_id and table_name:
            # only do this if table_id is not provided
            table_id = self.__service_client__.get_cached_results('table', table_name, 'table_id')

        # prioritise field id
        if field_id:
            field_physical_name = f"field_{field_id}"
        elif field_name:
            for key in [table_name, table_id]:
                field_physical_name = self.__service_client__.get_cached_results('table', key, field_name)
                if field_physical_name:
                    break
        else:
            raise PeliqanClientException("field_id or field_name must be provided as kwargs")

        # Discover table_id and field_physical_name
        if not field_physical_name or not table_id:
            lookup_data = self.find_resource('table', resource_id=table_id, resource_name=table_name,
                                             field_id=field_id, field_name=field_name)
            field_physical_name = f"field_{lookup_data['field_id']}"
            table_id = lookup_data['table_id']

        # set the final url
        if type(table_id) != int:
            raise PeliqanClientException("table_id could not be resolved, please check provided arguments.")

        # set table_id to base url
        url = base_url % table_id

        data = {
            'row_id': row_pk,
            'value': value,
            'table_id': table_id,
            field_physical_name: value
        }
        return self.__service_client__.push_cdclog(url, data)

    def refresh_connection(self, connection_name=None, connection_id=None):
        base_url = f"{self.BACKEND_URL}/api/servers/%s/syncdb/"
        return self.__service_client__.refresh_resource(resource_type='connection', refresh_baseurl=base_url,
                                                        resource_name=connection_name, resource_id=connection_id)

    def refresh_database(self, connection_name=None, database_name=None, database_id=None):
        base_url = f"{self.BACKEND_URL}/api/applications/%s/syncdb/"
        return self.__service_client__.refresh_resource(resource_type='database', refresh_baseurl=base_url,
                                                        resource_name=database_name, resource_id=database_id,
                                                        connection_name=connection_name)

    def refresh_table(self, connection_name=None, database_name=None, table_name=None, table_id=None):

        base_url = f"{self.BACKEND_URL}/api/database/tables/%s/syncdb/"
        return self.__service_client__.refresh_resource(resource_type='table', refresh_baseurl=base_url,
                                                        resource_name=table_name, resource_id=table_id,
                                                        database_name=database_name, connection_name=connection_name)

    def connect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = WritebackClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def _validate_and_lookup_table(self, table_id, table_name):
        if not table_id and not table_name:
            raise PeliqanClientException("table_id or table_name must be provided as kwargs")
        elif not table_id and table_name:
            # only do this if table_id is not provided
            table_id = self.__service_client__.get_cached_results('table', table_name, 'table_id')

        if not table_id:
            lookup_data = self.find_resource('table', resource_id=table_id, resource_name=table_name)
            table_id = lookup_data['table_id']

        if type(table_id) != int:
            raise PeliqanClientException("table_id could not be resolved, please check provided arguments.")

        return table_id

    def _validate_writeback_status(self, writeback_status):
        error = False
        if type(writeback_status) == list:
            writeback_status_str = ''
            for w in writeback_status:
                w_status = w.upper()
                if w_status not in ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]:
                    error = True
                    break
                else:
                    writeback_status_str += w_status + ','
            writeback_status = writeback_status_str.rstrip(',')
        elif (
            writeback_status is not None and
            (
                type(writeback_status) != str or writeback_status.upper() not in
                ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]
            )
        ):
            error = True

        if error:
            raise PeliqanClientException(
                f"writeback_status is not valid. "
                f"Allowed status values are "
                f"'NOT_PROCESSED', 'PROCESSED', 'CONFIRMED', 'FAILED'."
            )

        return writeback_status

    def list_changes(self, table_id=None, table_name=None, writeback_status=None, change_type=None,
                     latest_changes_first=False):
        """
        List the cdc changes in order.
        Optionally, pass writeback_status and/or change_type as a string or list of strings.

        :param table_id: unique integer identifier for a table
        :param table_name: the name or fqn of the table.
        :param writeback_status: valid string or list of string values
        :param change_type: valid string or list of string values
        :param latest_changes_first: use this to get toggle the order of changes (Asc/Desc of id). default is False.
        :return:
        """

        error = False
        # i = insert, u = update, d = delete, t = transformation, f = formula, l = link (to another table)
        # m = multiselect
        if type(change_type) == list:
            change_type_str = ''
            for c in change_type:
                c_type = c.lower()
                if c_type not in ["i", "u", "d", "f", "t", "m", "l"]:
                    error = True
                    break
                else:
                    change_type_str += c_type + ','

            change_type = change_type_str.rstrip(',')
        elif (
            change_type is not None and
            (type(change_type) != str or change_type.lower() not in ["i", "u", "d", "f", "t", "m", "l"])
        ):
            error = True

        if error:
            raise PeliqanClientException(
                f"change_type is not valid. Allowed status values are 'i', 'u', 'd', 'f', 't', 'm', 'l'.\n"
                f"i = insert, u = update, d = delete, t = transformation, f = formula, l = link (to another table)"
                f"m = multiselect."
            )

        writeback_status = self._validate_writeback_status(writeback_status)

        table_id = self._validate_and_lookup_table(table_id, table_name)

        return self.__service_client__.get_cdclogs(table_id=table_id, writeback_status=writeback_status,
                                                   change_type=change_type, latest_changes_first=latest_changes_first)

    def update_writeback_status(self, change_id, writeback_status, table_id=None, table_name=None):
        """
        Update the writeback_status for a cdc log.

        :param change_id: unique integer identifier for a cdc log.
        :param writeback_status: valid status value.
        :param table_id: unique integer identifier for a table
        :param table_name: the name or fqn of the table.
        :return:
        """
        table_id = self._validate_and_lookup_table(table_id, table_name)
        if (
            type(writeback_status) != str or
            writeback_status.upper() not in ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]
        ):
            raise PeliqanClientException(
                f"writeback_status is not valid. "
                f"Allowed status values are "
                f"'NOT_PROCESSED', 'PROCESSED', 'CONFIRMED', 'FAILED'."
            )

        try:
            change_id = int(change_id)
        except ValueError:
            raise PeliqanClientException("change_id must be a valid integer")

        return self.__service_client__.update_writeback_status(table_id, change_id, writeback_status)

    def list_databases(self):
        """
        Returns a list of all databases in the account including tables and fields in tables.

        :return: list of databases
        """
        return self.__service_client__.get_databases()

    def update_field(self, id, description=None, tags=None):
        """
        Updates a field (column).

        :param id: required, integer, id of the field to update
        :param description: optional, string, description of the field (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the field (data catalog metadata)
        :return: result of update
        """

        return self.__service_client__.update_field_metadata(id, description, tags)

    def update_table(self, id, name=None, table_type=None, query=None, external=None, pk_field=None, settings=None,
                     description=None, tags=None):
        """
        Updates a table.

        :param id: required, integer, id of the table to update
        :param name: optional, string, new name of the table
        :param table_type: optional, string, new type of the table, e.g. 'query'
        :param query: optional, string, new SQL query for tables of type 'query'
        :param external: optional, boolean, true for external tables, false for internal tables
        :param pk_field: optional, string, primary key field name for this table, e.g. 'id'
        :param settings: optional, string (json), settings of the table
        :param description: optional, string, description of the table (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the table (data catalog metadata)
        :return: result of update
        """

        update_result_dict = {}
        update_metadata_result_dict = {}
        if name or table_type or query or external or pk_field or settings:
            update_result_dict = self.__service_client__.update_table(id, name, table_type, query, external, pk_field,
                                                                      settings)
        if description or tags:
            update_metadata_result_dict = self.__service_client__.update_table_metadata(id, description, tags)
        return {**update_result_dict, **update_metadata_result_dict}

    def update_database(self, id, description=None, tags=None):
        """
        Updates a database.

        :param id: required, integer, id of the database to update
        :param description: optional, string, description of the database (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the database (data catalog metadata)
        :return: result of update
        """

        return self.__service_client__.update_database_metadata(id, description, tags)

    def generate_sql_union(self, table_ids, sources=None):
        """
        Generates an SQL UNION query for the given tables.
        All columns of all tables will be added to the UNION query.
        If a column does not exist in one of the tables, it will be added with a null value.
        Optionally, a "source" column can be added to indicate from which table each row originated.

        :param table_ids: required, list of integers, list of table ids to include in UNION query
        :param sources: optional, dict, if set an extra 'source' column will be added to indicate to which table the record belongs. Keys are table ids. Values are source value to include in UNION result. Example: { 1: "Paris", 2: "London" }. This will add a column "source" to the UNION where all records from table id 1 will have value "Paris" for the source.
        :param table_type: optional, string, new type of the table, e.g. 'query'
        :param query: optional, string, new SQL query for tables of type 'query'
        :param external: optional, boolean, true for external tables, false for internal tables
        :param pk_field: optional, string, primary key field name for this table, e.g. 'id'
        :param settings: optional, string (json), settings of the table
        :return: result of update
        """
        databases = self.__service_client__.get_databases()
        tables = []
        fields = []
        field_types = {}
        fields_to_cast = []
        for database in databases:
            for table in database["tables"]:
                if table["id"] in table_ids:
                    tables.append(table)
                    for field in table["all_fields"]:
                        if field["name"] not in fields:
                            fields.append(field["name"])
                            if field["sql_data_type"]:
                                field_types[field["name"]] = field[
                                    "sql_data_type"]  # Actual field type in source, e.g. timestamp, timestamptz... (might not be available for all sources)
                            else:
                                field_types[field["name"]] = field["type"]  # Peliqan field type, e.g. "date"
                        elif (field["sql_data_type"] and field["sql_data_type"] != field_types[field["name"]]) or field[
                            "type"] != field_types[field["name"]]:
                            fields_to_cast.append(field["name"])

        table_selects = []
        for table in tables:
            table_select_fields = []
            if sources:
                source_name = ""
                for source_table_id, source_table_name in sources.items():
                    if int(source_table_id) == table['id']:
                        source_name = source_table_name
                table_select_fields.append("'%s'" % source_name + " source")
            for field in fields:
                table_has_field = False
                for table_field in table["all_fields"]:
                    if (
                        field[0] == '"' and table_field["name"] == field) or (
                        field[0] != '"' and table_field["name"].lower() == field.lower()
                    ):
                        table_has_field = True
                        break
                if table_has_field:
                    if field in fields_to_cast:
                        if table_field["sql_data_type"] and table_field["sql_data_type"] == "timestamptz":
                            # Postgres fields of type timestamptz (timestamp with timezone) cannot be cast to varchar directly by Trino
                            table_select_fields.append("CAST(CAST(%s AS TIMESTAMP) AS VARCHAR) AS %s" % (field, field))
                        else:
                            table_select_fields.append("CAST(%s AS VARCHAR) AS %s" % (field, field))
                    else:
                        table_select_fields.append(field)
                else:
                    table_select_fields.append("null " + field)
            table_select_fields_str = ", ".join(table_select_fields)

            table_select = "SELECT %s FROM %s" % (table_select_fields_str, table["name"])
            table_selects.append(table_select)

        union = " UNION ALL ".join(table_selects)
        return union


class Peliqan(BasePeliqanClient):
    """
        Import this API client to connect to a Peliqan environment and perform valid operations.

        :param jwt: The jwt token assigned to an Account.

        :param backend_url: The url of the Peliqan environment we want to connect to. A default can be set using the 'PELIQAN_URl' environment variable. If no value is provided it will fall back to "https://app.peliqan.io".
    """

    def __init__(self, jwt, backend_url=PELIQAN_URL):
        super(Peliqan, self).__init__(jwt, backend_url)
