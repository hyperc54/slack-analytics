#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 23:42:45 2018

This module gathers some chat dataframe log processing

@author: pierre
"""
#%%
import re
import datetime as dt
import pandas as pd

class DataProcessor(object):

    @classmethod
    def count_occ_pattern(cls, text, pattern):
        return len(re.findall(pattern, text))

    @classmethod
    def count_occurences_pattern_in_messages(cls, df_logs, agg_fields, pattern):
        df_logs['nb_occ_pattern'] = df_logs['text'].apply(lambda x:count_occ_pattern(x,pattern))
        df_logs = df_logs.groupby(agg_fields, as_index=False).agg({'nb_occ_pattern':'sum'})
        return df_logs

    @classmethod
    def get_personal_stats(cls, df_logs, uid):
        """
        Gets number of messages and number of words for a specific uid within df_logs
        """
        df_logs = df_logs[df_logs['id'] == uid]
        df_logs['nb_words'] = df_logs['text'].apply(lambda text:len(text.split(' ')))

        return {
            'number_messages': int(df_logs['id'].count()),
            'number_words': int(df_logs['nb_words'].sum())
        }

    @classmethod
    def get_simple_messages_count(cls, df_logs, agg_fields):
        df_logs['count'] = 1
        df_grouped_logs = df_logs.groupby(agg_fields)[['count']].count()['count']

        return pd.to_numeric(df_grouped_logs).to_dict()

    @classmethod
    def get_hour_from_ts(cls, ts):
        date = dt.datetime.fromtimestamp(float(ts))
        return date.strftime('%H')

    @classmethod
    def get_messages_counts_by_hour(cls, df_logs, agg_fields):
        df_logs['h'] = df_logs['ts'].apply(cls.get_hour_from_ts)

        return cls.get_simple_messages_count(df_logs, agg_fields + ['h'])
