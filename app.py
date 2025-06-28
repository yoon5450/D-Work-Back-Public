from bson import ObjectId
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask.json.provider import JSONProvider
import json
import sys

# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

app = Flask(__name__)
client = MongoClient('mongodb://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST, 27017)
user_db = client.dwork
CORS(app)
KST = pytz.timezone('Asia/Seoul')

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)


app.json = CustomJSONProvider(app)

# 0.0.0.0 메인 렌더링
@app.route('/')
def home():
    return render_template('index.html')

# 회원가입
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if user_db.users.find_one({'username': username}):
        return jsonify({'result': 'failure', 'msg': '이미 존재하는 사용자입니다.'}), 400

    user_db.users.insert_one({'username': username, 'password': password})
    return jsonify({'result': 'success', 'msg': '회원가입 성공'}), 201

# 로그인
# 아 첨쓸때 snake_case 안써가지고 조졌네.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = user_db.users.find_one({'username': username, 'password': password})
    if user:
        return jsonify({'result': 'success', 'msg': '로그인 성공'}), 200
    else:
        return jsonify({'result': 'failure', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다'}), 401

# 메모 추가
# TODO: CUR
@app.route('/addmemo', methods=['POST'])
def add_memo():
    data = request.get_json()
    userName = data['username']
    memoTitle = data['memotitle']
    memoContents = data['memocontents']
    now = datetime.now(KST);
    memoTime = int(now.timestamp())

    user_db.memos.insert_one({
        'username': userName, 
        'title': memoTitle, 
        'memocontents': memoContents, 
        'writeTime': memoTime})
    
    return jsonify({'result': 'success', 'msg': '메모 성공'}), 201

# 유저 아이디로 조회한 전체 메모 조회
@app.route('/memos', methods=['POST'])
def get_user_memos():
    data = request.get_json()
    userName = data['username']
    memos = list(user_db.memos.find({'username': userName}, {'_id': 0}))
    return jsonify({'result': 'success', 'memos': memos}), 200

# 전체 공고 조회
@app.route('/postings', methods=['GET'])
def get_postings():
    postings = list(user_db.postings.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'postings': postings}), 200

# 북마크 추가
@app.route('/addbookmark', methods=['POST'])
def add_bookmark():
    data = request.get_json()
    username = data['username']
    posting_id = data['postingid']

    # 사용자 확인
    user = user_db.users.find_one({"username": username})
    if not user:
        return jsonify({'result': 'failure', 'msg': '사용자 없음'}), 404

    # 중복 확인
    existing = user_db.user_bookmarks.find_one({
        "username": username,
        "postingid": posting_id
    })
    if existing:
        return jsonify({'result': 'failure', 'msg': '이미 북마크한 공고입니다.'}), 400

    user_db.user_bookmarks.insert_one({
        "username": username,
        "postingid": posting_id,
        "createdAt": int(datetime.now(KST).timestamp())
    })

    return jsonify({'result': 'success'}), 200

# 유저 북마크 목록 조회
@app.route('/mybookmarks', methods=['POST'])
def get_user_bookmarks():
    data = request.get_json()
    username = data['username']

    # 사용자 확인
    user = user_db.users.find_one({"username": username})
    if not user:
        return jsonify({'result': 'failure', 'msg': '유저 없음'}), 404

    # 북마크된 postingid 목록만 추출
    bookmarks = user_db.user_bookmarks.find(
        {"username": username}, {"_id": 0, "postingid": 1}
    )
    
    bookmark_ids = [doc["postingid"] for doc in bookmarks]

    # 응답 형태 맞춰서 반환
    return jsonify({
        'result': 'success',
        'username': username,
        'bookmarklist': bookmark_ids
    }), 200


# 유저 북마크 삭제
@app.route('/removebookmark', methods=['POST'])
def remove_bookmark():
    try:
        data = request.get_json()

        username = data.get('username')
        posting_id = data.get('postingid')

        # 필수 필드 체크
        if not username or not posting_id:
            return jsonify({'result': 'failure', 'msg': 'username 또는 postingid 누락'}), 400

        # 삭제 요청
        result = user_db.user_bookmarks.delete_one({
            "username": username,
            "postingId": posting_id
        })

        if result.deleted_count == 0:
            return jsonify({'result': 'failure', 'msg': '북마크 내역 없음'}), 404

        return jsonify({'result': 'success', 'msg': '북마크 삭제 완료'}), 200

    except Exception as e:
        return jsonify({'result': 'failure', 'msg': f'서버 에러: {str(e)}'}), 500




if __name__ == '__main__':
   app.run('0.0.0.0',port=5000, debug=True)

