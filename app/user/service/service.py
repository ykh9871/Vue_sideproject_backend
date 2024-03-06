from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.user.dto.dto import User, UserInfo, UserID
from typing import Optional, Union
from jose import jwt
import mysql.connector

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

class UserService:
    def __init__(self):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 20 # 20 minutes
        self.REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 30  # 1 month
        self.SECRET_KEY = "asdasdqweasdqwea"
        self.ALGORITHM = "HS256"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.conn = mysql.connector.connect(
            port=3307,
            user="root",
            host="localhost",
            password="ykh9871",
            database="shoppingmall"
        )
        self.cursor= self.conn.cursor()

    def signup(self, user: User):
    # 직업명에 해당하는 id를 찾기 위한 쿼리 실행  
        hashed_password = self.hash_password(user.password)
        # 검색된 직업 id와 함께 사용자 정보를 삽입하는 쿼리 실행
        self.cursor.execute(
            "INSERT INTO customer (Name, Email, Password, Address, Phone) "
            "VALUES (%s, %s, %s, %s, %s)",
            (user.name, user.email, hashed_password, user.address, user.phone),
        )
        self.conn.commit()
        
    def get_user_info(self, email: str) -> UserInfo:
        self.cursor.execute(
            "SELECT name, email, address, phone, createdat, modifiedat "
            "FROM customer  WHERE email=%s",
            (email,))
        user = self.cursor.fetchone()
        if user:
            return UserInfo(
                name=user[0],
                email=user[1],
                address=user[2],
                phone=user[3],
                created_at=user[4],
                modified_at=user[5]
            )
        return None

    def update_user_info(self, email: str, name: str, phone: str, address: str) -> None:
        modified_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.cursor.execute(
            "UPDATE customer "
            "SET name=%s, phone=%s, address=%s, modifiedat=%s "
            "WHERE email=%s",
            (name, phone, address, modified_at, email)
        )
        self.conn.commit()

    def update_user_password(self, email: str, new_password: str) -> None:
        # 새로운 비밀번호를 해싱합니다.
        hashed_password = self.hash_password(new_password)
        # 수정된 날짜를 현재 시간으로 설정합니다.
        modified_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        # 사용자 비밀번호와 수정된 날짜를 업데이트합니다.
        self.cursor.execute(
            "UPDATE customer "
            "SET password=%s, modifiedat=%s "
            "WHERE email=%s",
            (hashed_password, modified_at, email)
        )
        self.conn.commit()

    def withdrawal(self, email:str):
        self.cursor.execute(
            "UPDATE customer "
            "SET activate=0, deletedat=%s "
            "WHERE email=%s", 
            (datetime.now().strftime('%Y-%m-%d %H:%M'), email)
        )
        self.conn.commit()
            
    def authenticate(self, email: str, password: str):
        self.cursor.execute(
            "SELECT * "
            "FROM customer "
            "WHERE email=%s AND activate=1",
            (email,))
        user = self.cursor.fetchone()
        if user and self.verify_password(password, user[3]):
            return User(
                name=user[1], 
                email=user[2], 
                password=user[3], 
                address=user[4],
                phone=user[5]
            )
        return None
    def exp_date(self):
        return self.ACCESS_TOKEN_EXPIRE_MINUTES
        

    def create_access_token(self, username : str):
        data = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        access_token = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return access_token

    def create_refresh_token(self, username : str):
        data = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_SECONDS)
        }
        refresh_token = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return refresh_token

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_email_from_token(self, token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)
        return payload.get("sub")
    
    def get_userid_by_email(self, token: str = Depends(oauth2_scheme)):
        email = self.get_email_from_token(token)
        self.cursor.execute(
            "SELECT id "
            "FROM customer "
            "WHERE email = %s",
            (email,),
        )
        userid = self.cursor.fetchone()
        return userid[0]