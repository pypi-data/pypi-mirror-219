import pandas as pd

from sj_tool.fjsp.entity.fjsp_pool import FjspPool
import os
import pickle
import json
from datetime import timedelta


def to_gantt_json(
    pool: FjspPool, save_folder: str, machine_rate: dict, sorted_dict={"加弹": 1, "整经": 2, "经编": 3, "剖绒": 4, "前整": 5}
):
    gantt_data = []
    i = 0
    max_day = max([op.op_end for op in pool.op_dict.values() if op.op_end])
    min_day = min([op.op_start for op in pool.op_dict.values() if op.op_start])
    for machine_id in sorted(
        pool.machine_dict.keys(),
        key=lambda x: (sorted_dict.get(pool.machine_dict[x].name[:2], 0), pool.machine_dict[x].name[-1]),
    ):
        machine_dict = {}
        machine_object = pool.machine_dict[machine_id]
        # 放入 machine 信息
        machine_dict["id"] = machine_id
        machine_dict["rawIndex"] = i
        machine_dict["machine_name"] = machine_object.name
        i += 1
        machine_dict["machine_time"] = machine_rate.get(machine_id, 0)
        machine_dict["rest_time"] = []
        capacity = (
            machine_object.original_calendar
            if hasattr(machine_object, "original_calendar")
            else machine_object.calendar
        )
        for d in pd.date_range(min_day, max_day):
            calendar = (
                capacity.get(d - timedelta(days=1), {}).get("c_list", [{"s_t": d - timedelta(days=1), "e_t": d}])[-1:]
                + capacity.get(d, {}).get("c_list", [{"s_t": d, "e_t": d + timedelta(days=1)}])
                + capacity.get(d + timedelta(days=1), {}).get(
                    "c_list", [{"s_t": d + timedelta(days=1), "e_t": d + timedelta(days=2)}]
                )[:1]
            )
            for idx, c in enumerate(calendar):
                if idx == 0:
                    continue
                s_t = calendar[idx - 1]["e_t"]
                e_t = calendar[idx]["s_t"]
                if e_t - s_t >= timedelta(seconds=2):
                    machine_dict["rest_time"].append(
                        {"start": s_t.strftime("%Y-%m-%d %H:%M:%S"), "end": e_t.strftime("%Y-%m-%d %H:%M:%S")}
                    )
        # 放入 operation 信息
        machine_dict["gtArray"] = []
        scheduled_op_id = machine_object.scheduled_ops
        for op_id in scheduled_op_id:
            op_object = pool.op_dict[op_id]
            machine_op_dict = {}
            machine_op_dict["process"] = pool.process_dict[op_object.process_id].name
            machine_op_dict["processId"] = op_object.process_id
            machine_op_dict["productId"] = op_object.product_id
            machine_op_dict["productSN"] = pool.product_dict[op_object.product_id].model
            machine_op_dict["count"] = pool.job_dict[op_object.job_id].demand
            machine_op_dict["start"] = op_object.op_start.strftime("%Y-%m-%d %H:%M:%S")
            machine_op_dict["end"] = op_object.op_end.strftime("%Y-%m-%d %H:%M:%S")
            machine_op_dict["Delivery"] = pool.job_dict[op_object.job_id].ots_time.strftime("%Y-%m-%d")
            machine_op_dict["operation_id"] = op_id
            machine_op_dict["job_id"] = pool.job_dict[op_object.job_id].id
            machine_op_dict["parentId"] = machine_object.id
            machine_op_dict["pre_ops"] = op_object.pre_ops

            machine_dict["gtArray"].append(machine_op_dict)

        gantt_data.append(machine_dict)

    with open(os.path.join(save_folder, "gantt.json"), "w", encoding="utf-8") as f:
        json.dump({"data": gantt_data}, f, ensure_ascii=False)


if __name__ == "__main__":
    save_folder = r"C:\Users\86178\Desktop\新建文件夹 (2)"
    with open(os.path.join(save_folder, "result.pkl"), "rb") as f:
        fjsppool = pickle.load(f)

    to_gantt_json(fjsppool, save_folder, {})
