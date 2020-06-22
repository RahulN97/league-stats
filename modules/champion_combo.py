from constants import URLS
from utils.match_history_utils import MatchHistoryUtils
from modules.strategy import Strategy
from resource_manager import RESOURCES


class ChampionCombo(Strategy):
    def __init__(self, root_summoner, history_size):
        super().__init__(root_summoner)
        self.history_size = history_size
        self.history_utils = MatchHistoryUtils(root_summoner)


    def execute(self):
        # result2 = f'{self.acct_id}\n{RESOURCES["champion_cache"]["141"]}\n\n{len(RESOURCES["match_history"])}'
        # result = self.history_utils.get_participant_id_from_match()
        self.write(type(self).__name__, '')
