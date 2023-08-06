import os
import time
from typing import List, Union

import pandas as pd

from sj_tool.fjsp.erp_next.constant import lock_str, unlock_str
from sj_tool.fjsp.erp_next.util import connect_erp_db, get_http_header, update_table, select_data_from_table


def lock_unlock_sale_orders(order_ids: Union[str, List[str]], lock: bool, owner: str):
    if isinstance(order_ids, str):
        order_ids = [order_ids]

    conn = connect_erp_db()
    parent_order_ids = []
    sub_order_item_ids = []
    for order_item_id in order_ids:
        parent_order_ids.append(order_item_id[: order_item_id.rfind("-")])
        item_id = order_item_id[order_item_id.rfind("-") + 1 :]
        # update_table(conn, table_name, {"locked": 1 if lock else 0}, f"name='{item_id}'")
        sub_order_item_ids.append(item_id)

    parent_order_ids = str(parent_order_ids)[1:-1].replace("'", '"')
    sub_order_item_ids = str(sub_order_item_ids)[1:-1].replace("'", '"')
    # 更新销售订单明细表
    table_name = "tabSales Order Item"
    update_table(
        conn,
        table_name,
        {"locked": f"'{lock_str}'" if lock else f"'{unlock_str}'"},
        f"owner = '{owner}' and name in ({sub_order_item_ids})",
    )
    # 更新销售订单总表
    table_sale_order = "tabSales Order"
    update_table(
        conn,
        table_sale_order,
        {"locked": f"'{lock_str}'" if lock else f"'{unlock_str}'"},
        f"owner = '{owner}' and name in ({parent_order_ids})",
    )

    conn.close()


def lock_on_way_inv_by_df(df_material_result_merged, owner="1091076149@qq.com"):
    """
    锁定库存（在库和在途）
    :param df_material_result_merged: 按照[part_number, request_date, if_on_hand]合并后的物料方案
    :param owner: 数据所有者
    :return:
    """
    print("锁定库存")
    st = time.perf_counter()

    conn = connect_erp_db()
    table_name = "tabPurchase Order Item"
    fields = ["name", "item_code", "qty", "schedule_date", "lock_qty"]

    try:
        # 取物料
        part_numbers = df_material_result_merged["part_number"].unique().tolist()
        placeholders = ", ".join(["%s"] * len(part_numbers))
        query_data = select_data_from_table(
            conn,
            table_name,
            columns=fields,
            where_clause=f"owner = %s and item_code in ({placeholders})",
            where_params=(owner, *part_numbers),
        )
        df_db = pd.DataFrame(query_data)
        df_db["new_lock_qty"] = df_db["lock_qty"].copy(deep=True)

        # 逐个进行锁定
        for _, material_row in df_material_result_merged.iterrows():
            part_number = material_row["part_number"]
            lock_qty = material_row["part_quantity"]
            if_on_hand = material_row["if_on_hand"]
            request_date = material_row["request_date"]

            if if_on_hand:
                tmp_data = df_db[df_db["item_code"] == part_number]
            else:
                tmp_data = df_db[
                    (df_db["item_code"] == part_number)
                    & (df_db["schedule_date"] == pd.to_datetime(request_date).date())
                ]
            for idx, row in tmp_data.sort_values(by=["schedule_date"]).iterrows():
                if lock_qty == 0:
                    break
                qty = row["qty"]
                locked_qty = row["new_lock_qty"]
                tmp = min(qty - locked_qty, lock_qty)
                df_db.iat[idx, df_db.columns.get_loc("new_lock_qty")] = locked_qty + tmp
                # update_table(conn, table_name, {"lock_qty": tmp}, f"name='{idx}'")
                lock_qty -= tmp
            if lock_qty != 0:
                raise Exception(
                    part_number + " lock error, if_on_hand: " + str(if_on_hand) + ", error num: " + str(lock_qty)
                )

        # 更新数据库
        df_to_lock = df_db[df_db["lock_qty"] != df_db["new_lock_qty"]]
        for _, lock_row in df_to_lock.iterrows():
            update_table(conn, table_name, {"lock_qty": lock_row["new_lock_qty"]}, f"name='{lock_row['name']}'")
    finally:
        conn.close()
    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")


def lock_on_way_inv(part_number, lock_qty, if_on_hand, mad=None, owner="1091076149@qq.com"):
    """
    锁定库存，速度慢，暂时弃用
    :param part_number:
    :param lock_qty:
    :param if_on_hand:
    :param mad:
    :param owner:
    :return:
    """
    conn = connect_erp_db()
    table_name = "tabPurchase Order Item"
    fields = ["name", "item_code", "qty", "schedule_date", "lock_qty"]

    # 查询物料
    results = []
    try:
        # 查询物料
        tmp_data = select_data_from_table(
            conn,
            table_name,
            columns=fields,
            where_clause=f"owner = %s and item_code = %s"
            if if_on_hand
            else f"owner = %s and item_code = %s and schedule_date = %s",
            where_params=(owner, part_number) if if_on_hand else (owner, part_number, mad),
        )
        for row in tmp_data:
            results.append(
                {
                    "name": row["name"],
                    "item_code": row["item_code"],
                    "qty": row["qty"],
                    "schedule_date": row["schedule_date"],
                    "lock_qty": row["lock_qty"],
                }
            )
        results = pd.DataFrame(results)

        for idx, row in results.sort_values(by=["schedule_date"]).iterrows():
            if lock_qty == 0:
                break
            qty = row["qty"]
            # 表里已经锁定的数量
            locked_qty = row["lock_qty"]
            idx = row["name"]
            # 本次要锁的数量
            tmp = min(qty - locked_qty, lock_qty)
            update_table(conn, table_name, {"lock_qty": tmp + locked_qty}, f"name='{idx}'")
            lock_qty -= tmp
        if lock_qty != 0:
            raise Exception(
                part_number + " lock error, if_on_hand: " + str(if_on_hand) + ", error num: " + str(lock_qty)
            )
    except Exception as e:
        raise Exception(f"{part_number} lock error, if_on_hand: {if_on_hand}, query_length: {len(results)}")
    finally:
        conn.close()


if __name__ == "__main__":
    order_ids = ["fp_SIZE_4400451300_L420-000010-0a69ac4ef1", "fp_SIZE_4312305275_L420-000001-c6f609f95d"]
    lock_unlock_sale_orders(order_ids, True, owner="1091076149@qq.com")
    # lock_on_way_inv("SD10M34154", 5000, True)

    from sj_tool.util import get_root_dir

    # df_material_result = pd.read_csv(os.path.join(get_root_dir(), "examples", "data", "20230703143734.csv"))
    # df_material_result = df_material_result[["part_number", "request_date", "if_on_hand", "part_quantity"]]
    # df_material_result_merged = df_material_result.groupby(
    #     by=["part_number", "request_date", "if_on_hand"], as_index=False, sort=False
    # ).agg(sum)
    # lock_on_way_inv_by_df(df_material_result_merged)
