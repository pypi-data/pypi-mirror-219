import copy
import os
import pickle
from datetime import timedelta, datetime
from typing import Callable
import time

import pandas as pd
import copy
from sj_tool.fjsp.entity.fjsp_pool import FjspPool
from sj_tool.fjsp.entity.job import BaseJob
from sj_tool.fjsp.entity.machine import BaseMachine
from sj_tool.fjsp.entity.operation import BaseOperation
from sj_tool.fjsp.entity.product import BaseProduct
from sj_tool.fjsp.entity.process import BaseProcess
from sj_tool.fjsp.entity.changeover import Changeover
from sj_tool.fjsp.entity.standing_time import StandingTime


def build_pool_from_file(
    data_dir: str,
    plan_start_date: str,
    df_atb: pd.DataFrame,
    MachineClass=BaseMachine,
    ProcessClass=BaseProcess,
    ProductClass=BaseProduct,
    JobClass=BaseJob,
    OperationClass=BaseOperation,
    PoolClass=FjspPool,
):
    """
    根据标准文件构建FJSP问题的标准数据结构
    :param MachineClass:
    :param data_dir:
    :return:
    """
    df_machine = pd.read_csv(os.path.join(data_dir, "machine.csv"))
    df_product = pd.read_csv(os.path.join(data_dir, "product.csv"))
    df_process = pd.read_csv(os.path.join(data_dir, "process.csv"))
    df_standing_time = pd.read_csv(os.path.join(data_dir, "standing_time.csv"))
    df_product_process_machine = pd.read_csv(os.path.join(data_dir, "prod_prs_machine.csv"))
    df_changeover = pd.read_csv(os.path.join(data_dir, "changeover.csv"))
    df_product_process = pd.read_csv(os.path.join(data_dir, "prod_process.csv"))
    df_calendar = pd.read_csv(os.path.join(data_dir, "calendar.csv"))
    df_shift = pd.read_csv(os.path.join(data_dir, "shift.csv"))

    df_process["id"] = df_process["id"].astype("str")
    df_standing_time["process_id"] = df_standing_time["process_id"].astype("str")
    df_product_process_machine["process_id"] = df_product_process_machine["process_id"].astype("str")

    # df_machine["id"] = df_machine["id"].apply(lambda x: f"m-{x}")
    # df_product_process_machine["machine_id"] = df_product_process_machine["machine_id"].apply(lambda x: f"m-{x}")
    # df_calendar["machine_id"] = df_calendar["machine_id"].apply(lambda x: f"m-{x}")
    # df_changeover["machine_id"] = df_changeover["machine_id"].apply(lambda x: f"m-{x}")
    # df_machine.to_csv(os.path.join(data_dir, "machine.csv"), index=False)
    # df_product_process_machine.to_csv(os.path.join(data_dir, "prod_prs_machine.csv"), index=False)
    # df_calendar.to_csv(os.path.join(data_dir, "calendar.csv"), index=False)
    # df_changeover.to_csv(os.path.join(data_dir, "changeover.csv"), index=False)

    return build_from_df(
        df_machine,
        df_product,
        df_process,
        df_standing_time,
        df_product_process_machine,
        df_changeover,
        df_product_process,
        df_atb,
        df_calendar,
        df_shift,
        plan_start_date,
        MachineClass=MachineClass,
        ProcessClass=ProcessClass,
        ProductClass=ProductClass,
        JobClass=JobClass,
        OperationClass=OperationClass,
        PoolClass=PoolClass,
    )


def process_shift(df_shift):
    shift_dict = {}
    for ind, row in df_shift.iterrows():
        shift_type = row["shift"]
        # start_time_str = row["start_time"]
        # end_time_str = row["end_time"]
        start_time = row["start_time"]
        end_time = row["end_time"]
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M").time()
            start_time = timedelta(hours=start_time.hour, minutes=start_time.minute)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M").time()
            end_time = timedelta(hours=end_time.hour, minutes=end_time.minute)
        end_time = timedelta(seconds=end_time.seconds)
        start_time = timedelta(seconds=start_time.seconds)
        if end_time <= start_time:
            end_time += timedelta(hours=24)
        shift_length = end_time - start_time
        if shift_type not in shift_dict:
            shift_dict[shift_type] = {
                "c_list": [{"s_t": start_time, "e_t": end_time, "shift": shift_length}],
                "shift": shift_length,
            }
        else:
            shift_dict[shift_type]["shift"] += shift_length
            shift_dict[shift_type]["c_list"].append({"s_t": start_time, "e_t": end_time, "shift": shift_length})
    return shift_dict


