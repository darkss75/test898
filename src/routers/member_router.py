from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import database
from ..models import member
from ..schemas import member_schema

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/members/", response_model=member_schema.MemberResponse)
def create_member(member_data: member_schema.MemberCreate, db: Session = Depends(get_db)):
    db_member = db.query(member.Member).filter(member.Member.phone_number == member_data.phone_number).first()
    if db_member:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    db_member = member.Member(**member_data.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@router.get("/members/", response_model=List[member_schema.MemberResponse])
def get_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = db.query(member.Member).offset(skip).limit(limit).all()
    return members

@router.get("/members/{member_id}", response_model=member_schema.MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(member.Member).filter(member.Member.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.put("/members/{member_id}", response_model=member_schema.MemberResponse)
def update_member(member_id: int, member_data: member_schema.MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(member.Member).filter(member.Member.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if member_data.phone_number and member_data.phone_number != db_member.phone_number:
        existing_member = db.query(member.Member).filter(member.Member.phone_number == member_data.phone_number).first()
        if existing_member:
            raise HTTPException(status_code=400, detail="Phone number already registered")
    
    update_data = member_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member

@router.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(member.Member).filter(member.Member.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(db_member)
    db.commit()
    return {"message": "Member deleted successfully"}

@router.get("/members/check/{last_four_digits}")
def check_member_by_phone(last_four_digits: str, db: Session = Depends(get_db)):
    """전화번호 뒷자리 4자리로 회원 출입 확인"""
    if len(last_four_digits) != 4 or not last_four_digits.isdigit():
        raise HTTPException(status_code=400, detail="전화번호 뒷자리 4자리를 입력해주세요")
    
    # 전화번호 뒷자리가 일치하는 회원 검색
    members = db.query(member.Member).filter(
        member.Member.phone_number.like(f"%-{last_four_digits}")
    ).all()
    
    if not members:
        raise HTTPException(status_code=404, detail="등록되지 않은 회원입니다")
    
    if len(members) > 1:
        # 여러 명이 같은 뒷자리를 가진 경우
        member_list = [{"id": m.id, "name": m.name, "phone": m.phone_number} for m in members]
        raise HTTPException(
            status_code=409, 
            detail={
                "message": "동일한 뒷자리를 가진 회원이 여러 명 있습니다",
                "members": member_list
            }
        )
    
    found_member = members[0]
    
    # 남은 기간 계산
    today = date.today()
    if found_member.end_date:
        remaining_days = (found_member.end_date - today).days
        if remaining_days < 0:
            status = "만료"
            remaining_days = abs(remaining_days)
            remaining_message = f"{remaining_days}일 전에 만료되었습니다"
        elif remaining_days == 0:
            status = "오늘만료"
            remaining_message = "오늘까지입니다"
        else:
            status = "유효"
            remaining_message = f"{remaining_days}일 남았습니다"
    else:
        status = "무제한"
        remaining_message = "무제한 회원입니다"
    
    return {
        "member": {
            "id": found_member.id,
            "name": found_member.name,
            "phone_number": found_member.phone_number,
            "start_date": found_member.start_date,
            "end_date": found_member.end_date
        },
        "status": status,
        "remaining_message": remaining_message,
        "welcome_message": f"안녕하세요, {found_member.name}님! 🏋️‍♂️"
    }