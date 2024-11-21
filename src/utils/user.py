from passlib.context import CryptContext
from database.database import SessionLocal
from src.models.user import USER
from fastapi import HTTPException,status
import re
from config import SENDER_MAIL,PASSWORD,ALGORITHM,SECRET_KEY
import jwt
from datetime import datetime,timezone,timedelta
import random

db = SessionLocal()

pwd_content = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def find_same_email(email:str):
    find_email = db.query(USER).filter(USER.email == email).first()
    if find_email:
        if find_email.isActive == True and find_email.isVerified == True:
            raise HTTPException(status_code=400,detail="Email Already In Use")
        if find_email.isActive == True and find_email.isVerified == False:
            raise HTTPException(status_code=400,detail="Email Already In Use But Verification Pending")
        if find_email.isActive == False:
            raise HTTPException(status_code=400,detail="Same Email Found But Not In Use")

def find_same_username(name:str):
    find_email = db.query(USER).filter(USER.username == name).first()
    if find_email:
        if find_email.isActive == True and find_email.isVerified == True:
            raise HTTPException(status_code=400,detail="Username Already In Use")
        if find_email.isActive == False:
            raise HTTPException(status_code=400,detail="Same Username Found But Not In Use")

def username_validation(username:str):
    if not len(username) >= 8 or not re.match("^[a-zA-Z0-9_-]+$", username):
        raise HTTPException(status_code=400,detail="Username Criteria doesn't Match")

def password_validation(password:str):
    pattern = "^.*(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    if not len(password) >= 8 or not re.findall(pattern,password):
        raise HTTPException(status_code=400,detail="Password Criteria doesn't Match")

def generate_otp_():
    generated_otp = random.randint(100000,999999)
    print("------------------------------")
    print(f"Generated OTP {generated_otp}")
    print("------------------------------")
    return generated_otp

# This part of code is to send the generated OTP to the user via email

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver, subject, body):

    # SMTP Configuration (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = SENDER_MAIL
    smtp_pass = PASSWORD

    #build the mail system to send someone
    msg = MIMEMultipart()
    msg['From'] = SENDER_MAIL
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    #now try to send the mail to receiver 

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(SENDER_MAIL, receiver, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def passchecker(user_entered_password:str,password:str):
    if pwd_content.verify(user_entered_password,password):
        return True
    else:
        raise HTTPException(status_code=400,detail="Incorrect Password")
    
def get_token(id:str,username:str,email:str):
    payload = {
        "id":id,
        "username":username,
        "email":email,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=120)
    }
    access_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return access_token

def decode_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id = payload.get("id")
        username = payload.get("username")
        email = payload.get("email")
        if not id or not username or not email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Token")
        return {"id":id,"username":username,"email":email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Token")