from typing import Union

import pandas as pd


class BaseJob(object):
    def __init__(
        self,
        job_id: Union[int, str],
        product_id: Union[int, str],
        mad: Union[str, int],
        ots_time: Union[str, int],
        demand: Union[int, float],
    ):
        """

        :param job_id:
        :param product_id: 产品编码
        :param mad: job到达时间，即最早可开始时间
        :param ots_time: 截止时间
        :param demand: 需求量
        """
        self.id = job_id
        self.product_id = product_id
        self.mad = pd.to_datetime(mad) if isinstance(mad, str) else mad
        self.ots_time = pd.to_datetime(ots_time) if isinstance(ots_time, str) else ots_time
        self.demand = demand
        self.start_operations = []
        self.operations = []

        self.job_start = None
        self.job_end = None
