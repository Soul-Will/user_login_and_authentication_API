from fastapi import APIRouter,HTTPException,status,Depends
from database.database import SessionLocal
from src.schemas.user import RegisterUserSchema,GetAllUserSchema,PatchUserSchema,PutForgetPassword,resetUserPassword
from src.models.user import USER,OTP
from src.utils.user import pwd_content,find_same_email,find_same_username,username_validation,password_validation,generate_otp_,send_email,passchecker,get_token,decode_token
import random
import uuid

user_router = APIRouter()
db = SessionLocal()

@user_router.post("/user_registration")
def user_registration(user:RegisterUserSchema):
    new_user = USER(
        id = str(uuid.uuid4()),
        username = user.username,
        email = user.email,
        password = pwd_content.hash(user.password),
        country = user.country.upper()
    )
    find_data = db.query(USER).first()
    if find_data:
        find_same_email(user.email)
        find_same_username(user.username)
    username_validation(user.username)
    password_validation(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "Registration Successfully"

@user_router.get("/get_all_user",response_model=list[GetAllUserSchema])
def get_all_user():
    find_user_data = db.query(USER).filter(USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).all()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    return find_user_data

@user_router.get("/search_user/{user_id}",response_model=GetAllUserSchema)
def search_user(user_id:str):
    find_user_data = db.query(USER).filter(USER.id == user_id,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    return find_user_data

@user_router.patch("/update_user/{user_id}")
def update_user(user_id:str,user:PatchUserSchema):
    find_user_data = db.query(USER).filter(USER.id == user_id,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    data_without_none = user.model_dump(exclude_none=True)
    for key,value in data_without_none.items():
        if key == "password":
            setattr(find_user_data,key,pwd_content.hash(value))
        elif key == "username":
            find_same_username(value)
            setattr(find_user_data,key,value)
        elif key == "email":
            find_same_email(value)
            setattr(find_user_data,key,value)
        else:
            setattr(find_user_data,key,value)
    db.commit()
    db.refresh(find_user_data)
    return {"Message":"User Data Updated Successfully","Data":find_user_data}

@user_router.delete("/delete_user/{user_id}")
def delete_user(user_id:str):
    find_user_data = db.query(USER).filter(USER.id == user_id,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first()
    if db.query(USER).filter(USER.id == user_id,USER.isDeleted == True,USER.isActive == False, USER.isVerified == False).first():
        raise HTTPException(status_code=400,detail="User Already Deleted")
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    find_user_data.isActive = False
    find_user_data.isVerified = False
    find_user_data.isDeleted = True
    db.commit()
    db.refresh(find_user_data)
    return {"Message":"User Data Deleted Successfully","Data":find_user_data}

@user_router.post("/generate_otp/{email}")
def generate_otp(email:str):
    find_user_data = db.query(USER).filter(USER.email == email,USER.isActive == True, USER.isVerified == False, USER.isDeleted == False).first()
    if db.query(USER).filter(USER.email == email,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first():
        raise HTTPException(status_code=400,detail="Email Already Verified")
    if not find_user_data:
        raise HTTPException(status_code=400,detail="Email Not Found")
    
    
    generated_otp = generate_otp_()
    send_email(find_user_data.email,"Verification OTP",f"OTP for Verification is {generated_otp}")

    new_otp_data = OTP(
        user_id = find_user_data.id,
        email = find_user_data.email,
        otp = generated_otp
    )

    db.add(new_otp_data)
    db.commit()
    db.refresh(new_otp_data)
    return "OTP Generated Successfully"

@user_router.get("/verify_otp")
def verify_otp(email:str,otp:str):
    find_user_data = db.query(USER).filter(USER.email == email,USER.isActive == True, USER.isVerified == False, USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    find_otp_data = db.query(OTP).filter(OTP.email == email, OTP.otp == otp).first()
    if not find_otp_data:
        raise HTTPException(status_code=400,detail="OTP Not Found")
    find_user_data.isVerified = True
    db.delete(find_otp_data)
    db.commit()
    db.refresh(find_user_data)
    return "User Verification Done Successfully"

@user_router.get("/login")
def login(username:str,password:str):
    find_user_data = db.query(USER).filter(USER.username == username,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    passchecker(password,find_user_data.password)

    access_token = get_token(find_user_data.id,find_user_data.username,find_user_data.email)
    return {"Access Token":access_token}

@user_router.post("/forget_password_and_generate_otp")
def forget_password_and_generate_otp(email:str):
    find_user_data = db.query(USER).filter(USER.email == email,USER.isActive == True,USER.isVerified == True,USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="Email Not Found")
    generated_otp = generate_otp_()
    send_email(find_user_data.email,"Verification OTP",f"OTP for Forget Password is {generated_otp}")
    new_otp_data = OTP(
        user_id = find_user_data.id,
        email = find_user_data.email,
        otp = generated_otp
    )

    db.add(new_otp_data)
    db.commit()
    db.refresh(new_otp_data)
    return "OTP Generated Successfully for Forget Password"

def forget_password_verification(email:str,otp:str):
    find_user_data = db.query(USER).filter(USER.email == email,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    find_otp_data = db.query(OTP).filter(OTP.email == email, OTP.otp == otp).first()
    if not find_otp_data:
        raise HTTPException(status_code=400,detail="OTP Not Found")
    db.delete(find_otp_data)
    db.commit()
    db.refresh(find_user_data)
    return email

@user_router.put("/forget_password_set_new_password")
def forget_password_set_new_password(password:PutForgetPassword ,email:str=Depends(forget_password_verification)):
    find_user_data = db.query(USER).filter(USER.email == email).first()
    if password.new_password != password.confirm_password:
        raise HTTPException(status_code=400,detail="New Password and Confirm Password didn't Match")
    find_user_data.password = pwd_content.hash(password.confirm_password)
    db.commit()
    db.refresh(find_user_data)
    return "Password Change Successfully"

@user_router.put("/reset_password")
def reset_password(token:str,change_password:resetUserPassword):
    info = decode_token(token)
    id = info.get("id")
    find_user_data = db.query(USER).filter(USER.id == id,USER.isActive == True, USER.isVerified == True, USER.isDeleted == False).first()
    if not find_user_data:
        raise HTTPException(status_code=400,detail="User Not Found")
    passchecker(change_password.password,find_user_data.password)
    if change_password.new_password != change_password.confirm_password:
        raise HTTPException(status_code=400,detail="New Password and Confirm Password didn't Match")
    find_user_data.password = pwd_content.hash(change_password.confirm_password)
    db.commit()
    db.refresh(find_user_data)
    return "Password Change Successfully"

    