#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 21:06:03 2018

This module gathers mutiple messages loading functions.

We output results in Pandas Dataframes

@author: pierre
"""

from slackclient import SlackClient

from functools import reduce
from itertools import product
import datetime as dt
import pandas as pd


#%%
class SlackMessagesLoader:
    
    def __init__(self, key):
        self.sc = SlackClient(key)
        
    def __get_chat_history_between_timestamps(self,
                                              channel_id,
                                              start_ts,
                                              end_ts):
        """
        Gets chat history from channel_id between two timestamps
        ASSUMES that all messages have been received in one query
        TODO : If not true, make multiple queries.
        """
        if channel_id:
            method = 'groups.history'
        else:
            method = 'channels.history'
        
        history = self.sc.api_call(method,
                              channel=channel_id,
                              count=1000,
                              latest=end_ts,
                              oldest=start_ts,
                              pretty=1)
        
        if 'messages' in history:
            return history['messages']
        else:
            return []
        
    def __get_chat_history_in_a_day(self, d, channel_id):
        date = dt.datetime.strptime(d, "%Y%m%d") # TODO make utils func
        ts = (date - dt.datetime(1970, 1, 1)).total_seconds()
        
        return self.__get_chat_history_between_timestamps(channel_id,
                                                          ts,
                                                          ts + 86400)
        
    def __get_user_info(self, user_id):
        """
        Calls Slack API to get one user_id info
        """
        return self.sc.api_call('users.info', user=user_id, pretty=1)
    
    def __get_df_user_from_uids(self, uid_list):
        """
        Constructs user dataframes from a list of requested UIDs
        For now we just want Ids and real names in the output df.
        TODO : Build Dataframe in place (there we just copy a dict)
        """
        COLUMNS_TO_KEEP = ['id', 'real_name']
        usernames = []
        for user_id in uid_list:
            record = self.__get_user_info(user_id)
            try:
                usernames.append(record['user'])
            except KeyError:
                print("No real name has been found for id {}".format(str(user_id)))
                
        return pd.DataFrame.from_records(usernames)[COLUMNS_TO_KEEP]
    
    
    def __get_df_logs_single(self, d, channel_id):
        """
        Public method to get logs from a single d and channel_id
        TODO : Build Dataframe in place (there we just copy a dict)
        """
        COLUMNS_TO_KEEP = ['text', 'ts', 'type', 'user', 'reactions']
        
        # Get records
        chat_records = self.__get_chat_history_in_a_day(d, channel_id)
        
        # Structure it
        df_log = pd.DataFrame.from_records(chat_records)
        
        if df_log.empty:
            print('It\'s empty there ! [{},{}]'.format(str(d), str(channel_id)))
            return df_log
        
        COLUMNS_TO_KEEP = [c for c in COLUMNS_TO_KEEP if c in df_log.columns]
        df_log = df_log[COLUMNS_TO_KEEP]
        
        # Add d & channel info
        df_log['d'] = d
        df_log['channel_id'] = channel_id
        
        return df_log    

    def __get_df_logs_multiple(self, d_list, channel_id_list):
        combinations = product(d_list, channel_id_list)
        return reduce(lambda a,b:a.append(b), [self.__get_df_logs_single(*c) for c in combinations])
    
    def __get_channel_ids_from_names(self, channel_names):
        list_chan = self.sc.api_call('channels.list')['channels']
        list_chan += self.sc.api_call('groups.list')['groups']
    
        return [c['id'] for c in list_chan if c['name'] in channel_names]
    
    def get_df_logs(self, days, channel_names):
        """
        Gets records structured as pandas dataframe for days from channel_id
        """
        channel_ids = self.__get_channel_ids_from_names(channel_names)
        
        df_log = self.__get_df_logs_multiple(days, channel_ids)
        
        # Add real username
        df_user = self.__get_df_user_from_uids(
                    df_log['user'].drop_duplicates().tolist()
                )
        df_log = pd.merge(df_log, df_user, how='inner', left_on='user', right_on='id')
        
        return df_log
    
    def get_who_i_am(self):
        return self.sc.api_call('auth.test', pretty=1)['user_id']

    def getx(self):
        return self.sc.api_call('groups.list')
