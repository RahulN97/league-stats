from . import check_resource
from resource_manager import RESOURCES


class MatchHistoryUtils:
    def __init__(self, summoner=None):
        self.summoner = summoner


    @check_resource(resource='match_history')
    def get_match_result(self, match_id):
        return ''


    @check_resource(resource='match_history')
    def get_ally_summoner_names(self, match_id):
        return ''
