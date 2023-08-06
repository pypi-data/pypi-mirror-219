#!/usr/bin/env Python
# coding=utf-8
# @Time : 2023/6/15 18:00
# @Author : ZhangYan
# @File : get_data.py
import os
import time
from typing import List

import pandas as pd
from datetime import datetime

from sj_tool.fjsp.erp_next.constant import unlock_str, lock_str
from sj_tool.fjsp.erp_next.util import select_data_from_table, connect_erp_db


"""
销售订单表：tabSales Order
销售订单物料(产品)表：tabSales Order Item
客户表：tabCustomer
BOM表：tabBOM
BOM下层物料表：tabBOM Item
替换料表：tabItem Alternative
物料表：tabItem
物料采购记录表：tabPurchase Order
物料采购明细表：tabPurchase Order Item
物料出库记录表：tabDelivery Note
物料出库明细表：tabDelivery Note Item
停机记录表：tabDowntime Entry

"""


def transfer_sale_order(conn, owner="Administrator", **kwargs):
    print("同步销售订单相关表数据。。。")
    st = time.perf_counter()
    # 销售订单表
    table_sale = "tabSales Order"
    # 销售订单物料(产品)表
    table_sale_item = "tabSales Order Item"
    # 客户表
    table_sale_customer = "tabCustomer"

    # 客户表
    customers = select_data_from_table(
        conn,
        table_sale_customer,
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    customer_dict = {}
    for customer in customers:
        customer_dict[customer["name"]] = {
            "name": customer["customer_name"],
            "geo": customer["territory"],
            "segment": customer["segment"],
        }

    lock_status = lock_str if kwargs.get("lock", False) else unlock_str
    # 销售订单
    sale_orders = select_data_from_table(conn, table_sale, columns=["name", "customer"])
    # 销售订单明细
    sale_items_dict = select_data_from_table(
        conn,
        table_sale_item,
        columns=[
            "name",
            "item_code",
            "qty",
            "transaction_date",
            "delivery_date",
            "priority",
            "priority_type",
            "brand",  # 品牌
            "ots_sla",  # 生产提前期
            "amount",  # 金额
            "derived_net_revenue",  # 预期收益
            "brand_map",  # 品牌大类
            "parent",  # 关联父表
            "process_file_num",  # 工艺文件
        ],
        where_clause=f"owner = %s and locked = %s and docstatus = %s",
        where_params=(owner, lock_status, 1),
        to_dict=True,
        dict_key="parent",
    )

    results = []
    for sale_order in sale_orders:
        sale_order_id = sale_order["name"]

        sale_items = sale_items_dict[sale_order_id] if sale_order_id in sale_items_dict else []
        for item in sale_items:
            results.append(
                {
                    "customer": sale_order["customer"],
                    "sales_order": sale_order_id,
                    "sales_line": item["name"],
                    "demand_order_id": f"{sale_order_id}-{item['name']}",
                    "part_number": item["item_code"],
                    "part_quantity": item["qty"],
                    "ORDER_ENTRY": item["transaction_date"].strftime("%Y-%m-%d %H:%M:%S"),
                    "RSD": item["delivery_date"].strftime("%Y-%m-%d") + " 23:59:59",
                    "COUNTRY": customer_dict.get(sale_order["customer"], {"geo": "China"})["geo"],
                    "priority": item["priority"],
                    "PriorityType": item["priority_type"],
                    "BRAND": item["brand"],
                    "OTS_SLA": item["ots_sla"],
                    "NETPR": item["amount"],
                    "SEGMENT": customer_dict[sale_order["customer"]]["segment"]
                    if sale_order["customer"] in customer_dict
                    else "None",
                    "derived_net_revenue": item["derived_net_revenue"],
                    "brand_map": item["brand_map"],
                    "process_file_num": item["process_file_num"],
                }
            )
    df = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "demand_order.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # df.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"sale_order": df}


def transfer_bom(conn, owner="Administrator", **kwargs):
    print("同步BOM表和替换料表数据。。。")
    st = time.perf_counter()
    table_bom = "tabBOM"
    table_bom_next_level_item = "tabBOM Item"
    table_alternative = "tabItem Alternative"

    boms = select_data_from_table(
        conn,
        table_bom,
        columns=["item", "name", "process_file_num"],
        where_clause=f"owner = %s and docstatus = %s",
        where_params=(owner, 1),
    )
    bom_children_dict = select_data_from_table(
        conn,
        table_bom_next_level_item,
        columns=["item_code", "qty_consumed_per_unit", "parent","operation", "sub_qty"],
        where_clause=f"owner = %s and docstatus = %s",
        where_params=(owner, 1),
        to_dict=True,
        dict_key="parent",
    )

    # BOM中间表
    result_bom = []
    for bom in boms:
        children = bom_children_dict[bom["name"]] if bom["name"] in bom_children_dict else []
        for child in children:
            result_bom.append(
                {
                    "bom_name": bom["item"],
                    "consumed_item_name": child["item_code"],
                    "consumed_quantity": child["qty_consumed_per_unit"],
                    "process_file_num": bom["process_file_num"],
                    "operation_number": child["operation"],
                    "sub_unit": child["sub_qty"]
                }
            )

    # 替换料中间表
    rows = select_data_from_table(
        conn,
        table_alternative,
        columns=["parent_item", "item_code", "alternative_item_code", "qty", "priority", "two_way"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    result_alternative = []
    for row in rows:
        result_alternative.append(
            {
                "bom_name": row["parent_item"],
                # 被替换物料
                "consumed_item_name": row["item_code"],
                # 替换物料
                "substitute_item": row["alternative_item_code"],
                # 替换单位所需数量
                "consumed_quantity": row["qty"],
                # 替换优先级
                "priority": row["priority"],
            }
        )
        if row["two_way"] == 1:
            result_alternative.append(
                {
                    "bom_name": row["parent_item"],
                    # 被替换物料
                    "consumed_item_name": row["alternative_item_code"],
                    # 替换物料
                    "substitute_item": row["item_code"],
                    # 替换单位所需数量
                    "consumed_quantity": row["qty"],
                    # 替换优先级
                    "priority": row["priority"],
                }
            )

    # filename = os.path.join(get_project_root(), "output", "bom.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    df_bom = pd.DataFrame(result_bom)
    # df_bom.to_csv(filename, index=False)

    # filename = os.path.join(get_project_root(), "output", "bom_alternative.csv")
    bom_alternative = pd.DataFrame(result_alternative)
    # df_bom.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"bom": df_bom, "bom_alter": bom_alternative}


def transfer_inventory_old(conn, owner="Administrator", **kwargs):
    print("同步物料库存数据。。。")
    st = time.perf_counter()
    # 物料表
    table_item = "tabItem"
    # 采购 -> 采购订单
    tab_purchase_order = "tabPurchase Order"
    # 采购 -> 采购订单明细 (net_amount: 采购总成本， base_net_rate: 单价, qty: 采购数量, item_code: 物料编码,
    # schedule_date: 需求日期/预计到料日期, status: 状态(含有To Receive表示未入库), received_qty: 已经入库数量)
    tab_purchase_order_item = "tabPurchase Order Item"
    # 出库记录
    tab_out = "tabDelivery Note"
    # 出库明细
    tab_out_item = "tabDelivery Note Item"

    # 物料及期初库存
    inventory_data = select_data_from_table(
        conn,
        table_item,
        columns=["item_code", "opening_stock"],
        where_clause=f"owner = %s",
        where_params=(owner,),
        to_dict=True,
        dict_key="item_code",
    )
    # 采购订单（在途入库）
    purchase_data = select_data_from_table(
        conn,
        tab_purchase_order_item,
        columns=["item_code", "item_name", "qty", "received_qty", "schedule_date"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    # 出库
    out_records = select_data_from_table(
        conn,
        tab_out,
        columns=["name", "posting_date"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    out_data_detail = select_data_from_table(
        conn,
        tab_out_item,
        columns=["item_code", "item_name", "qty", "parent"],
        where_clause=f"owner = %s",
        where_params=(owner,),
        to_dict=True,
        dict_key="parent",
    )

    # {物料编号:{出库日期:数量}}
    out_inventory = {}
    for record in out_records:
        for item in out_data_detail[record["name"]]:
            item_code = item["item_code"]
            date = record["posting_date"]
            if item_code not in out_inventory:
                out_inventory[item_code] = {date: item["qty"]}
            elif date not in out_inventory[item_code]:
                out_inventory[item_code][date] = item["qty"]
            else:
                out_inventory[item_code][date] += item["qty"]

    # {物料编号:数量}
    on_hand_inventory = {item_code: value[0]["opening_stock"] for item_code, value in inventory_data.items()}
    # {物料编号:{入库日期:数量}}
    in_transit_inventory = {item_code: {} for item_code, _ in inventory_data.items()}

    # codes_only_in_transit = []
    # 根据物料的出入库记录，计算出当前时刻的库存情况
    for item in purchase_data:
        date = item["schedule_date"]
        # 添加入库
        if item["item_code"] not in on_hand_inventory:
            on_hand_inventory[item["item_code"]] = 0
        on_hand_inventory[item["item_code"]] += item["received_qty"]

        # 在途
        if item["item_code"] not in in_transit_inventory:
            in_transit_inventory[item["item_code"]] = {}
            # codes_only_in_transit.append(item['item_code'])
        if date not in in_transit_inventory[item["item_code"]]:
            in_transit_inventory[item["item_code"]][date] = 0
        in_transit_inventory[item["item_code"]][date] += item["qty"] - item["received_qty"]
    # 出库扣减
    for item_code, value in out_inventory.items():
        if item_code not in on_hand_inventory:
            on_hand_inventory[item_code] = 0
        for out_date, qty in value.items():
            on_hand_inventory[item_code] -= qty

    result_on_hand = []
    curr_d = datetime.now().strftime("%Y-%m-%d")
    for part_number, part_quantity in on_hand_inventory.items():
        result_on_hand.append({"part_number": part_number, "part_quantity": part_quantity, "arrival_time": curr_d})

    result_in_transit = []
    for part_number, value in in_transit_inventory.items():
        # if len(value) > 0:
        for arrival_time, part_quantity in value.items():
            result_in_transit.append(
                {"part_number": part_number, "part_quantity": part_quantity, "arrival_time": arrival_time}
            )

    # filename = os.path.join(get_project_root(), "output", "inventory_on_hand.csv")
    df_inventory_on_hand = pd.DataFrame(result_on_hand)

    # filename = os.path.join(get_project_root(), "output", "inventory_in_transit.csv")
    df_inventory_in_transit = pd.DataFrame(result_in_transit)

    df_inventory = pd.concat([df_inventory_on_hand, df_inventory_in_transit], axis=0)
    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    # print(f'codes_only_in_transit: {codes_only_in_transit}')
    # df_only_in_transit = pd.DataFrame([{'item_code':code} for code in codes_only_in_transit])
    # df_only_in_transit.to_excel('补充物料.xlsx',index=False)
    # return {"on_hand_inv": df_inventory_on_hand, "in_transit_inv": df_inventory_in_transit, "merged_inv": df_inventory}
    return {"inv": df_inventory}


def transfer_inventory(conn, owner="Administrator", **kwargs):
    print("同步物料库存数据。。。")
    st = time.perf_counter()
    # 物料表
    table_item = "tabItem"
    # 采购 -> 采购订单
    tab_purchase_order = "tabPurchase Order"
    # 采购 -> 采购订单明细 (net_amount: 采购总成本， base_net_rate: 单价, qty: 采购数量, item_code: 物料编码,
    # schedule_date: 需求日期/预计到料日期, status: 状态(含有To Receive表示未入库), received_qty: 已经入库数量)
    tab_purchase_order_item = "tabPurchase Order Item"
    # 出库记录
    tab_out = "tabDelivery Note"
    # 出库明细
    tab_out_item = "tabDelivery Note Item"

    # 物料及期初库存
    # inventory_data = select_data_from_table(
    #     conn,
    #     table_item,
    #     columns=["item_code", "opening_stock",'lock_qty'],
    #     where_clause=f"owner = %s",
    #     where_params=(owner,),
    #     to_dict=True,
    #     dict_key="item_code",
    # )
    # 采购订单（在途入库）
    purchase_data = select_data_from_table(
        conn,
        tab_purchase_order_item,
        columns=["item_code", "item_name", "qty", "schedule_date", "lock_qty"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )

    # 出库
    out_records = select_data_from_table(
        conn,
        tab_out,
        columns=["name", "posting_date"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    out_data_detail = select_data_from_table(
        conn,
        tab_out_item,
        columns=["item_code", "item_name", "qty", "parent"],
        where_clause=f"owner = %s",
        where_params=(owner,),
        to_dict=True,
        dict_key="parent",
    )

    # {物料编号:{出库日期:数量}}
    out_inventory = {}
    for record in out_records:
        for item in out_data_detail[record["name"]]:
            item_code = item["item_code"]
            date = record["posting_date"]
            if item_code not in out_inventory:
                out_inventory[item_code] = {date: item["qty"]}
            elif date not in out_inventory[item_code]:
                out_inventory[item_code][date] = item["qty"]
            else:
                out_inventory[item_code][date] += item["qty"]

    # {物料编号:数量}
    on_hand_inventory = {}
    # {物料编号:{入库日期:数量}}
    in_transit_inventory = {}

    curr_d = datetime.now()
    curr_d_str = curr_d.strftime("%Y-%m-%d")
    # 根据物料的出入库记录，计算出当前时刻的库存情况
    for item in purchase_data:
        date = item["schedule_date"]

        if pd.to_datetime(date) <= curr_d:
            # 在手
            if item["item_code"] not in on_hand_inventory:
                on_hand_inventory[item["item_code"]] = 0
            on_hand_inventory[item["item_code"]] += item["qty"] - item["lock_qty"]
        else:
            # 在途
            if item["item_code"] not in in_transit_inventory:
                in_transit_inventory[item["item_code"]] = {}
                # codes_only_in_transit.append(item['item_code'])
            if date not in in_transit_inventory[item["item_code"]]:
                in_transit_inventory[item["item_code"]][date] = 0
            in_transit_inventory[item["item_code"]][date] += item["qty"] - item["lock_qty"]
    # 出库扣减
    for item_code, value in out_inventory.items():
        if item_code not in on_hand_inventory:
            on_hand_inventory[item_code] = 0
        for out_date, qty in value.items():
            on_hand_inventory[item_code] -= qty

    result_on_hand = []
    for part_number, part_quantity in on_hand_inventory.items():
        result_on_hand.append({"part_number": part_number, "part_quantity": part_quantity, "arrival_time": curr_d_str})

    result_in_transit = []
    for part_number, value in in_transit_inventory.items():
        # if len(value) > 0:
        for arrival_time, part_quantity in value.items():
            result_in_transit.append(
                {"part_number": part_number, "part_quantity": part_quantity, "arrival_time": arrival_time}
            )

    # filename = os.path.join(get_project_root(), "output", "inventory_on_hand.csv")
    df_inventory_on_hand = pd.DataFrame(result_on_hand)

    # filename = os.path.join(get_project_root(), "output", "inventory_in_transit.csv")
    df_inventory_in_transit = pd.DataFrame(result_in_transit)

    df_inventory = pd.concat([df_inventory_on_hand, df_inventory_in_transit], axis=0)
    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    # print(f'codes_only_in_transit: {codes_only_in_transit}')
    # df_only_in_transit = pd.DataFrame([{'item_code':code} for code in codes_only_in_transit])
    # df_only_in_transit.to_excel('补充物料.xlsx',index=False)
    # return {"on_hand_inv": df_inventory_on_hand, "in_transit_inv": df_inventory_in_transit, "merged_inv": df_inventory}
    return {"inv": df_inventory}


def transfer_wip(conn, owner="Administrator", **kwargs):
    print("同步在制库存数据。。。")
    st = time.perf_counter()
    table_wip = "tabWIP"

    wip_data = select_data_from_table(
        conn, table_wip, columns=["mo", "so", "unfinished_qty"], where_clause=f"owner = %s", where_params=(owner,)
    )
    results = []
    for row in wip_data:
        results.append(
            {"produced_order": row["mo"], "consumed_order": row["so"], "unfinished_qty": row["unfinished_qty"]}
        )

    # filename = os.path.join(get_project_root(), "output", "wip.csv")
    wip = pd.DataFrame(results)
    # df_bom.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"wip": wip}


def transfer_process_table(conn, owner="Administrator", **kwargs):
    table_process = "tabOperation"

    process_table = select_data_from_table(
        conn, table_process, columns=["operation_number", "name", "operation_name"], where_clause=f"owner = %s", where_params=(owner,)
    )
    results = []
    for row in process_table:
        results.append({"id": row["operation_number"], "name": row["operation_name"]})

    df_process = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "process.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # df_process.to_csv(filename, index=False)
    return {"process": df_process}


def transfer_machine_table(conn, owner="Administrator", **kwargs):
    table_machine = "tabWorkstation"
    machine_table = select_data_from_table(
        conn, table_machine, columns=["workstation_id", "workstation_name"], where_clause=f"owner = %s", where_params=(owner,)
    )

    results = []
    for row in machine_table:
        results.append({"id": row["workstation_id"], "name": row["workstation_name"]})

    df_machine = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "machine.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # df_machine.to_csv(filename, index=False)
    return {"machine": df_machine}


# 设备停运
def transfer_machine_stop(conn, owner="Administrator", **kwargs):
    table_downtime = "tabDowntime Entry"
    downtime_data = select_data_from_table(
        conn,
        table_downtime,
        columns=["workstation", "from_time", "to_time", "downtime"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )


def transfer_prod_process_table(conn, owner="Administrator", **kwargs):
    print("同步产品-工艺表")
    st = time.perf_counter()
    table_prod_process = "tabProd process"
    machine_table = select_data_from_table(
        conn,
        table_prod_process,
        columns=["item_code", "operation_number", "pre_operation", "next_operation", "input_bom", "output_bom"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )

    results = []

    for row in machine_table:
        results.append(
            {
                "product_id": row["item_code"],
                "process_id": row["operation_number"],
                "pre_process_id": row["pre_operation"],
                "next_process_id": row["next_operation"],
                "input_bom": row["input_bom"],
                "output_bom": row["output_bom"],
            }
        )

    prod_process = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "prod_process.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # df_machine.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"prod_process": prod_process}


def transfer_standing_table(conn, owner="Administrator", **kwargs):
    print("同步静置时间表")
    st = time.perf_counter()
    table_prod_process = "tabProd process"
    standing_table = select_data_from_table(
        conn,
        table_prod_process,
        columns=["item_code", "operation_number", "standing_time"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )

    results = []

    for row in standing_table:
        results.append(
            {
                "product_id": row["item_code"],
                "process_id": row["operation_number"],
                "standing_time(s)": row["standing_time"],
            }
        )

    df_standing_time = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "standing_time.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # df_standing_time.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"standing": df_standing_time}


def transfer_changeover_table(conn, owner="Administrator", **kwargs):
    print("同步换型时间表")
    st = time.perf_counter()
    table_prod_process = "tabchangeover"
    changeover_table = select_data_from_table(
        conn,
        table_prod_process,
        columns=["workstation_id", "pre_brand", "pre_process", "post_brand", "post_process", "changeover"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )

    results = []

    for row in changeover_table:
        results.append(
            {
                "machine_id": row["workstation_id"],
                "pre_model": row["pre_brand"],
                "pre_process_id": row["pre_process"],
                "post_model": row["post_brand"],
                "post_process_id": row["post_process"],
                "changeover(s)": row["changeover"],
            }
        )

    changeover_table = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "changeover.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # changeover_table.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"changeover": changeover_table}


def tansfer_processtime_table(conn, owner="Administrator", **kwargs):
    print("同步设备生产时间")
    st = time.perf_counter()
    table_prod_process = "tabProcess Time"
    processtime_table = select_data_from_table(
        conn,
        table_prod_process,
        columns=["item_code", "workstation_name", "operation", "process_time", "unit"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )

    results = []

    for row in processtime_table:
        results.append(
            {
                "product_id": row["item_code"],
                "process_id": row["operation"],
                "machine_id": row["workstation_name"],
                "process_time(s)": row["process_time"],
                "unit": row["unit"],
            }
        )

    processtime_table = pd.DataFrame(results)
    # filename = os.path.join(get_project_root(), "output", "prod_prs_machine.csv")
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # processtime_table.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"process_time": processtime_table}


def transfer_products(conn, owner="Administrator", **kwargs):
    print("同步产品表数据。。。")
    st = time.perf_counter()

    product_ids = kwargs.get("product_ids", None)

    if product_ids is None:
        where_clause = f"owner = %s"
        where_params = (owner,)
    else:
        where_clause = f"owner = %s and item_code in %s"
        where_params = (owner, product_ids)

    table_item = "tabItem"
    data = select_data_from_table(
        conn,
        table_item,
        columns=["item_code", "item_name", "model"],
        where_clause=where_clause,
        where_params=where_params,
    )
    results = []
    for item in data:
        results.append({"id": item["item_code"], "name": item["item_name"], "model": item["model"]})
    # filename = os.path.join(get_project_root(), "output", "product.csv")
    df_bom = pd.DataFrame(results)
    # df_bom.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"product": df_bom}


def transfer_calendar(conn, owner="Administrator", **kwargs):
    print("同步设备日历数据。。。")
    st = time.perf_counter()

    table_item = "tabWorkstation Working Hour"
    data = select_data_from_table(
        conn,
        table_item,
        columns=["parent", "start_date", "end_date", "shift"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    results = []
    for item in data:
        for date in pd.date_range(item["start_date"], item["end_date"]):
            results.append({"machine_id": item["parent"], "date": date.strftime("%Y-%m-%d"), "shift": item["shift"]})
    # filename = os.path.join(get_project_root(), "output", "product.csv")
    df_bom = pd.DataFrame(results)
    # df_bom.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"calendar": df_bom}


def transfer_shift(conn, owner="Administrator", **kwargs):
    print("同步班制数据。。。")
    st = time.perf_counter()

    table_item = "tabShift Item"
    data = select_data_from_table(
        conn,
        table_item,
        columns=["parent", "start_time", "end_time"],
        where_clause=f"owner = %s",
        where_params=(owner,),
    )
    results = []
    for item in data:
        results.append({"shift": item["parent"], "start_time": item["start_time"], "end_time": item["end_time"]})
    # filename = os.path.join(get_project_root(), "output", "product.csv")
    df_bom = pd.DataFrame(results)
    # df_bom.to_csv(filename, index=False)

    et = time.perf_counter()
    print(f"消耗时间: {round(et - st, 3)} s")
    return {"shift": df_bom}


def get_data(owner, need_data_list: List[str], **kwargs):
    """
    :param owner：用户邮箱
    :param need_data_list：需要获取的所有数据名的列表，[key1, key2, ...]，key需要在key_dict中
    return result_dict: {key: df}
    """
    key_dict = {
        "machine": transfer_machine_table,
        "standing": transfer_standing_table,
        "changeover": transfer_changeover_table,
        "process_time": tansfer_processtime_table,
        "sale_order": transfer_sale_order,
        "bom": transfer_bom,
        "process": transfer_process_table,
        "prod_process": transfer_prod_process_table,
        "inventory": transfer_inventory,
        "wip": transfer_wip,
        "product": transfer_products,
        "calendar": transfer_calendar,
        "shift": transfer_shift,
    }
    result_dict = {}
    conn = connect_erp_db()
    for k in need_data_list:
        if k in key_dict:
            result_dict.update(key_dict[k](conn, owner, **kwargs))
    conn.close()
    return result_dict


if __name__ == "__main__":
    result = get_data(
        "1091076149@qq.com",
        list(
            {
                "machine": transfer_machine_table,
                "standing": transfer_standing_table,
                "changeover": transfer_changeover_table,
                "process_time": tansfer_processtime_table,
                "sale_order": transfer_sale_order,
                "bom": transfer_bom,
                "process": transfer_process_table,
                "prod_process": transfer_prod_process_table,
                "inventory": transfer_inventory,
                "wip": transfer_wip,
                "product": transfer_products,
                "calendar": transfer_calendar,
                "shift": transfer_shift,
            }.keys()
        ),
    )
    print(1)
