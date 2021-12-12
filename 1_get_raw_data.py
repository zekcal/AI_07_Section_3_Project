# tfttactics 정보 가져오기 관련 import
import requests
import json
# mongodb 관련 import
from pymongo import MongoClient

# api와 id 정보
api_key = 'RGAPI-5046e6fe-ae96-49e6-b3e4-44093d14f15c'
game_id = '바마카타' #일단 내 아이디로 집어넣기

# id 정보 가져와서 puuid 확보 함수
def get_id():
    ID_URL = f'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/{game_id}?api_key={api_key}'
    puuid = requests.get(ID_URL).json()['puuid']
    return puuid

# puuid 활용해서 매치 리스트 확보 함수
def get_matchlist(puuid):
    MATCHID_URL = f'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=50&api_key={api_key}'
    parsed_matchid = requests.get(MATCHID_URL).json()
    return parsed_matchid

# mongodb 준비
HOST = 'tft.siirq.mongodb.net'
USER = 'dbuser'
PASSWORD = 'dbuser'
DATABASE_NAME = 'MyFirstDatabase'
COLLECTION_NAME = 'TFT'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]
collecton = database[COLLECTION_NAME]

# 매치 리스트를 활용해서 db 저장 함수
def making_raw_db(matchlist):
    for match_list in matchlist:
        RESULT_URL = f'https://asia.api.riotgames.com/tft/match/v1/matches/{match_list}?api_key={api_key}'
        raw_result = requests.get(RESULT_URL).json()
        collecton.insert_one(raw_result)

# db에 들어갈 data 늘리기 위해 같이 한 사람 id 확보 /너무 많은 data 확보 바라지 않아 1판 기준으로 함수 작성
def get_others_id(matchid):
    RESULT_URL = f'https://asia.api.riotgames.com/tft/match/v1/matches/{matchid}?api_key={api_key}'
    raw_result = requests.get(RESULT_URL).json()
    get_others_id = raw_result["metadata"]["participants"]
    return get_others_id

# 기본 db 만들기
making_raw_db(get_matchlist(get_id()))

# 같이 한 사람 db 만들기
matchid = 'KR_5570547882' #하나 무작위로 선정
others_id = get_others_id(matchid)
for others in others_id:
    making_raw_db(get_matchlist(others))