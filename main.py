import argparse
import csv
import os
from tkfilebrowser import askopendirnames
from tkinter.filedialog import askdirectory

from helper_methods import *

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
    is_legacy = args.legacy

    save_name = input("Enter csv file name (don't include extension)\n")
    save_path = askdirectory(title="Select Save Folder")

    data = [
        [
            "Folder Name",
            "Start Date",
            "Start Time",
            "End Date",
            "End Time",
            "Picks",
            "Success",
            "Fails",
            "Vacuum",
            "Magnetic",
            "UR",
            "EoP",
            "Velocity",
            "Acceleration",
        ]
    ]

    if is_network_drive:
        folders = []
        folder = askdirectory(title="Select an experiment folder")
        while folder is not None and folder != "":
            folders.append(folder)
            folder = askdirectory(title="Select an experiment folder")
    else:
        folders = askopendirnames(title="Select Experiment Folders")

    for folder in folders:
        basename = os.path.basename(folder)
        csv_dfs = parse_data(folder, has_pick_trigger)
        picks, success, fails = get_pick_counts(csv_dfs)
        start_date, start_time = get_start_dates(csv_dfs)
        end_date, end_time = get_end_dates(csv_dfs)

        vacuum, magnetic, ur, eop = (
            get_trigger_counts(csv_dfs) if has_pick_trigger else (None, None, None, None)
        )

        vel, acc = get_vel_acc(csv_dfs)

        row = [
            basename,
            start_date,
            start_time,
            end_date,
            end_time,
            picks,
            success,
            fails,
            vacuum,
            magnetic,
            ur,
            eop,
            vel,
            acc,
        ]
        data.append(row)

    save_path = os.path.join(save_path, save_name + ".csv")
    with open(save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(data)
