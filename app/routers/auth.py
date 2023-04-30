from fastapi import APIRouter, status, HTTPException, Response, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2, token_utils, mailer_utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = '/login',
    tags = ["Authentification"]
)

@router.post('/', response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user.is_verified == False:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail= "Account Not Verified")

    if user == None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail= f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail= f"Invalid Credentials")

    # Create a token

    # Get room access data
    room_access = []
    [room_access.append(i.room_id) for i in user.access]

    access_token = oauth2.create_access_token(
        data = {
        "user_id" : user.id,
        "roles" : user.roles
        }
        )

    return {"access_token" : access_token, "token_type": "bearer" }

@router.get('/')
def authentication(current_user: dict = Depends(oauth2.get_current_user), response_model=schemas.UserData):
    return current_user.access


@router.post('/confirm-email/{token}/', status_code=status.HTTP_202_ACCEPTED)
async def user_verification(token:str, db: Session = Depends(get_db)):
        
    token_data = token_utils.verify_token(token, expiry=1800)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail= "Invalid Token Provided"
                            )
    
    user = db.query(models.User).filter(models.User.email==token_data['email']).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"User with email {user.email} does not exist"
                            )
    
    user.is_verified = True

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        'message':'Email Verification Successful',
        'status':status.HTTP_202_ACCEPTED
        }


@router.post('/resend-verification/', status_code=status.HTTP_201_CREATED)
async def send_email_verfication(email_data: schemas.EmailSchema, db: Session = Depends(get_db)):

       
    user_check = db.query(models.User).filter(models.User.email ==email_data.email).first()
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= "User information does not exist"
                            )
                            
    token = token_utils.token(email_data.email)
    

    frontend_url = 'http://localhost:5173/'

    email_verification_endpoint = f'{frontend_url}confirm-email/{token}/'
    
    mail_body = {
        'email':user_check.email,
        'project_name': 'Room Booking App',
        'url': email_verification_endpoint
    }
    
    mail_status = await mailer_utils.send_email_async(
    subject="Email Verification: Registration Confirmation",
    email_to=user_check.email, body=mail_body, template='template.html'
    )
    
    if mail_status == True:    
        return {
            "message":"mail for Email Verification has been sent, kindly check your inbox.",
            "status": status.HTTP_201_CREATED
        }
    else:
        return {
            "message":"mail for Email Verification failled to send, kindly reach out to the server guy.",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
    }



@router.post('/reset-password-email/', status_code=status.HTTP_201_CREATED)
async def send_reset_password(email_data: schemas.EmailSchema, db: Session = Depends(get_db)):

       
    user_check = db.query(models.User).filter(models.User.email ==email_data.email).first()
    
    if not user_check:
        return
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail= "User information does not exist"
        #                     )

    if not user_check.is_verified:
        return

    token = token_utils.token(email_data.email)
    
    frontend_url = 'http://localhost:5173/'

    email_verification_endpoint = f'{frontend_url}reset-password/{token}/'
    
    mail_body = {
        'email':user_check.email,
        'project_name': 'Room Booking App',
        'url': email_verification_endpoint
    }
    
    mail_status = await mailer_utils.send_email_async(
    subject="Password Reset",
    email_to=user_check.email, body=mail_body, template='reset-password.html'
    )
    
    if mail_status == True:    
        return {
            "message":"mail for Password Reset has been sent, kindly check your inbox.",
            "status": status.HTTP_201_CREATED
        }
    else:
        return {
            "message":"mail for Password Reset failled to send, kindly reach out to the server guy.",
            "status": status.HTTP_503_SERVICE_UNAVAILABLE
    }


@router.post('/reset-password-auth/{token}/', status_code=status.HTTP_202_ACCEPTED)
async def reset_password_email(token:str, db: Session = Depends(get_db)):
        
    token_data = token_utils.verify_token(token, expiry=900)

    if not token_data:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail= "Invalid Token Provided"
                            )
    
    return {
        'message': token_data,
        'status':status.HTTP_202_ACCEPTED
        }

@router.post('/reset-password/{token}/', status_code=status.HTTP_202_ACCEPTED)
async def reset_password(token:str, password: schemas.UserResetPassword, db: Session = Depends(get_db)):
        
    token_data = token_utils.verify_token(token, expiry=900)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail= "Invalid Token Provided"
                            )
    
    user = db.query(models.User).filter(models.User.email==token_data['email']).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"User with email {user.email} does not exist"
                            )
    
    # Hash the password - user.password
    hashed_password = utils.hash(password.password)
    user.password = hashed_password

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        'message':'Password Succesfully Reset',
        'status':status.HTTP_202_ACCEPTED
        }