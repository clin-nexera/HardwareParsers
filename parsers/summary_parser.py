from datetime import datetime

def summarize_folder(has_pick_trigger, basename, csv_dfs):
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
    return row

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
    successful = counts[True] if True in counts.keys() else 0
    failed_picks = counts[False] if False in counts.keys() else 0
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
