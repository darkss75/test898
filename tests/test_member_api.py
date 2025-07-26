import pytest
from datetime import datetime
from fastapi.testclient import TestClient

def test_create_member(client: TestClient):
    member_data = {
        "name": "홍길동",
        "phone_number": "010-1234-5678",
        "start_date": "2023-01-01T00:00:00",
        "end_date": "2023-12-31T23:59:59"
    }
    
    response = client.post("/api/v1/members/", json=member_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "홍길동"
    assert data["phone_number"] == "010-1234-5678"
    assert "id" in data

def test_create_member_invalid_phone(client: TestClient):
    member_data = {
        "name": "홍길동",
        "phone_number": "010-12345-678",  # 잘못된 형식
        "start_date": "2023-01-01T00:00:00"
    }
    
    response = client.post("/api/v1/members/", json=member_data)
    assert response.status_code == 422

def test_create_member_duplicate_phone(client: TestClient):
    member_data = {
        "name": "홍길동",
        "phone_number": "010-1234-5678",
        "start_date": "2023-01-01T00:00:00"
    }
    
    # 첫 번째 회원 생성
    response = client.post("/api/v1/members/", json=member_data)
    assert response.status_code == 200
    
    # 같은 전화번호로 두 번째 회원 생성 시도
    response = client.post("/api/v1/members/", json=member_data)
    assert response.status_code == 400

def test_get_members(client: TestClient):
    # 회원 2명 생성
    member1 = {
        "name": "홍길동",
        "phone_number": "010-1234-5678",
        "start_date": "2023-01-01T00:00:00"
    }
    member2 = {
        "name": "김철수",
        "phone_number": "010-8765-4321",
        "start_date": "2023-02-01T00:00:00"
    }
    
    client.post("/api/v1/members/", json=member1)
    client.post("/api/v1/members/", json=member2)
    
    # 회원 목록 조회
    response = client.get("/api/v1/members/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2

def test_get_member_by_id(client: TestClient):
    member_data = {
        "name": "홍길동",
        "phone_number": "010-1234-5678",
        "start_date": "2023-01-01T00:00:00"
    }
    
    # 회원 생성
    response = client.post("/api/v1/members/", json=member_data)
    member_id = response.json()["id"]
    
    # 특정 회원 조회
    response = client.get(f"/api/v1/members/{member_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "홍길동"
    assert data["id"] == member_id

def test_get_member_not_found(client: TestClient):
    response = client.get("/api/v1/members/999")
    assert response.status_code == 404

def test_update_member(client: TestClient):
    member_data = {
        "name": "홍길동",
        "phone_number": "010-1234-5678",
        "start_date": "2023-01-01T00:00:00"
    }
    
    # 회원 생성
    response = client.post("/api/v1/members/", json=member_data)
    member_id = response.json()["id"]
    
    # 회원 정보 수정
    update_data = {"name": "홍길동수정"}
    response = client.put(f"/api/v1/members/{member_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "홍길동수정"
    assert data["phone_number"] == "010-1234-5678"  # 변경되지 않은 필드

def test_update_member_not_found(client: TestClient):
    update_data = {"name": "홍길동"}
    response = client.put("/api/v1/members/999", json=update_data)
    assert response.status_code == 404

def test_delete_member(client: TestClient):
    member_data = {
        "name": "홍길동",
        "phone_number": "010-1234-5678",
        "start_date": "2023-01-01T00:00:00"
    }
    
    # 회원 생성
    response = client.post("/api/v1/members/", json=member_data)
    member_id = response.json()["id"]
    
    # 회원 삭제
    response = client.delete(f"/api/v1/members/{member_id}")
    assert response.status_code == 200
    
    # 삭제된 회원 조회 시도
    response = client.get(f"/api/v1/members/{member_id}")
    assert response.status_code == 404

def test_delete_member_not_found(client: TestClient):
    response = client.delete("/api/v1/members/999")
    assert response.status_code == 404