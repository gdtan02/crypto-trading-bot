import os
import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

from requests import RequestException

from config.settings import CYBOTRADE_API_URL, CRYPTOQUANT_API_URL, DEFAULT_RESPONSE_LIMIT, ENDPOINTS_PARAMS
from src.utils.utils import save_json, convert_unix_timestamp_to_datetime, get_start_time, \
    convert_datetime_to_unix_timestamp
from src.models.response_model import ResponseModel

logger = logging.getLogger(__name__)

class CryptoQuantConnector:

    ROOT_URL = str(CRYPTOQUANT_API_URL)
    LIMIT = DEFAULT_RESPONSE_LIMIT
    SYMBOLS = ["btc", "eth"]


    def __init__(self):
        self.api_key = os.getenv("CYBOTRADE_API_KEY")
        self.headers = {"X-API-Key" : self.api_key }

    def fetch_data(self, symbol: str, category: str) -> ResponseModel:
        curr_timestamp = convert_datetime_to_unix_timestamp(datetime.now())
        logger.info(f"Current timestamp: {curr_timestamp}")

        if category not in ENDPOINTS_PARAMS.keys():
            error_message = "The API call does not fall belong a valid category"
            logger.error(error_message)
            return ResponseModel(is_success=False, message=error_message, data=None)

        responses: List[Dict] = []

        for endpoint, params in ENDPOINTS_PARAMS[category].items():
            url = self._parse_endpoint_url(symbol, category, endpoint, params)

            try:
                api_response = requests.get(url, headers=self.headers, timeout=30)
                api_response.raise_for_status()
                data = api_response.json()["data"]

                if data is None or []:
                    error_msg = "Failed to retrieve data. The data is empty. Please check the endpoint URL."
                    logger.error(error_msg)
                    return ResponseModel(is_success=False, message=error_msg, data=None)

                responses.append({"endpoint": endpoint, "data": data})

            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP Error occurred: {http_err}")
                return ResponseModel(is_success=False, message=f"HTTP Error occurred: {http_err}", data=None)

            except requests.exceptions.ConnectionError as conn_err:
                logger.error(f"Connection Error occurred: {conn_err}")
                return ResponseModel(is_success=False, message=f"Connection Error occurred: {conn_err}", data=None)

            except requests.exceptions.Timeout as timeout_err:
                logger.error(f"Connection Timeout: {timeout_err}")
                return ResponseModel(is_success=False, message=f"Connection Timeout: {timeout_err}", data=None)

            except requests.exceptions.JSONDecodeError as json_err:
                logger.error(f"Error while parsing JSON: {json_err}")
                return ResponseModel(is_success=False, message=f"Error while parsing JSON: {json_err}", data=None)

            except requests.exceptions.RequestException as err:
                logger.error(f"Error occurred: {err}")
                return ResponseModel(is_success=False, message=f"Error occurred: {err}", data=None)

        print("Final response: ", responses)
        return ResponseModel(is_success=True, message=None, data=responses)


    def _parse_endpoint_url(self, symbol: str, category: str, endpoint: str, params: Dict[str, str]) -> str:
        start_time = get_start_time(500)
        url = f"{self.ROOT_URL}/{symbol}/{category}/{endpoint}?start_time={start_time}&limit={self.LIMIT}"

        for key, value in params.items():
            url += f"&{key}={value}"

        logger.info(f"Endpoint URL: {url}")
        return url


if __name__ == "__main__":
    api_connector = CryptoQuantConnector()

    btc_market_data_response = api_connector.fetch_data('btc', 'market-data')
    if btc_market_data_response.is_success:
        save_json(btc_market_data_response.data, "new-btc-market-data.json")
    else:
        raise Exception(btc_market_data_response.message)

    btc_miner_flows_response = api_connector.fetch_data('btc', 'miner-flows')
    if btc_miner_flows_response.is_success:
        save_json(btc_miner_flows_response.data, "new-btc-miner-flows.json")
    else:
        raise Exception(btc_miner_flows_response.message)

    btc_exchange_flows_response = api_connector.fetch_data('btc', 'exchange-flows')
    if btc_exchange_flows_response.is_success:
        save_json(btc_exchange_flows_response.data, "new-btc-exchange-flows.json")
    else:
        raise Exception(btc_exchange_flows_response.message)

    btc_network_data_response = api_connector.fetch_data('btc', 'network-data')
    if btc_network_data_response.is_success:
        save_json(btc_network_data_response.data, "new-btc-network-data.json")
    else:
        raise Exception(btc_network_data_response.message)

    btc_flow_indicator_response = api_connector.fetch_data('btc', 'flow-indicator')
    if btc_flow_indicator_response.is_success:
        save_json(btc_flow_indicator_response.data, "new-btc-flow-indicator.json")
    else:
        raise Exception(btc_flow_indicator_response.message)

    btc_market_indicator_response = api_connector.fetch_data('btc', 'market-indicator')
    if btc_market_indicator_response.is_success:
        save_json(btc_market_indicator_response.data, "new-btc-market-indicator.json")
    else:
        raise Exception(btc_market_indicator_response.message)

    btc_network_indicator_response = api_connector.fetch_data('btc', 'network-indicator')
    if btc_network_indicator_response.is_success:
        save_json(btc_network_indicator_response.data, "new-btc-network-indicator.json")
    else:
        raise Exception(btc_network_indicator_response.message)

    # eth_market_data_response = api_connector.fetch_data('eth', 'market-data')
    # save_json(eth_market_data_response.data, "eth-market-data.json")
    #
    # eth_miner_flows_response = api_connector.fetch_data('eth', 'miner-flows')
    # save_json(eth_miner_flows_response.data, "eth-miner-flows.json")
    #
    # eth_exchange_flows_response = api_connector.fetch_data('eth', 'exchange-flows')
    # save_json(eth_exchange_flows_response.data, "eth-exchange-flows.json")
    #
    # eth_network_data_response = api_connector.fetch_data('eth', 'network-data')
    # save_json(eth_network_data_response.data, "eth-network-data.json")







