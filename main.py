import argparse
import csv
import os
from tkfilebrowser import askopendirnames
from tkinter.filedialog import askdirectory

from parsers.general import parse_data
from parsers.picks_parser import aggregate_pick_data
from parsers.summary_parser import summarize_folder


SUMMARY_HEADERS = [
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

    save_name = input("Enter csv file name (don't include extension)\n")
    save_path = askdirectory(title="Select Save Folder")

    if is_network_drive:
        folders = []
        folder = askdirectory(title="Select an experiment folder")
        while folder is not None and folder != "":
            folders.append(folder)
            folder = askdirectory(title="Select an experiment folder")
    else:
        folders = askopendirnames(title="Select Experiment Folders")

    summary_data = [SUMMARY_HEADERS]

    for folder in folders:
        basename = os.path.basename(folder)
        csv_dfs = parse_data(folder)

        # Summary
        row = summarize_folder(has_pick_trigger, basename, csv_dfs)
        summary_data.append(row)

        # Per Pick
        pick_data = aggregate_pick_data(csv_dfs)
        save_path = os.path.join(save_path, f"{save_name}_{basename}.csv")
        with open(save_path, "w") as f:
            write = csv.writer(f, lineterminator="\n")
            write.writerows(pick_data)

    save_path = os.path.join(save_path, save_name + ".csv")
    with open(save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(summary_data)
