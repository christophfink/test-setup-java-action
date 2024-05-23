#!/usr/bin/env python3

# This is a init file common to all tests. It is automatically sourced
# by pytest et al.

# Define common constants (e.g., paths to test data) and fixtures (e.g.,
# transport network) here.

import datetime
import pathlib
import pytest


# test data
DATA_DIRECTORY = pathlib.Path(__file__).resolve().parent / "data"
ORIGINS_INVALID_NO_ID = DATA_DIRECTORY / "test_invalid_points_no_id_column.geojson"
ORIGINS_INVALID_DUPLICATE_IDS = (
    DATA_DIRECTORY / "test_invalid_points_duplicate_ids.geojson"
)
ORIGINS_VALID_IDS = DATA_DIRECTORY / "test_valid_points_data.geojson"
SINGLE_VALID_ORIGIN = DATA_DIRECTORY / "test_valid_single_point_data.geojson"

R5_JAR_URL = (
    "https://github.com/r5py/r5/releases/download/v7.1-r5py/r5-v7.1-r5py-all.jar"
)
R5_JAR_SHA256 = "cd697b50323fd99977c98039ea317698bcf5fbbdb12b59e3e094ae9443648db2"
R5_JAR_SHA256_INVALID = "adfadsfadsfadsfasdfasdf"
R5_JAR_SHA256_GITHUB_ERROR_MESSAGE_WHEN_POSTING = (
    "14aa2347be79c280e4d0fd3a137fb8f5bf2863261a1e48e1a122df1a52a0f453"
)

SNAPPED_POPULATION_GRID_POINTS = (
    DATA_DIRECTORY / "test_snapped_population_grid_centroids.geojson"
)

WALKING_TIMES_SNAPPED = DATA_DIRECTORY / "test_walking_times_snapped.csv"
WALKING_TIMES_NOT_SNAPPED = DATA_DIRECTORY / "test_walking_times_not_snapped.csv"
WALKING_DETAILS_SNAPPED = DATA_DIRECTORY / "test_walking_details_snapped.csv"
WALKING_DETAILS_NOT_SNAPPED = DATA_DIRECTORY / "test_walking_details_not_snapped.csv"

DETAILED_ITINERARIES_BICYCLE = (
    DATA_DIRECTORY / "test_detailed_itineraries_bicycle.gpkg.zip"
)
DETAILED_ITINERARIES_CAR = DATA_DIRECTORY / "test_detailed_itineraries_car.gpkg.zip"
DETAILED_ITINERARIES_TRANSIT = (
    DATA_DIRECTORY / "test_detailed_itineraries_transit.gpkg.zip"
)
DETAILED_ITINERARIES_WALK = DATA_DIRECTORY / "test_detailed_itineraries_walk.gpkg.zip"

SAMPLE_DATA_SET_URL = "https://raw.githubusercontent.com/r5py/r5py.sampledata.sao_paulo/main/data/spo_hexgrid.csv"
SAMPLE_DATA_SET_SHA256 = (
    "769660f8f1bc95d2741bbc4225e5e0e77e73461ea8b3e225a58e397b0748bdd4"
)


@pytest.fixture
def data_columns_with_breakdown():
    yield [
        "from_id",
        "to_id",
        "travel_time",
        "routes",
        "board_stops",
        "alight_stops",
        "ride_times",
        "access_time",
        "egress_time",
        "transfer_time",
        "wait_times",
        "total_time",
        "n_iterations",
    ]


@pytest.fixture(scope="session")
def departure_datetime():
    yield datetime.datetime(2022, 2, 22, 8, 30)


@pytest.fixture
def gtfs_timezone_helsinki():
    yield "Europe/Helsinki"
