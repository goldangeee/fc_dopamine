# mongodb.py

import os
import django

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pymongo import MongoClient
from django.conf import settings

# MongoDB 클라이언트 생성
client = MongoClient(
    host=settings.MONGODB_SETTINGS['host'],
    port=settings.MONGODB_SETTINGS['port'],
    username=settings.MONGODB_SETTINGS.get('username'),
    password=settings.MONGODB_SETTINGS.get('password')
)

# 데이터베이스 선택
db = client[settings.MONGODB_SETTINGS['db']]

# 데이터 삽입 예제
db.my_collection.insert_one({"테스트키": "테스트밸류"})

# 데이터 조회 예제
documents = db.my_collection.find()
for doc in documents:
    print(doc)