def build_from_df(
    df_machine,
    df_product,
    df_process,
    df_standing_time,
    df_product_process_machine,
    df_changeover: pd.DataFrame,
    df_product_op: pd.DataFrame,
    df_job: pd.DataFrame,
    df_calendar: pd.DataFrame,
    df_shift: pd.DataFrame,
    plan_start_date: str,
    MachineClass=BaseMachine,
    ProcessClass=BaseProcess,
    ProductClass=BaseProduct,
    JobClass=BaseJob,
    OperationClass=BaseOperation,
    PoolClass=FjspPool,
):
    pool = PoolClass()

    # 处理班制基础信息
    t1 = time.time()
    shift_dict = process_shift(df_shift)
    t2 = time.time()
    print("班制处理", t2 - t1)
    # 获取 job 涉及的 产品
    related_product = df_job["prodCode"].unique().tolist()
    df_product = df_product[df_product["id"].isin(related_product)]
    df_product_op = df_product_op[df_product_op["product_id"].isin(related_product)]
    df_product_process_machine = df_product_process_machine[
        df_product_process_machine["product_id"].isin(related_product)
    ]
    df_standing_time = df_standing_time[df_standing_time["product_id"].isin(related_product)]

    t1 = time.time()
    # 1. 处理机器 machine
    for index, row in df_machine.iterrows():
        unit_times = {}
        df_machine_speed = df_product_process_machine[df_product_process_machine["machine_id"] == row["id"]]
        for index2, row2 in df_machine_speed.iterrows():
            unit_times[(row2["product_id"], row2["process_id"])] = row2["process_time(s)"]
        machine = MachineClass(idx=row["id"], name=row["name"], unit_times=unit_times)
        pool.machine_dict[row["id"]] = machine
    t2 = time.time()
    print("设备", t2 - t1)
    # 为机器加入日历
    t1 = time.time()
    for ind, row in df_calendar.iterrows():
        machine_id = row["machine_id"]
        shift_type = row["shift"]
        date = row["date"]
        shift = copy.deepcopy(shift_dict[shift_type])
        for item in shift["c_list"]:
            # item["s_t"] = pd.to_datetime(f"{date} {item['s_t']}")
            # item["e_t"] = pd.to_datetime(f"{date} {item['e_t']}")
            item["s_t"] = pd.to_datetime((pd.to_datetime(date) + item["s_t"]).strftime("%Y-%m-%d %H:%M:%S"))
            item["e_t"] = pd.to_datetime((pd.to_datetime(date) + item["e_t"]).strftime("%Y-%m-%d %H:%M:%S"))
        pool.machine_dict[machine_id].calendar[pd.to_datetime(date)] = shift
    t2 = time.time()
    print("设备日历添加", t2 - t1)
    # 2. 处理产品 product
    t1 = time.time()
    for index, row in df_product.iterrows():
        pool.product_dict[row["id"]] = ProductClass(row["id"], row["name"], row["model"])
    t2 = time.time()
    print("产品", t2 - t1)

    # 3. 处理工序 process
    t1 = time.time()
    for index, row in df_process.iterrows():
        pool.process_dict[row["id"]] = ProcessClass(row["id"], row["name"])
    t2 = time.time()
    print("工序", t2 - t1)

    # 4. 处理静置时间 standing time
    t1 = time.time()
    pool.standing_time = StandingTime()
    for index, row in df_standing_time.iterrows():
        pool.standing_time.add(row["product_id"], row["process_id"], row["standing_time(s)"])
    t2 = time.time()
    print("静置", t2 - t1)

    # 5. 处理换型时间 changeover
    t1 = time.time()
    pool.changeover = Changeover()
    for index, row in df_changeover.iterrows():
        pool.changeover.add(
            row["pre_model"],
            row["pre_process_id"],
            row["post_model"],
            row["post_process_id"],
            row["machine_id"],
            row["changeover(s)"],
        )
    t2 = time.time()
    print("换型", t2 - t1)

    # 6. 构建每个产品的工艺路线
    t1 = time.time()
    df_product_op_group = df_product_op.groupby("product_id")
    for product_id, df_group in df_product_op_group:
        if isinstance(product_id, tuple):
            product_id = product_id[0]
        op_dict = {}
        op_ind = 0
        operations = {}
        pre_op_dict = {}
        next_op_dict = {}
        df_group.sort_values("process_id", key=lambda x: x.astype(int), inplace=True)
        for index, row in df_group.iterrows():
            op_ind += 1
            cur_process = str(row["process_id"])
            pre_processes = str(row["pre_process_id"])
            next_processes = str(row["next_process_id"])
            # 将含有多个process的情况转为list
            if "," in pre_processes:
                pre_processes = pre_processes.split(",")
            else:
                pre_processes = [pre_processes]
            if "," in next_processes:
                next_processes = next_processes.split(",")
            else:
                next_processes = [next_processes]

            op_dict[op_ind] = {}
            op_dict[op_ind]["pre"] = pre_processes
            op_dict[op_ind]["cur"] = cur_process
            op_dict[op_ind]["next"] = next_processes
            operations[op_ind] = OperationClass(op_ind, "", str(product_id), -1, cur_process, {}, [], [])

        for cur_op_id, cur_op in operations.items():
            cur_info_dict = op_dict[cur_op_id]
            for other_op_ind, other_info_dict in op_dict.items():
                # 如果工序在当前工序的前置工序列表中，并且工序的后置工序列表包含当前工序
                if other_info_dict["cur"] in cur_info_dict["pre"] and cur_info_dict["cur"] in other_info_dict["next"]:
                    cur_op.pre_ops.append(other_op_ind)
                    operations[other_op_ind].next_ops.append(cur_op.id)
                    pre_op_dict.setdefault(cur_op_id, []).append(other_op_ind)
                    next_op_dict.setdefault(other_op_ind, []).append(cur_op.id)

            # 添加虚拟头和尾
            if cur_info_dict["pre"][0] == "0":
                next_op_dict.setdefault(0, []).append(cur_op.id)
                pre_op_dict[cur_op.id] = [0]
            if cur_info_dict["next"][0] == "-1":
                pre_op_dict.setdefault(-1, []).append(cur_op.id)
                next_op_dict[cur_op.id] = [-1]

        # product = ProductClass("1", "1", "1")
        # product.operations = operations
        # product.pre_op_dict = pre_op_dict
        # product.next_op_dict = next_op_dict
        # pool.product_dict[str(product_id)] = product

        pool.product_dict[product_id].operations = operations
        pool.product_dict[product_id].pre_op_dict = pre_op_dict
        pool.product_dict[product_id].next_op_dict = next_op_dict
    t2 = time.time()
    print("产品工艺路径", t2 - t1)

    # 处理订单和对应 opeteration
    t1 = time.time()
    for index, row in df_job.iterrows():
        pool.job_dict[row["worderID"]] = JobClass(
            job_id=row["worderID"],
            product_id=row["prodCode"],
            arrival_time=row["orderTime"],
            ots_time=(pd.to_datetime(row["deliveryTime"]) + timedelta(days=1)).strftime("%Y-%m-%d"),
            demand=row["prodCount"],
        )
        process_ops = copy.deepcopy(pool.product_dict[row["prodCode"]].operations)
        for op in process_ops.values():
            op_id = "{}-{}".format(row["worderID"], op.id)
            df_machine_op = df_product_process_machine[
                (df_product_process_machine["product_id"] == row["prodCode"])
                & (df_product_process_machine["process_id"] == op.process_id)
            ]
            machine_times = dict(zip(df_machine_op["machine_id"], row["prodCount"] * df_machine_op["process_time(s)"]))
            op.id = op_id
            op.model = pool.product_dict[row["prodCode"]].model
            op.demand = row["prodCount"]
            op.job_id = row["worderID"]
            op.mad = row["MAD"]
            op.ots_time = (pd.to_datetime(row["deliveryTime"]) + timedelta(days=1)).strftime("%Y-%m-%d")
            op.process_id = op.process_id
            op.pre_ops = ["{}-{}".format(row["worderID"], x) for x in op.pre_ops]
            op.next_ops = ["{}-{}".format(row["worderID"], x) for x in op.next_ops]
            op.machine_times = machine_times
            op.available_machines = list(machine_times.keys())
            # 更新 Basemachine 中的 available_ops
            for machine_id in op.available_machines:
                pool.machine_dict[machine_id].available_ops.append(op.id)

            # 添加到 job
            pool.op_dict[op_id] = op
            pool.job_dict[row["worderID"]].operations.append(op_id)
            if len(op.pre_ops) == 0:
                pool.job_dict[row["worderID"]].start_operations.append(op_id)
    t2 = time.time()
    print("job&op", t2 - t1)

    # 加上 排程开始时间
    pool.plan_start_date = plan_start_date

    return pool


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    plan_start_date = "2023-05-01"
    df_atb = pd.read_csv(os.path.join(data_dir, "job.csv"))
    pool = build_pool_from_file(data_dir, plan_start_date, df_atb)
    print(1)
