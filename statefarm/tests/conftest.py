import httpx
import pytest

import numpy as np
import pandas as pd
from companyname.data.data_preparation import DataSplitter, DataPreprocessor
from companyname import app


@pytest.fixture(scope="module")
def sample_dataframe():
    return pd.read_csv("companyname/files/data/exercise_26_train.csv").head(1000)


@pytest.fixture(scope="function")
def data_splitter(sample_dataframe):
    y_vars = ["y"]
    return DataSplitter(sample_dataframe, y_vars)


@pytest.fixture(scope="module")
def data_preprocessor():
    columns_to_convert = ["x12", "x63"]
    columns_to_impute = [
        "x0",
        "x1",
        "x2",
        "x3",
        "x4",
        "x6",
        "x7",
        "x8",
        "x9",
        "x10",
        "x11",
        "x13",
        "x14",
        "x15",
        "x16",
        "x17",
        "x18",
        "x19",
        "x20",
        "x21",
        "x22",
        "x23",
        "x24",
        "x25",
        "x26",
        "x27",
        "x28",
        "x29",
        "x30",
        "x32",
        "x33",
        "x34",
        "x35",
        "x36",
        "x37",
        "x38",
        "x39",
        "x40",
        "x41",
        "x42",
        "x43",
        "x44",
        "x45",
        "x46",
        "x47",
        "x48",
        "x49",
        "x50",
        "x51",
        "x52",
        "x53",
        "x54",
        "x55",
        "x56",
        "x57",
        "x58",
        "x59",
        "x60",
        "x61",
        "x62",
        "x64",
        "x65",
        "x66",
        "x67",
        "x68",
        "x69",
        "x70",
        "x71",
        "x72",
        "x73",
        "x74",
        "x75",
        "x76",
        "x77",
        "x78",
        "x79",
        "x80",
        "x83",
        "x84",
        "x85",
        "x86",
        "x87",
        "x88",
        "x89",
        "x90",
        "x91",
        "x92",
        "x93",
        "x94",
        "x95",
        "x96",
        "x97",
        "x98",
        "x99",
    ]
    columns_to_dummy = ["x5", "x31", "x81", "x82"]
    return DataPreprocessor(columns_to_convert, columns_to_impute, columns_to_dummy)


