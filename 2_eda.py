# mongodb 관련 import
from pymongo import MongoClient
# df 관련 import
import pandas as pd

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

# mongodb에서 가져오기
raw_df = collecton.find()

# df 제작에 쓰일 특성 리스트
traits_list = ['Set6_Academy', 'Set6_Arcanist', 'Set6_Assassin', 'Set6_Bodyguard', 'Set6_Bruiser', 'Set6_Challenger', 'Set6_Chemtech', 'Set6_Colossus', 'Set6_Clockwork', 'Set6_Cuddly', 'Set6_Enchanter', 'Set6_Enforcer', 'Set6_Glutton', 'Set6_Imperial', 'Set6_Innovator', 'Set6_Mercenary', 'Set6_Mutant', 'Set6_Protector', 'Set6_Scholar', 'Set6_Scrap', 'Set6_Sister', 'Set6_Sniper', 'Set6_Socialite', 'Set6_Syndicate', 'Set6_Transformer', 'Set6_Twinshot', 'Set6_Yordle']

# df 만들기
## 기본 : 깊게 안들어간 딕셔너리
df_base = {'rank' : [], 'gold_left' : [], 'traits_count' : [], 'total_damage_to_players' : [], 'Set6_Academy':[], 'Set6_Arcanist':[], 'Set6_Assassin':[], 'Set6_Bodyguard':[], 'Set6_Bruiser':[], 'Set6_Challenger':[], 'Set6_Chemtech':[], 'Set6_Colossus':[], 'Set6_Clockwork':[], 'Set6_Cuddly':[], 'Set6_Enchanter':[], 'Set6_Enforcer':[], 'Set6_Glutton':[], 'Set6_Imperial':[], 'Set6_Innovator':[], 'Set6_Mercenary':[], 'Set6_Mutant':[], 'Set6_Protector':[], 'Set6_Scholar':[], 'Set6_Scrap':[], 'Set6_Sister':[], 'Set6_Sniper':[], 'Set6_Socialite':[], 'Set6_Syndicate':[], 'Set6_Transformer':[], 'Set6_Twinshot':[], 'Set6_Yordle':[]}
df_base = pd.DataFrame(df_base)
for i in raw_df:
    for n in range(8):
        rank = i['info']['participants'][n]['placement']
        gold_left = i['info']['participants'][n]['gold_left']
        traits_count = len(i['info']['participants'][n]['traits'])
        total_damage_to_players = i['info']['participants'][n]['total_damage_to_players']
        
        temp_list = {'rank' : rank, 'gold_left' : gold_left, 'traits_count' : traits_count, 'total_damage_to_players' : total_damage_to_players}

## 특성 가졌을 경우, 특성 수준 추가
        temp_dic = {}
        for l in range(traits_count):
            for traits in traits_list:
                if traits == i['info']['participants'][n]['traits'][l]['name']:
                    temp_dic[traits] = i['info']['participants'][n]['traits'][l]['tier_current']

        df_base = df_base.append({**temp_list, **temp_dic}, ignore_index=True)
        temp_dic = {}

# 결측치 0으로 채우기
df = df_base.fillna(0)

# #숫자형으로 모두 바꾸기
df = df.astype(int)

# #로컬에 파일 저장하기
print(df)
df.to_csv('df.csv')