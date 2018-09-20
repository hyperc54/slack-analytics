#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 23:27:02 2018

Utils

@author: pierre
"""

import datetime as dt

def get_range_dates(start_d, nb_days):
    """
    Output lists of days in Ymd format.
    List has nb_days consecutive days starting from start_d
    """
    d_list = []
    date_current = dt.datetime.strptime(start_d, "%Y%m%d")
    d_list.append(date_current.strftime("%Y%m%d"))
    
    for i in range(nb_days):
        date_current = date_current + dt.timedelta(days=1)
        d_list.append(date_current.strftime("%Y%m%d"))

    return d_list