@pytest.fixture
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
def sample_data():
    return {
        "data": [
            {
                "x0": 0.042317,
                "x1": -3.344721,
                "x2": 4.6351242122,
                "x3": -0.5983959993,
                "x4": -0.6477715046,
                "x5": "monday",
                "x6": 0.184902,
                "x7": 46.690015,
                "x8": 3.034132,
                "x9": 0.364704,
                "x10": 14.260733,
                "x11": -1.559332,
                "x12": "$5,547.78",
                "x13": 0.520324,
                "x14": 31.212255,
                "x15": 4.891671,
                "x16": 0.357763,
                "x17": 14.766366,
                "x18": -17.467243,
                "x19": 0.224628,
                "x20": 0.096752,
                "x21": 1.305564,
                "x22": 0.353632,
                "x23": 3.909028,
                "x24": -91.273052,
                "x25": 1.396952,
                "x26": 4.401593,
                "x27": 0.443086,
                "x28": 14.048787,
                "x29": -0.932243,
                "x30": 5.255472,
                "x31": "germany",
                "x32": 0.54199153,
                "x33": 2.98948039,
                "x34": -1.78334189,
                "x35": 0.80127315,
                "x36": -2.60231221,
                "x37": 3.39682926,
                "x38": -1.22322646,
                "x39": -2.20977636,
                "x40": -68.69,
                "x41": 522.25,
                "x42": -428.69,
                "x43": 381.37,
                "x44": 0.0197503,
                "x45": 0.75116479,
                "x46": 0.8630479008,
                "x47": -1.0383166613,
                "x48": -0.2726187635,
                "x49": -0.3430207259,
                "x50": 0.3109008666,
                "x51": -0.797841974,
                "x52": -2.0390175153,
                "x53": 0.87182889,
                "x54": 0.14373012,
                "x55": -1.15212514,
                "x56": -2.1703139704,
                "x57": -0.267842962,
                "x58": 0.212110633,
                "x59": 1.6926559407,
                "x60": -0.9522767913,
                "x61": -0.8625864974,
                "x62": 0.0748487158,
                "x63": "36.29%",
                "x64": 3.47125327,
                "x65": -3.16656509,
                "x66": 0.65446814,
                "x67": 14.60067029,
                "x68": -20.57521013,
                "x69": 0.71083785,
                "x70": 0.16983767,
                "x71": 0.55082127,
                "x72": 0.62814576,
                "x73": 3.38608078,
                "x74": -112.45263714,
                "x75": 1.48370808,
                "x76": 1.77035368,
                "x77": 0.75702363,
                "x78": 14.75731742,
                "x79": -0.62550355,
                "x80": np.NaN,
                "x81": "October",
                "x82": "Female",
                "x83": -0.7116680715,
                "x84": -0.2653559892,
                "x85": 0.5175495907,
                "x86": -1.0881027092,
                "x87": -1.8188638198,
                "x88": -1.3584469527,
                "x89": -0.654995195,
                "x90": -0.4933042262,
                "x91": 0.373853,
                "x92": 0.94143481,
                "x93": 3.54679834,
                "x94": -99.8574882,
                "x95": 0.403926,
                "x96": 1.65378726,
                "x97": 0.00771459,
                "x98": -32.02164582,
                "x99": -60.3127828,
            },
            {
                "x0": 0.123456,
                "x1": -2.345678,
                "x2": 5.6789012345,
                "x3": -0.987654321,
                "x4": -1.2345678901,
                "x5": "tuesday",
                "x6": 0.567890,
                "x7": 12.345678,
                "x8": 6.789012,
                "x9": 0.123456,
                "x10": 23.456789,
                "x11": -3.456789,
                "x12": "$7,890.12",
                "x13": 0.234567,
                "x14": 45.678901,
                "x15": 7.890123,
                "x16": 0.456789,
                "x17": 23.456789,
                "x18": -12.345678,
                "x19": 0.345678,
                "x20": 0.567890,
                "x21": 2.345678,
                "x22": 1.234567,
                "x23": 4.567890,
                "x24": -67.890123,
                "x25": 2.345678,
                "x26": 5.678901,
                "x27": 0.678901,
                "x28": 12.345678,
                "x29": -1.234567,
                "x30": 7.890123,
                "x31": "usa",
                "x32": 0.67890123,
                "x33": 3.45678901,
                "x34": -2.3456789,
                "x35": 0.12345678,
                "x36": -1.23456789,
                "x37": 2.34567890,
                "x38": -0.12345678,
                "x39": -1.23456789,
                "x40": -45.67,
                "x41": 123.45,
                "x42": -34.56,
                "x43": 67.89,
                "x44": 0.05678901,
                "x45": 0.12345678,
                "x46": 0.2345678901,
                "x47": -0.3456789012,
                "x48": -0.4567890123,
                "x49": -0.5678901234,
                "x50": 0.6789012345,
                "x51": -0.7890123456,
                "x52": -0.8901234567,
                "x53": 0.9012345678,
                "x54": 0.0123456789,
                "x55": -1.1234567890,
                "x56": -2.2345678901,
                "x57": -0.3456789012,
                "x58": 0.4567890123,
                "x59": 2.3456789012,
                "x60": -1.2345678901,
                "x61": -0.3456789012,
                "x62": 0.1234567890,
                "x63": "45.67%",
                "x64": 4.567890123,
                "x65": -4.567890123,
                "x66": 0.567890123,
                "x67": 12.34567890,
                "x68": -23.45678901,
                "x69": 0.789012345,
                "x70": 0.890123456,
                "x71": 0.901234567,
                "x72": 0.012345678,
                "x73": 4.567890123,
                "x74": -123.4567890,
                "x75": 2.345678901,
                "x76": 2.345678901,
                "x77": 0.890123456,
                "x78": 12.34567890,
                "x79": -0.123456789,
                "x80": np.NaN,
                "x81": "November",
                "x82": "Male",
                "x83": -0.9876543210,
                "x84": -0.2345678901,
                "x85": 0.6789012345,
                "x86": -1.5678901234,
                "x87": -1.2345678901,
                "x88": -0.7890123456,
                "x89": -0.4567890123,
                "x90": -0.5678901234,
                "x91": 0.678901234,
                "x92": 0.9012345678,
                "x93": 4.567890123,
                "x94": -67.8901234,
                "x95": 0.234567890,
                "x96": 1.234567890,
                "x97": 0.123456789,
                "x98": -45.67890123,
                "x99": -12.34567890,
            },
        ]
    }