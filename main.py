import argparse
import csv
from datetime import datetime
from email.mime import base
from nexera_packages.data_management.adapters.validation_gui_experiment_parser import (
    ValidationGUIExperimentParser,
)
import os
from tkfilebrowser import askopendirnames, askopendirname

def get_start_dates(experiment):
    csv = experiment.csv_dfs["pre_pick_process_states"]
    date = str(csv["pick_start_date"][0])
    time = str(csv["pick_start_time"][0])
    date_obj = datetime.strptime(date, '%Y%m%d')
    time_obj = datetime.strptime(time, '%H%M%S')

    date_reformatted = date_obj.strftime("%b-%d")
    time_reformatted = time_obj.strftime("%H:%M")

    return date_reformatted, time_reformatted


def get_end_dates(experiment):
    csv = experiment.csv_dfs["post_pick_process_states"]
    num = len(csv["index"]) - 1
    date = str(csv["pick_end_date"][num])
    time = str(csv["pick_end_time"][num])
    date_obj = datetime.strptime(date, "%Y%m%d")
    time_obj = datetime.strptime(time, "%H%M%S")

    date_reformatted = date_obj.strftime("%b-%d")
    time_reformatted = time_obj.strftime("%H:%M")

    return date_reformatted, time_reformatted


def get_pick_counts(experiment):
    picks = experiment.picks

    num_picks = 0
    successful = 0

    for pick in picks.values():
        num_picks += 1
        if pick.pick_successful:
            successful += 1
    failed_picks = num_picks - successful
    return num_picks, successful, failed_picks

def get_trigger_counts(experiment):
    picks = experiment.picks

    vacuum = 0
    magnetic = 0
    ur = 0
    eop = 0

    for pick in picks.values():
        pick_activation = pick.pick_activation
        if pick_activation == "Vacuum":
            vacuum += 1
        elif pick_activation == "Magnetic Sensor":
            magnetic += 1
        elif pick_activation == "UR":
            ur += 1
        else:
            eop += 1
    
    return vacuum, magnetic, ur, eop


def get_vel_acc(experiment):
    csv = experiment.csv_dfs["path_planner"]
    vel = csv["pose_path_2_above_drop_bin_vel"][0]
    acc = csv["pose_path_2_above_drop_bin_acc"][0]
    return vel, acc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-pt",
        "--pick-trigger",
        dest="pick_trigger",
        action="store_true",
        help="Is pick trigger implemented",
    )
    args = parser.parse_args()
    has_pick_trigger = args.pick_trigger

    save_name = input("Enter csv file name (don't include extension)\n")
    save_path = askopendirname(title="Select Save Folder")

    experiment_parser = ValidationGUIExperimentParser()
    data = [["Folder Name", "Start Date", "Start Time", "End Date", "End Time", "Picks", "Success", "Fails", "Vacuum", "Magnetic", "UR", "EoP", "Velocity", "Acceleration"]]

    folders = askopendirnames(title="Select Experiment Folders")
    for folder in folders:
        basename = os.path.basename(folder)
        experiment = experiment_parser.parseExperiment(folder, has_pick_trigger)
        picks, success, fails = get_pick_counts(experiment)
        start_date, start_time = get_start_dates(experiment)
        end_date, end_time = get_end_dates(experiment)

        vacuum, magnetic, ur, eop = (
            get_trigger_counts(experiment) if has_pick_trigger else (None, None, None, None)
        )

        vel, acc = get_vel_acc(experiment)

        row = [basename, start_date, start_time, end_date, end_time, picks, success, fails, vacuum, magnetic, ur, eop, vel, acc]
        data.append(row)

    save_path = os.path.join(save_path, save_name + ".csv")
    with open(save_path, "w") as f:
        write = csv.writer(f, lineterminator="\n")
        write.writerows(data)
