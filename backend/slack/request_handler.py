"""
This class gets request params and handles them
"""
from backend.slack.load_messages import SlackMessagesLoader
from backend.slack.simple_analytics import DataProcessor
from backend.slack.utils import get_range_dates

class GraphRequestHandler(object):
    def __init__(self):
        self.personal_slack_clients = {}

    def register_new_client(self, code, token):
        self.personal_slack_clients[code] = SlackMessagesLoader(token)

    def load_data(self, code, token_start, chan_name, nb_days):
        loader = self.personal_slack_clients[code]

        days_list = get_range_dates(token_start, nb_days)

        df = loader.get_df_logs(days_list, [chan_name])
        my_uid = loader.get_who_i_am()


        return df, my_uid


    def process_graphs_data(self, df, my_uid):
        return {
            'big_chatters': DataProcessor.get_simple_messages_count(df, ['real_name']),
            'personal_stats': DataProcessor.get_personal_stats(df, my_uid)
        }

    def handle_request(self, code, token_start, chan_name, nb_days):
        df, my_uid = self.load_data(code, token_start, chan_name, nb_days)
        graphs_data = self.process_graphs_data(df, my_uid)

        return graphs_data




