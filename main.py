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
    "Gripper Number",
    "Picks",
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
    "Num Lockouts",
]

PICKS_HEADER = [
    "pick_id",
    "start_date",
    "start_time",
    "capture_count",
    "pick_attempts",
    "total_picks",
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

    save_name = input("Enter csv file name (don't include extension)\n")
    save_folder = askdirectory(title="Select Save Folder")

    if is_network_drive:
        folders = []
        folder = askdirectory(title="Select an experiment folder")
        while folder is not None and folder != "":
            folders.append(folder)
            folder = askdirectory(title="Select an experiment folder")
    else:
        folders = askopendirnames(title="Select Experiment Folders")

    summary_data = [SUMMARY_HEADERS]
    all_picks_data = [PICKS_HEADER]

    for folder in folders:
        try:
            basename = os.path.basename(folder)
            exp_number = basename[:15]
            lockout_path = os.path.join(folder, exp_number+"_lockout.txt")
            csv_dfs = parse_data(folder)

            # Summary
            row = summarize_folder(has_pick_trigger, basename, csv_dfs, lockout_path)
            summary_data.append(row)

            # Per Pick
            pick_data = aggregate_pick_data(csv_dfs)
            all_picks_data.extend(pick_data)

            save_path = os.path.join(save_folder, f"{save_name}_{basename}.csv")
            with open(save_path, "w") as f:
                write = csv.writer(f, lineterminator="\n")
                write.writerow(PICKS_HEADER)
                write.writerows(pick_data)

        except Exception as e:
            print(str(e))

    summary_save_path = os.path.join(save_folder, save_name + "_summary.csv")
    with open(summary_save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(summary_data)

    all_picks_save_path = os.path.join(save_folder, save_name + "_all_picks.csv")
    with open(all_picks_save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(all_picks_data)
