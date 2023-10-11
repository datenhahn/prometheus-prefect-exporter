import requests
import time


class PrefectFlows:
    """
    PrefectFlows class for interacting with Prefect's flows endpoints.
    """

    def __init__(self, url, headers, max_retries, logger, uri = "flows") -> None:
        """
        Initialize the PrefectFlows instance.

        Args:
            url (str): The URL of the Prefect instance.
            headers (dict): Headers to be included in HTTP requests.
            max_retries (int): The maximum number of retries for HTTP requests.
            logger (obj): The logger object.
            uri (str, optional): The URI path for administrative endpoints. Default is "flows".

        """
        self.headers     = headers
        self.uri         = uri
        self.url         = url
        self.max_retries = max_retries
        self.logger      = logger


    def get_flows_count(self) -> dict:
        """
        Get the count of Prefect flows.

        Returns:
            dict: JSON response containing the count of flows.

        """
        endpoint = f"{self.url}/{self.uri}/count"

        for retry in range(self.max_retries):
            try:
                resp = requests.post(endpoint, headers=self.headers)
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self.logger.error(err)
                if retry >= self.max_retries - 1:
                    time.sleep(1)
                    raise SystemExit(err)
            else:
                break

        return resp.json()


    def get_flows_info(self) -> dict:
        """
        Get information about Prefect flows.

        Returns:
            dict: JSON response containing information about flows.

        """
        endpoint = f"{self.url}/{self.uri}/filter"

        for retry in range(self.max_retries):
            try:
                resp = requests.post(endpoint, headers=self.headers)
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self.logger.error(err)
                if retry >= self.max_retries - 1:
                    time.sleep(1)
                    raise SystemExit(err)
            else:
                break

        return resp.json()


    def get_flows_name(self, flow_id) -> str:
        """
        Get name Prefect flows.

        Returns:
            dict: JSON response containing name flows.

        """
        endpoint = f"{self.url}/{self.uri}/{flow_id}"

        for retry in range(self.max_retries):
            try:
                resp = requests.get(endpoint, headers=self.headers)
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self.logger.error(err)
                if retry >= self.max_retries - 1:
                    time.sleep(1)
                    raise SystemExit(err)
            else:
                break

        return resp.json().get("name", "null")
