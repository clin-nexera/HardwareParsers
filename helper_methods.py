import json
import os
import pandas as pd
from datetime import datetime

pd.DataFrame()

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
        raise FileNotFoundError(
            f"ERROR - The csv files directory for {path} was not found"
        )
    
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
        raise FileNotFoundError(
            f"ERROR - The config json file in {path} was not found"
        )

    return config_file


def get_csv_paths(csv_directory_path: str, csv_names: list[str]):
    csv_filenames = os.listdir(csv_directory_path)
    csv_paths = {}

    for csv in csv_names:
        csv_paths[csv] = os.path.join(
            csv_directory_path,
            next((name for name in csv_filenames if csv in name), None),
        )

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


def get_start_dates(csv_dfs):
    csv = csv_dfs["pre_pick_process_states"]
    date = str(csv["pick_start_date"][0])
    time = str(csv["pick_start_time"][0])
    date_obj = datetime.strptime(date, "%Y%m%d")
    time_obj = datetime.strptime(time, "%H%M%S")

    date_reformatted = date_obj.strftime("%b-%d")
    time_reformatted = time_obj.strftime("%H:%M")

    return date_reformatted, time_reformatted


def get_end_dates(csv_dfs):
    csv = csv_dfs["post_pick_process_states"]
    num = len(csv["index"]) - 1
    date = str(object=csv["pick_end_date"][num])
    time = str(csv["pick_end_time"][num])
    date_obj = datetime.strptime(date, "%Y%m%d")
    time_obj = datetime.strptime(time, "%H%M%S")

    date_reformatted = date_obj.strftime("%b-%d")
    time_reformatted = time_obj.strftime("%H:%M")

    return date_reformatted, time_reformatted


def get_pick_counts(csv_dfs):
    csv = csv_dfs["pick_execution"]
    num_picks = len(csv.index)
    counts = csv["is_successful_pick"].value_counts()
    successful = counts[True] if "successful" in counts.keys() else 0
    failed_picks = counts[False] if "failed_picks" in counts.keys() else 0
    return num_picks, successful, failed_picks


def get_trigger_counts(csv_dfs):
    csv = csv_dfs["pick_execution"]
    counts = csv["pick_activation"].value_counts()
    vacuum = counts["Vacuum"] if "Vacuum" in counts.keys() else 0
    magnetic = counts["Magnetic Sensor"] if "Magnetic Sensor" in counts.keys() else 0
    ur = counts["UR"] if "UR" in counts.keys() else 0
    eop = counts["End of Path"] if "End of Path" in counts.keys() else 0

    return vacuum, magnetic, ur, eop


def get_vel_acc(csv_dfs):
    csv = csv_dfs["path_planner"]
    vel = csv["pose_path_2_above_drop_bin_vel"][0]
    acc = csv["pose_path_2_above_drop_bin_acc"][0]
    return vel, acc
