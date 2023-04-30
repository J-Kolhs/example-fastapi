from fastapi import status, HTTPException, APIRouter, Depends, Response
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from .. import schemas, models, oauth2

# The router is created using APIRouter from fastapi, with a prefix of /companies and a tag of Companies.
router = APIRouter(
    prefix = "/companies",
    tags = ["Companies"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.CompanyData)
def create_companies(company: schemas.CompaniesCreate, db: Session = Depends((get_db)), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can create companies")
   
    new_company = models.Companies(companies_name = company.companies_name) 
    
    try:
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

    except IntegrityError as e:
        print(e.orig)
        if type(e.orig) == UniqueViolation:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail =  str(e.orig) )    
        if type(e.orig) == ForeignKeyViolation:
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail = str(e.orig))
    else:
        return new_company

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    company_query = db.query(models.Companies).filter(models.Companies.id == id)
    company = company_query.first()

    if company == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Company with id {id} does not exist")

    if current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can delete companies")

    company_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", status_code=status.HTTP_200_OK, response_model= List[schemas.CompanyData])
def get_company(db: Session = Depends((get_db))):
    
    companies = db.query(models.Companies).all()
    return companies

@router.put("/{id}",  response_model = schemas.CompanyData)
def update_company(id: int, company: schemas.CompaniesCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    try:
        companies_query = db.query(models.Companies).filter(models.Companies.id == id)
        companies_updated = companies_query.first()

        if current_user.roles != 'ADMIN':
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can update companies")
        if companies_updated == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"Company with id {id} does not exist")

        companies_query.update(company.dict(), synchronize_session= False)

        db.commit()

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown Error")
            
    else:
        return companies_query.first()