#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from typing import Union

TimeType = Union[str, bytes, time.struct_time, float, int]


class TimeUtil(object):
    DATETIME_FORMAT_CHINESE = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_ENGLISH = '%b %d, %Y %I:%M:%S %p'
    _DATETIME_FORMATS = [DATETIME_FORMAT_CHINESE, DATETIME_FORMAT_ENGLISH]

    @staticmethod
    def format_time(time_src: TimeType) -> time.struct_time:
        time_formatted = None

        # decode bytes to str if necessary
        if isinstance(time_src, bytes):
            time_src = time_src.decode()

        if isinstance(time_src, str):
            first_match: bool = True
            for f in TimeUtil._DATETIME_FORMATS:
                try:
                    time_formatted = time.strptime(time_src, f)

                    if not first_match:
                        # move the matched item to first to speeding up matching
                        TimeUtil._DATETIME_FORMATS.remove(f)
                        TimeUtil._DATETIME_FORMATS.insert(0, f)
                    break
                except ValueError:
                    first_match = False

            if time_formatted is None:
                print('unknown format: %s' % time_src)
                raise ValueError('unknown format: %s' % time_src)
        elif isinstance(time_src, time.struct_time):
            time_formatted = time_src
        elif isinstance(time_src, float):
            time_formatted = time.localtime(time_src)
        elif isinstance(time_src, int):  # treat int as float
            time_formatted = time.localtime(time_src)

        # return time
        return time_formatted

    @staticmethod
    def format_time_to_str(time_src: TimeType, date_format: str = DATETIME_FORMAT_ENGLISH) -> str:
        return time.strftime(date_format, TimeUtil.format_time(time_src))

    @staticmethod
    def format_time_to_float(time_src: TimeType) -> float:
        return time.mktime(TimeUtil.format_time(time_src))

    @staticmethod
    def format_time_to_int(time_src: TimeType) -> int:
        return int(time.mktime(TimeUtil.format_time(time_src)))

    @staticmethod
    def current_time() -> time.struct_time:
        return time.localtime()

    @staticmethod
    def time_add(time_src, add: TimeType) -> time.struct_time:
        t = TimeUtil.format_time_to_float(time_src)
        a = TimeUtil.format_time_to_float(add)
        return TimeUtil.format_time(t + a)

    @staticmethod
    def time_sub(time_src, sub: TimeType) -> time.struct_time:
        t = TimeUtil.format_time_to_float(time_src)
        s = TimeUtil.format_time_to_float(sub)
        return TimeUtil.format_time(t - s)
