from constants import URLS
from modules.strategy import Strategy
from resource_manager import RESOURCES


class ChampionCombo(Strategy):
    def __init__(self, root_summoner, games=100):
        super().__init__(root_summoner)
        self.games = games


    def execute(self):
        result = f'{self.acct_id}\n{RESOURCES["champion_cache"]["141"]}\n\n{len(RESOURCES["match_history"])}'
        self.write(type(self).__name__, result)
