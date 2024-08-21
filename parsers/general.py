import json
import os

import pandas as pd

CSV_NAMES_VALIDATION = [
    "pre_pick_process_states",
    "inputs",
    "pick_pose",
    "place_pose",
    "mode_selection",
    "path_planner",
    "pick_execution",
    "post_pick_process_states",
]


def parse_data(path: str):
    csv_file_path = get_csv_file_name(path)

    csv_paths = get_csv_paths(os.path.join(path, csv_file_path), CSV_NAMES_VALIDATION)
    csv_dataframes = create_dataframes(csv_paths, CSV_NAMES_VALIDATION)

    if csv_paths["inputs"] == None:
        raise FileNotFoundError("Inputs CSV file not found")

    return csv_dataframes


def get_csv_file_name(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"ERROR - {path} was not found")

    sub_dirs = os.listdir(path)

    csv_directory = next(
        (name for name in sub_dirs if "csv_files" in name),
        None,
    )
    if csv_directory == None:
        raise FileNotFoundError(f"ERROR - The csv files directory for {path} was not found")

    return csv_directory


def get_config_file_name(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"ERROR - {path} was not found")

    sub_dirs = os.listdir(path)

    config_file = next(
        (name for name in sub_dirs if "config" in name),
        None,
    )

    if config_file == None:
        raise FileNotFoundError(f"ERROR - The config json file in {path} was not found")

    return config_file


def get_csv_paths(csv_directory_path: str, csv_names: list[str]):
    csv_filenames = os.listdir(csv_directory_path)
    csv_paths = {}

    for csv in csv_names:
        find_name = next((name for name in csv_filenames if csv in name), None)
        if find_name is None:
            raise FileNotFoundError(f"ERROR - The csv file {csv} could not be found")
        csv_paths[csv] = os.path.join(csv_directory_path, find_name)

    return csv_paths


def create_dataframes(paths, csv_names):
    csv_dataframes = {}

    for csv in csv_names:
        csv_dataframes[csv] = pd.read_csv(paths[csv])

    return csv_dataframes


def config_file_2_dict(path: str):
    json_file = open(path)
    json_data = json.load(json_file)
    json_file.close()
    return json_data
