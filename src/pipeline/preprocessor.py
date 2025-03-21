import logging
import numpy as np
import pandas as pd
from typing import Dict, Optional, List
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, StandardScaler, power_transform
from sklearn.model_selection import train_test_split
from pathlib import Path

from config.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.models.response_model import ResponseModel

logger = logging.getLogger(__name__)

class DataPreprocessor(BaseEstimator):

    SYMBOLS = ['btc', 'eth']
    ENDPOINTS = [
        'market-data', 'network-data', 'exchange-flows', 'miner-flows', 'market-indicator', 'network-indicator',
        'flow-indicator'
    ]

    def __init__(self, symbol: str = 'btc'):
        self.raw_data_files: Dict[str, pd.DataFrame] = {}
        self.full_df = pd.DataFrame()
        self.symbol = symbol if symbol in self.SYMBOLS and symbol is not None else 'btc'  # Default to btc
        self._load_data()

    def _load_data(self):
        try:
            for endpoint in self.ENDPOINTS:
                filename = f"new-{self.symbol}-{endpoint}.csv"
                filepath = RAW_DATA_DIR / filename
                df = pd.read_csv(filepath)
                df["datetime"] = pd.to_datetime(df["datetime"])
                df.set_index("datetime", inplace=True)
                self.raw_data_files[endpoint] = df
        except (IOError, FileNotFoundError) as err:
            logger.error(f"File Not Found: {err}")
            return ResponseModel(is_success=False, message=f"File Not Found: {err}", data=None)


    def merge_tables(self):
        if self.raw_data_files is None:
            logger.error("Data has not been loaded.")
            return ResponseModel(is_success=False, message="Data has not been loaded.", data=None)

        logger.info("Renaming the columns...")
        for endpoint, data in self.raw_data_files.items():
            # Append `miner` and `exchange` for miner flows and exchange flows data to differentiate these columns
            column_names = data.columns
            if endpoint == "miner-flows":
                column_names = { name : f"miner_{name}" for name in column_names }
                data.rename(columns=column_names, inplace=True)
            elif endpoint == "exchange-flows":
                column_names = { name : f"exchange_{name}" for name in column_names }
                data.rename(columns=column_names, inplace=True)

            logger.info(f"Endpoint: {endpoint}, Columns: {data.columns}")

        self.full_df = pd.concat(self.raw_data_files.values(), sort=True, axis=1)
        self.full_df.to_csv(PROCESSED_DATA_DIR / "btc_data.csv")

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    preprocessor.merge_tables()
