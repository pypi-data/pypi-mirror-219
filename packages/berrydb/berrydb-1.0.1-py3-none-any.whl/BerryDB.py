import requests
import json
from urllib.parse import quote

from sys import exit

debug_mode = False

generic_error_message = "Oops! something went wrong. Please try again later."

base_url = "https://app.berrydb.io"

get_database_id_url = base_url + "/profile/database"

documents_url = base_url + "/berrydb/documents"
query_url = base_url + "/berrydb/query"
upsert_url = base_url + "/berrydb/documents/{}"
document_by_id_url = base_url + "/berrydb/documents/{}"


class BerryDB:
    @classmethod
    def connect(self, api_key: str, database_name: str, bucket_name: str):
        """Function summary

        Args:
            arg1 (str): API Key
            arg2 (str): Database Name
            arg3 (str): Bucket Name

        Returns:
            Database Reference: An instance of the database
        """

        if debug_mode:
            print("api_key: ", api_key)
            print("database_name: ", database_name)
            print("bucket_name: ", bucket_name)
            print("\n\n")

        database_id: int = self.__getDataBaseId(self, api_key, database_name)

        return Database(api_key, bucket_name, database_id)

    def __getDataBaseId(self, api_key: str, database_name: str) -> int:
        """Function summary

        Args:
            arg1 (str): API Key
            arg2 (str): Database Name

        Returns:
            int : Database ID
        """

        url = get_database_id_url
        params = {"apiKey": api_key, "databaseName": database_name}

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                self.__handleApiCallFailure(self, response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            json_res = json.loads(response.text)
            if json_res.get("database", None):
                return json_res["database"].get("id", None)
            return
        except Exception as e:
            print("Failed to fetch your database: {}".format(str(e)))
            return None

    def __handleApiCallFailure(self, res, status_code):
        if status_code == 401:
            self.__print_error_and_exit(
                "You are Unauthorized. Please check you API Key"
            )
        if res.get("errorMessage", None):
            errMsg = res["errorMessage"]
        else:
            errMsg = generic_error_message if (res == None or res == "") else res
        raise Exception(errMsg)

    def __print_error_and_exit(self, msg=None):
        msg = msg if msg is not None else generic_error_message
        print(msg)
        exit()


class Database:
    __api_key: str
    __bucket_name: str
    __database_id: int

    def __init__(self, api_key: str, bucket_name: str, database_id: int):
        if api_key is None:
            self.__print_error_and_exit("API Key cannot be None")
        if bucket_name is None:
            self.__print_error_and_exit("Bucket name cannot be None")
        if database_id is None:
            self.__print_error_and_exit("Database not found")
        self.__api_key = api_key
        self.__bucket_name = bucket_name
        self.__database_id = database_id

    def get_all_documents(self):
        """Function summary

        Args:
            No Arguments

        Returns:
            list: List of Documents
        """

        url = documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                self.__handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_all_documents_with_col_filter(self, col_filter=["*"]):
        """Function summary

        Args:
            arg1 (list<str>): Column list (Optional)

        Returns:
            list: List of Documents
        """

        url = documents_url
        """ params = {
            "columns": col_filter,
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        } """
        url += "?apiKey=" + self.__api_key
        url += "&bucket=" + self.__bucket_name
        url += "&databaseId=" + str(self.__database_id)
        url += "&columns=" + (",".join(col_filter))

        if debug_mode:
            print("url:", url)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                self.__handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            # return response.json()
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_document_by_object_id(
        self,
        document_id,
        key_name=None,
        key_value=None,
    ):
        """Function summary

        Args:
            arg1 (str): Document Key/Id
            arg2 (str): Key Name (optional)
            arg3 (str): Key Value (optional)

        Returns:
            list: List of Documents
        """

        url = document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if document_id is not None:
            params["docId"] = document_id
        if key_name is not None:
            params["keyName"] = key_name
        if key_value is not None:
            params["keyValue"] = key_value

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                self.__handleApiCallFailure(response.json(), response.status_code)
            jsonRes = response.json()
            if debug_mode:
                print("docById result ", jsonRes)
            return jsonRes
        except Exception as e:
            print("Failed to fetch document by id {} : {}".format(document_id, str(e)))
            return ""

    def query(self, query: str):
        """Function summary

        Args:
            arg1 (str): Query String

        Returns:
            list: List of Documents
        """

        url = query_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }
        payload = query

        if debug_mode:
            print("url:", url)
            print("query:", query)
            print("params:", params)
        headers = self.__get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                self.__handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("query result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to query : {}".format(str(e)))
            return ""

    def upsert_document(self, document: object) -> json:
        """Function summary

        Args:
            arg1 (str): Document Data Object to add/update (Has to have a key 'objectId')

        Returns:
            str: Success message
        """

        docId = document.get("objectId")
        url = upsert_url.format(quote(docId))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        payload = json.dumps({"document": document, "bucket": self.__bucket_name})
        if debug_mode:
            print("docId:", docId)
            print("url:", url)
            print("payload:", payload)
        headers = self.__get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                self.__handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("upsert result ", response)
            return response.text
        except Exception as e:
            print("Failed to upsert document: {}".format(str(e)))
            return ""

    def __get_headers(self, api_key: str, content_type: str = "application/json"):
        return {"Content-Type": content_type, "x-api-key": api_key, "Accept": "*/*"}

    def __handleApiCallFailure(self, res, status_code):
        if status_code == 401:
            self.__print_error_and_exit(
                "You are Unauthorized. Please check you API Key"
            )
        if res.get("errorMessage", None):
            errMsg = res["errorMessage"]
        else:
            errMsg = generic_error_message if (res == None or res == "") else res
        raise Exception(errMsg)

    def __print_error_and_exit(self, msg=None):
        msg = msg if msg is not None else generic_error_message
        print(msg)
        exit(0)
