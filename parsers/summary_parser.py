import os
from datetime import datetime


def summarize_folder(has_pick_trigger, basename, csv_dfs, pick_attempts, total_lockouts):
    total_picks = pick_attempts + total_lockouts

    success, fails = get_pick_counts(csv_dfs)
    start_date, start_time = get_start_dates(csv_dfs)
    end_date, end_time = get_end_dates(csv_dfs)

    mode = get_gripper_mode(csv_dfs)
    vacuum_count, magnetic_count, ur_count, eop_count = (
        get_trigger_counts(csv_dfs) if has_pick_trigger else (None, None, None, None)
    )
    vacuum_success, magnetic_success, ur_success, eop_success = (
        get_trigger_success_counts(csv_dfs) if has_pick_trigger else (None, None, None, None)
    )

    vel, acc = get_vel_acc(csv_dfs)

    hours = get_total_hours(csv_dfs)

    average_pick_time = get_average_pick_time(csv_dfs)

    row = [
        basename,
        start_date,
        start_time,
        end_date,
        end_time,
        mode,
        pick_attempts,
        float(success) / float(pick_attempts),
        success,
        fails,
        float(vacuum_count) / float(pick_attempts),
        float(magnetic_count) / float(pick_attempts),
        float(ur_count) / float(pick_attempts),
        float(eop_count) / float(pick_attempts),
        vacuum_count,
        magnetic_count,
        ur_count,
        eop_count,
        float(vacuum_success) / float(vacuum_count) if vacuum_count else 0,
        float(magnetic_success) / float(magnetic_count) if magnetic_count else 0,
        float(ur_success) / float(ur_count) if ur_count else 0,
        float(eop_success) / float(eop_count) if eop_count else 0,
        vel,
        acc,
        total_lockouts,
        total_picks,
        total_picks / hours,
        average_pick_time,
    ]
    return row


def get_start_dates(csv_dfs):
    csv = csv_dfs["pre_pick_process_states"]
    date = str(csv["pick_start_date"][0])
    time = str(csv["pick_start_time"][0]).zfill(6)
    date_obj = datetime.strptime(date, "%Y%m%d")
    time_obj = datetime.strptime(time, "%H%M%S")

    date_reformatted = date_obj.strftime("%b-%d")
    time_reformatted = time_obj.strftime("%H:%M")

    return date_reformatted, time_reformatted


def get_end_dates(csv_dfs):
    csv = csv_dfs["post_pick_process_states"]
    num = len(csv["index"]) - 1
    date = str(object=csv["pick_end_date"][num])
    time = str(csv["pick_end_time"][num]).zfill(6)
    date_obj = datetime.strptime(date, "%Y%m%d")
    time_obj = datetime.strptime(time, "%H%M%S")

    date_reformatted = date_obj.strftime("%b-%d")
    time_reformatted = time_obj.strftime("%H:%M")

    return date_reformatted, time_reformatted


def get_total_hours(csv_dfs):
    csv_start = csv_dfs["pre_pick_process_states"]
    date_start = str(csv_start["pick_start_date"][0])
    time_start = str(csv_start["pick_start_time"][0])
    start_date_obj = datetime.strptime(date_start + time_start, "%Y%m%d%H%M%S")

    csv_end = csv_dfs["post_pick_process_states"]
    num = len(csv_end["index"]) - 1
    date_end = str(csv_end["pick_end_date"][num])
    time_end = str(csv_end["pick_end_time"][num])
    end_date_obj = datetime.strptime(date_end + time_end, "%Y%m%d%H%M%S")

    return (end_date_obj - start_date_obj).total_seconds() / 3600.0


def get_pick_counts(csv_dfs):
    csv = csv_dfs["pick_execution"]
    counts = csv["is_successful_pick"].value_counts()
    successful = counts[True] if True in counts.keys() else 0
    failed_picks = counts[False] if False in counts.keys() else 0
    return successful, failed_picks


def get_average_pick_time(csv_dfs):
    csv = csv_dfs["pick_execution"]
    return csv.loc[:, "pick_execution_time"].mean()


def get_gripper_mode(csv_dfs):
    csv = csv_dfs["mode_selection"]
    return csv["gripper_mode_num"][0]


def get_trigger_counts(csv_dfs):
    csv = csv_dfs["pick_execution"]
    counts = csv["pick_activation"].value_counts()
    vacuum = counts["Vacuum"] if "Vacuum" in counts.keys() else 0
    magnetic = counts["Magnetic Sensor"] if "Magnetic Sensor" in counts.keys() else 0
    ur = counts["UR"] if "UR" in counts.keys() else 0
    eop = counts["End of Path"] if "End of Path" in counts.keys() else 0

    return vacuum, magnetic, ur, eop


def get_trigger_success_counts(csv_dfs):
    csv = csv_dfs["pick_execution"]
    vacuum = csv[
        (csv["pick_activation"] == "Vacuum") & (csv["is_successful_pick"] == True)
    ].count()["is_successful_pick"]
    magnetic = csv[
        (csv["pick_activation"] == "Magnetic") & (csv["is_successful_pick"] == True)
    ].count()["is_successful_pick"]
    ur = csv[(csv["pick_activation"] == "UR") & (csv["is_successful_pick"] == True)].count()[
        "is_successful_pick"
    ]
    eop = csv[
        (csv["pick_activation"] == "End of Path") & (csv["is_successful_pick"] == True)
    ].count()["is_successful_pick"]

    return vacuum, magnetic, ur, eop


def get_vel_acc(csv_dfs):
    csv = csv_dfs["path_planner"]
    vel = csv["pose_path_2_above_drop_bin_vel"][0]
    acc = csv["pose_path_2_above_drop_bin_acc"][0]
    return vel, acc


def get_num_lockouts(text_path):
    if not os.path.exists(text_path):
        return None

    with open(text_path, "r") as f:
        num_lines = len(f.readlines())

    return num_lines
