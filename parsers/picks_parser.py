HEADERS = [
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


### FUNCTIONS ###
def aggregate_pick_data(csv_dfs):
    data = [[HEADERS]]
    pick_ids = get_all_pick_ids(csv_dfs)

    for idx, pick_id in enumerate(pick_ids):
        pick_id = pick_id
        pick_start_date = get_pick_start_date(csv_dfs, pick_id)
        pick_start_time = get_pick_start_time(csv_dfs, pick_id)
        capture_count = idx
        pick_attempts = get_pick_attempts(csv_dfs, pick_id)
        total_picks = get_total_picks(csv_dfs, pick_id)
        bin_region = get_bin_region(csv_dfs, pick_id)

        gen_source = get_gen_source(csv_dfs, pick_id)
        bin_empty = get_bin_empty(csv_dfs, pick_id)

        gripper_num = get_gripper_num(csv_dfs, pick_id)

        velocity = get_horizontal_vel(csv_dfs, pick_id)
        accerlation = get_horizontal_acc(csv_dfs, pick_id)

        pick_activation = get_pick_activation(csv_dfs, pick_id)
        is_successful = get_is_successful(csv_dfs, pick_id)
        pick_execution_time = get_pick_exec_time(csv_dfs, pick_id)

        pick_end_date = get_pick_end_date(csv_dfs, pick_id)
        pick_end_time = get_pick_end_time(csv_dfs, pick_id)

        row = [
            pick_id,
            pick_start_date,
            pick_start_time,
            capture_count,
            pick_attempts,
            total_picks,
            bin_region,
            gen_source,
            bin_empty,
            gripper_num,
            velocity,
            accerlation,
            pick_activation,
            is_successful,
            pick_execution_time,
            pick_end_date,
            pick_end_time
        ]

        data.append(row)

    return data


def get_all_pick_ids(csv_dfs):
    df = csv_dfs["pre_pick_process_states"]
    return list(_get_var(df, "index"))


def get_pick_start_time(csv_dfs, pick_id):
    return get_pre_pick_var_for_pick(csv_dfs, pick_id, "pick_start_time")


def get_pick_start_date(csv_dfs, pick_id):
    return get_pre_pick_var_for_pick(csv_dfs, pick_id, var_name="pick_start_date")


def get_pick_attempts(csv_dfs, pick_id):
    return get_pre_pick_var_for_pick(csv_dfs, pick_id, "pick_attempt_num")


def get_total_picks(csv_dfs, pick_id):
    return get_pre_pick_var_for_pick(csv_dfs, pick_id, "num_total_picks")


def get_bin_region(csv_dfs, pick_id):
    bin_region = get_pre_pick_var_for_pick(csv_dfs, pick_id, "pick_region_idx")
    if bin_region == 1:
        bin_region = "east"
    elif bin_region == 2:
        bin_region = "south"
    return bin_region


def get_gen_source(csv_dfs, pick_id):
    return get_pick_pose_var_for_pick(csv_dfs, pick_id, "generation_source")


def get_bin_empty(csv_dfs, pick_id):
    return get_pick_pose_var_for_pick(csv_dfs, pick_id, "is_bin_empty")


def get_horizontal_vel(csv_dfs, pick_id):
    return get_path_planner_var_for_pick(csv_dfs, pick_id, "pose_path_2_above_drop_bin_vel")


def get_horizontal_acc(csv_dfs, pick_id):
    return get_path_planner_var_for_pick(csv_dfs, pick_id, "pose_path_2_above_drop_bin_acc")


def get_gripper_num(csv_dfs, pick_id):
    return get_mode_sel_var_for_pick(csv_dfs, pick_id, "gripper_mode_num")


def get_is_successful(csv_dfs, pick_id):
    return get_pick_exec_var_for_pick(csv_dfs, pick_id, "is_successful_pick")


def get_pick_activation(csv_dfs, pick_id):
    return get_pick_exec_var_for_pick(csv_dfs, pick_id, "pick_activation")


def get_pick_exec_time(csv_dfs, pick_id):
    return get_pick_exec_var_for_pick(csv_dfs, pick_id, "pick_execution_time")


def get_pick_end_time(csv_dfs, pick_id):
    return get_post_pick_var_for_pick(csv_dfs, pick_id, "pick_end_time")


def get_pick_end_date(csv_dfs, pick_id):
    return get_post_pick_var_for_pick(csv_dfs, pick_id, "pick_end_date")


### HELPERS ###
def _get_row_at_pick_id(df, pick_id):
    return df[df["index"] == pick_id]


def _get_var(df, var_name):
    try:
        var = str(df[var_name])
    except:
        var = "N/A"

    return var


def _get_var_for_pick(df, pick_id, var_name):
    row = _get_row_at_pick_id(df, pick_id)
    if len(row) == 0:
        var = "DNR"
    else:
        var = _get_var(row, var_name)
    return var


def get_pre_pick_var_for_pick(csv_dfs, pick_id, var_name):
    df = csv_dfs["pre_pick_process_states"]
    return _get_var_for_pick(df, pick_id, var_name)


def get_pick_pose_var_for_pick(csv_dfs, pick_id, var_name):
    df = csv_dfs["pick_pose"]
    return _get_var_for_pick(df, pick_id, var_name)


def get_path_planner_var_for_pick(csv_dfs, pick_id, var_name):
    df = csv_dfs["path_planner"]
    return _get_var_for_pick(df, pick_id, var_name)


def get_mode_sel_var_for_pick(csv_dfs, pick_id, var_name):
    df = csv_dfs["mode_selection"]
    return _get_var_for_pick(df, pick_id, var_name)


def get_pick_exec_var_for_pick(csv_dfs, pick_id, var_name):
    df = csv_dfs["pick_execution"]
    return _get_var_for_pick(df, pick_id, var_name)


def get_post_pick_var_for_pick(csv_dfs, pick_id, var_name):
    df = csv_dfs["post_pick_process_states"]
    return _get_var_for_pick(df, pick_id, var_name)
