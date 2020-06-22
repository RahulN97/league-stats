from resource_manager import RESOURCES
from . import check_resource


class MatchHistoryUtils:
    def __init__(self, summoner=None, account_id=None, match_id=None):
        self.summoner = summoner
        self.account_id = account_id


    @check_resource(resource='match_history')
    def get_participant_id_from_match(self):
        return ''


    @check_resource(resource='match_history')
    def get_team_id_from_participant(self):
        return ''


    @check_resource(resource='match_history')
    def get_result_from_team(self):
        return ''
