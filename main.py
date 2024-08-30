import argparse
import csv
from genericpath import isfile
import os
from distutils.dir_util import copy_tree
import shutil
from tkfilebrowser import askopendirnames
from tkinter.filedialog import askdirectory

from parsers.general import get_csv_file_name, parse_data
from parsers.picks_parser import aggregate_pick_data
from parsers.summary_parser import summarize_folder


SUMMARY_HEADERS = [
    "Folder Name",
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "Gripper Number",
    "Pick Attempts",
    "Success Rate",
    "Success",
    "Fails",
    "Vacuum Rate",
    "Magnetic Rate",
    "UR Rate",
    "EoP Rate",
    "Vacuum",
    "Magnetic",
    "UR",
    "EoP",
    "Velocity",
    "Acceleration",
    "Num Incomplete Picks",
    "Total Picks",
    "Picks Per Hour",
]

PICKS_HEADER = [
    "pick_id",
    "start_date",
    "start_time",
    "capture_count",
    "pick_attempts",
    "total_picks",
    "total_lockouts",
    "bin_region",
    "gen_source",
    "bin_empty",
    "gripper_num",
    "hor_vel",
    "hor_acc",
    "pick_activation",
    "is_successful",
    "pick_exec_time",
    "pick_end_date",
    "pick_end_time",
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-pt",
        "--pick-trigger",
        dest="pick_trigger",
        action="store_true",
        help="Is pick trigger implemented",
    )
    parser.add_argument(
        "-nd",
        "--network-drive",
        dest="network_drive",
        action="store_true",
        help="Are we retrieving files from the network drive",
    )

    args = parser.parse_args()
    has_pick_trigger = args.pick_trigger
    is_network_drive = args.network_drive

    folder_date = input("Enter date (E.g. Aug29)\n")
    station_name = input("Enter station name (E.g. Delta)\n")
    save_folder = askdirectory(title="Select Save Folder")

    if is_network_drive:
        folders = []
        folder = askdirectory(title="Select an experiment folder")
        while folder is not None and folder != "":
            folders.append(folder)
            folder = askdirectory(title="Select an experiment folder")
    else:
        folders = askopendirnames(title="Select Experiment Folders")

    data_folder_path = os.path.join(
        save_folder, f"{folder_date}_DailySummary_{station_name}_2024"
    )
    csv_folder_path = os.path.join(
        data_folder_path, f"{folder_date}_DailySummary_CSVData_{station_name}_2024"
    )
    parsed_folder_path = os.path.join(
        data_folder_path, f"{folder_date}_DailySummary_ParserData_{station_name}_2024"
    )

    other_folder_path = os.path.join(
        data_folder_path, f"{folder_date}_DailySummary_OtherFiles_{station_name}_2024"
    )

    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)

    if not os.path.exists(parsed_folder_path):
        os.makedirs(parsed_folder_path)

    if not os.path.exists(other_folder_path):
        os.makedirs(other_folder_path)

    summary_data = [SUMMARY_HEADERS]
    all_picks_data = [PICKS_HEADER]
    all_picks_filtered_data = [PICKS_HEADER]

    for folder in folders:
        try:
            basename = os.path.basename(folder)
            exp_number = basename[:15]

            # Copy CSVs
            csv_file_name = get_csv_file_name(folder)
            copy_tree(os.path.join(folder, csv_file_name), os.path.join(csv_folder_path,csv_file_name))

            # Copy txt files
            for file in os.listdir(folder):
                full_path = os.path.join(folder, file)
                if os.path.isfile(full_path):
                    shutil.copy2(full_path, other_folder_path)

            csv_dfs = parse_data(folder)

            # Per Pick
            total_picks, total_lockouts, pick_data_all, pick_data_filtered = (
                aggregate_pick_data(csv_dfs)
            )
            all_picks_data.extend(pick_data_all)
            all_picks_filtered_data.extend(pick_data_filtered)

            # Summary
            row = summarize_folder(
                has_pick_trigger, basename, csv_dfs, total_picks, total_lockouts
            )
            summary_data.append(row)

            save_path = os.path.join(
                parsed_folder_path,
                f"{folder_date}_DailySummary_{station_name}_2024_{basename}_all.csv",
            )
            with open(save_path, "w") as f:
                write = csv.writer(f, lineterminator="\n")
                write.writerow(PICKS_HEADER)
                write.writerows(pick_data_all)

            save_path = os.path.join(
                parsed_folder_path,
                f"{folder_date}_DailySummary_{station_name}_2024_{basename}_filtered.csv",
            )
            with open(save_path, "w") as f:
                write = csv.writer(f, lineterminator="\n")
                write.writerow(PICKS_HEADER)
                write.writerows(pick_data_filtered)

        except Exception as e:
            print(str(e))

    summary_save_path = os.path.join(
        data_folder_path, f"{folder_date}_DailySummary_2024_{station_name}_summary.csv"
    )
    with open(summary_save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(summary_data)

    all_picks_save_path = os.path.join(
        data_folder_path, f"{folder_date}_DailySummary_2024_{station_name}_all_picks.csv"
    )
    with open(all_picks_save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(all_picks_data)

    all_picks_filtered_save_path = os.path.join(
        data_folder_path,
        f"{folder_date}_DailySummary_2024_{station_name}_all_picks_filtered.csv",
    )
    with open(all_picks_filtered_save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(all_picks_filtered_data)
