import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from pymongo import MongoClient

def save_html_to_file(url, filename="output.html"):
    """주어진 URL의 HTML 내용을 파일로 저장하는 함수."""
    url = "https://fconline.nexon.com/datacenter/PlayerList"

    player_name = "로랑 블랑"

    # POST 요청에 포함할 데이터 설정
    payload = {
        "strPlayerName": player_name,
    }

    # POST 요청 보내기
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"HTML 내용이 {filename} 파일에 저장되었습니다.")
    else:
        print("HTML을 가져오는 데 실패했습니다.", response.status_code)

def crawl_player_data(request):
    url = "https://fconline.nexon.com/datacenter/PlayerList"

    # 검색할 선수 이름
    name = "호날두"

    # POST 요청에 포함할 데이터 설정
    payload = {
        "n1Strong" : "5,6,7",
        "strSeason" : ",825,826,821,814,",
        "strPlayerName": name,
        # "n4OvrMax" : 102,
    }

    # POST 요청 보내기
    response = requests.post(url, data=payload)

    # 응답 상태 코드 확인
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch data"}, status=500)

    # 응답 내용을 BeautifulSoup으로 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # MongoDB 연결 설정
    client = MongoClient('mongodb://localhost:27017/')  # MongoDB 연결 문자열
    db = client['dopamine1']  # 데이터베이스 이름
    collection = db['crawled_data']  # 컬렉션 이름

    # 선수 정보 추출 (선수 이름과 가치)
    players = []
    for player in soup.select('.tr'):  # 선수 정보가 포함된 행 선택
        name_element = player.select_one('.name')  # 선수 이름이 포함된 클래스 선택
        bp_element = player.select_one('.td_ar_bp')  # 선수 가치(BP)가 포함된 클래스 선택

        # 요소가 존재할 경우에만 추가
        if name_element and bp_element:
            name = name_element.text.strip()  # 선수 이름

            # BP 값을 가져오기 (alt 속성 사용)
            bp_value = bp_element.find('span', {'class': 'span_bp5'})  # bp강화등급
            if bp_value:
                bp = bp_value['alt']  # alt 속성에서 BP 값 가져오기
            else:
                bp = "N/A"  # BP 값이 없을 경우

            # 선수 정보를 MongoDB에 저장
            player_data = {
                "name": name,
                # 시즌
                # 강화등급
                "value": bp  # 선수 가치(BP)
            }
            players.append(player_data)
            collection.update_one({"name": name}, {"$set": player_data}, upsert=True)  # 데이터 업데이트

    # 결과를 JSON 형식으로 반환
    return JsonResponse(players, safe=False)
