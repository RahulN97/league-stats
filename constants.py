import os

# Constants
API_KEY = os.environ.get('API_KEY')
ROOT_SUMMONER = 'Rahbiar'

# Strategies
STRATEGIES = {
    'championcombo'
}

# Riot Endpoints
URLS = {
    'champions': 'http://ddragon.leagueoflegends.com/cdn/10.12.1/data/en_US/champion.json',
    'summoner_dto': 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={API_KEY}',
    'match_history': 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{acct_id}?endIndex={end_index}&beginIndex={begin_index}&api_key={API_KEY}'
}
