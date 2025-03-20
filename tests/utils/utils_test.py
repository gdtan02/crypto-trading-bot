import unittest
from datetime import datetime
from src.utils.utils import convert_datetime_to_unix_timestamp, convert_unix_timestamp_to_datetime

class MyTestCase(unittest.TestCase):

    def test_convert_datetime_str_to_unix_timestamp(self):
        datetime_str = "2025-03-19 13:36:25"
        unix_timestamp = convert_datetime_to_unix_timestamp(datetime_str)

        assert int(unix_timestamp) == 1742362585

    def test_convert_datetime_to_unix_timestamp(self):
        date_time = datetime(2025, 3, 19, 13, 36, 25)
        unix_timestamp = convert_datetime_to_unix_timestamp(date_time)

        assert int(unix_timestamp) == 1742362585

    def test_convert_unix_timestamp_to_datetime(self):
        unix_timestamp = 1742362585
        datetime = convert_unix_timestamp_to_datetime(unix_timestamp)

        assert datetime == "2025-03-19 13:36:25"

    def test_get_time_interval(self):
        NotImplemented


if __name__ == '__main__':
    unittest.main()
