# df 관련 import
import pandas as pd
import numpy as np

# 머신 러닝 관련 import
from sklearn.model_selection import train_test_split #df 나누기
from sklearn.tree import DecisionTreeClassifier #트리
from sklearn.ensemble import RandomForestClassifier #랜덤포레스트
from sklearn.pipeline import make_pipeline #파이프라인
from xgboost import XGBClassifier #xgboost
from lightgbm import LGBMClassifier #lgbm
from sklearn.metrics import f1_score #평가

# 저장 관련 import
import joblib

# df 불러오기
df = pd.read_csv('df.csv')

# 분류형 문제로 풀기 위해 df 변형
bins = [0,5,9]
labels = [0, 1]
# 등수 1~4는 0(승리), 5~8은 1(패배)로 지정
cuts = pd.cut(df['rank'], bins, labels=labels)
df['target'] = cuts
#원래 rank 제거
df = df.drop(['rank'], axis=1)

# lgbm 에러 제거를 위한 컬럼명 변경
df.columns = df.columns.str.replace(pat=r'[^A-Za-z0-9]', repl=r' ', regex=True)

# 생긴 기타 열 제거
df = df.iloc[:, 1:]

#머신러닝을 위한 분류
target = 'target'
features = df.drop(columns=[target]).columns
#train, test
train,test = train_test_split(df, stratify=df[target], random_state=2)
#train, val
train, val = train_test_split(train, stratify=train[target],random_state=2)

X_train = train[features]
y_train = train[target]
X_val = val[features]
y_val = val[target]
X_test = test[features]
y_test = test[target]

# 기준 모델 설정
Base_model = y_val.mode()
Base_pred = [Base_model] * len(y_val)

# 결정나무 학습
Tree = DecisionTreeClassifier(random_state=2)
Tree.fit(X_train, y_train)
Tree_pred = Tree.predict(X_val)

# 랜덤 포레스트 학습
RF = RandomForestClassifier(random_state=2, n_jobs=-1, oob_score=True)
RF.fit(X_train, y_train)
RF_pred = RF.predict(X_val)

# XGBoost 학습
XGB = XGBClassifier(eval_metric='mlogloss')
XGB.fit(X_train, y_train)
XGB_pred = XGB.predict(X_val)

# LGBM 학습
LGBM = LGBMClassifier()
LGBM.fit(X_train, y_train)
LGBM_pred = LGBM.predict(X_val)

# 평가하기
print("기준 모델 평가 : ", f1_score(y_val, Base_pred))
print("Decision Tree 모델 평가 : ", f1_score(y_val, Tree_pred))
print("Random Forest 모델 평가 : ", f1_score(y_val, RF_pred))
print("XGBoost 모델 평가 : ", f1_score(y_val, XGB_pred))
print("LGBM 모델 평가 : ", f1_score(y_val, LGBM_pred))

#제일 점수 높았던 lgbm 모델 저장
joblib.dump(LGBM, './knn_model.pkl')