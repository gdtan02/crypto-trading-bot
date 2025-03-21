import json
import os
import logging
from json import JSONDecodeError

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict
from src.models.response_model import ResponseModel
from src.utils.utils import load_json
from config.settings import ENDPOINTS_PARAMS
from config.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, ETL_LOG_DIR

logger = logging.getLogger(__name__)

class JSONExtractor:

    ENDPOINT_COLUMNS = {
        'exchange-flows': [
            "reserve", "reserve_usd", "netflow_total", "inflow_total", "inflow_top10", "inflow_mean", "inflow_mean_ma7",
            "outflow_total", "outflow_top10", "outflow_mean", "outflow_mean_ma7", "transactions_count_inflow",
            "transactions_count_outflow", "addresses_count_inflow", "addresses_count_outflow"
        ],
        'miner-flows': [
            "reserve", "reserve_usd", "netflow_total", "inflow_total", "inflow_top10", "inflow_mean", "inflow_mean_ma7",
            "outflow_total", "outflow_top10", "outflow_mean", "outflow_mean_ma7", "transactions_count_inflow",
            "transactions_count_outflow", "addresses_count_inflow", "addresses_count_outflow"
        ],
        'market-data': [
            "high", "low", "open", "close", "volume", "open_interest", "taker_buy_ratio", "taker_sell_ratio",
            "taker_buy_sell_ratio", "taker_buy_volume", "taker_sell_volume", "long_liquidations",
            "long_liquidations_usd", "short_liquidations", "short_liquidations_usd", "coinbase_premium_gap",
            "coinbase_premium_gap_usdt_adjusted", "coinbase_premium_index","coinbase_premium_index_usdt_adjusted"
        ],
        "network-data": [
            "transactions_count_total", "transactions_count_mean", "addresses_count_active", "addresses_count_sender",
            "addresses_count_receiver", "fees_transaction_mean", "fees_transaction_mean_usd", "fees_transaction_median",
            "fees_transaction_median_usd", "blockreward", "blockreward_usd", "difficulty"
        ],
        "flow-indicator": [
            "mpi", "exchange_whale_ratio", "exchange_supply_ratio", "miner_supply_ratio"
        ],
        "market-indicator": [
            "estimated_leverage_ratio", "stablecoin_supply_ratio", "mvrv", "sopr"
        ],
        "network-indicator": [
            "nvt", "nvt_golden_cross", "nvm", "puell_multiple", "nupl", "nup", "nul", "nrpl"
        ]
    }

    def __init__(self):
        self.data = pd.DataFrame()

    def extract(self, symbol: str, category: str) -> ResponseModel:

        if category not in self.ENDPOINT_COLUMNS.keys():
            return ResponseModel(is_success=False, message="Not a valid category. Failed to fetch JSON data.", data=None)

        # Read the JSON file
        try:
            json_filename = os.path.join(RAW_DATA_DIR, f"new-{symbol}-{category}.json")
            responses = load_json(json_filename)
            if responses is None:
                return ResponseModel(is_success=False, message="Failed to load. The data is empty.", data=None)
        except (IOError, JSONDecodeError) as err:
            return ResponseModel(is_success=False, message="Failed to load JSON data", data=None)

        # Extract data into Pandas DataFrames and merge into single dataframe
        df_list = []
        for response in responses:
            df = pd.DataFrame(response["data"]).drop(columns="start_time")

            if ENDPOINTS_PARAMS[category][response["endpoint"]]["window"] == "day":
                df.rename(columns={"date": "datetime"}, inplace=True)

            df["datetime"] = pd.to_datetime(df["datetime"])
            df.set_index("datetime", inplace=True)
            df_list.append(df)

        self.data = pd.concat(df_list, sort=True, axis=1)

        # Save CSV
        try:
            csv_filename = f"new-{symbol}-{category}.csv"
            self.data.to_csv(os.path.join(RAW_DATA_DIR, csv_filename))
            logger.info(f"{csv_filename} has been saved successfully.")
            return ResponseModel(is_success=True, message=None, data=self.data)
        except Exception as e:
            logger.error(f"An error occurred while saving CSV file: {e}")
            return ResponseModel(is_success=True, message=f"An error occurred while saving CSV file: {e}", data=None)

if __name__ == "__main__":
    extractor = JSONExtractor()

    extracted_market_data = extractor.extract("btc", "market-data")
    if not extracted_market_data.is_success:
        print("Failed to extract market data")

    extracted_miner_flows = extractor.extract("btc", "miner-flows")
    if not extracted_miner_flows.is_success:
        print("Failed to extract miner flows data")

    extracted_exchange_flows = extractor.extract("btc", "exchange-flows")
    if not extracted_exchange_flows.is_success:
        print("Failed to extract exchange flows data")

    extracted_network_data = extractor.extract("btc", "network-data")
    if not extracted_network_data.is_success:
        print("Failed to extract network data")

    extracted_flow_indicator = extractor.extract("btc", "flow-indicator")
    if not extracted_flow_indicator.is_success:
        print("Failed to extract flow indicator data")

    extracted_market_indicator = extractor.extract("btc", "market-indicator")
    if not extracted_market_indicator.is_success:
        print("Failed to extract market indicator data")

    extracted_network_indicator = extractor.extract("btc", "network-indicator")
    if not extracted_network_indicator.is_success:
        print("Failed to extract network indicator data")