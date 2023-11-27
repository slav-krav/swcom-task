from __future__ import annotations

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

import crud
import models
from database import SessionLocal, create_tables, get_or_create
from opa_middleware import opa_access_check
from schemas import User, UserWithToken

app = FastAPI()
API_ENDPOINT = '/api/users'

app.middleware('http')(opa_access_check)

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', include_in_schema=False)
def home():
    content = """<h1>Dear swisscom engineer, welcome!</h1>
    <p> To initialize database and add sample users go to <a href="/init"> /init </a> page.
     </br> 
     Copy JWT tokens provided. Or just dont close the page.
     </br>
     Go to <a href="/docs"> a swagger </a> page and use the tokens for authorisation.
     </br>
     Play around! Any request to /api will be authorised via OPA sidecar service.
     </p>
    """
    return HTMLResponse(content=content)


@app.get('/init', include_in_schema=False)
def init(db: Session = Depends(get_db)):
    """Issue a simple get request here to populate database with initial entities."""
    create_tables(db.connection())
    get_or_create(db, models.Role, type='admin')
    get_or_create(db, models.Role, type='regular')
    admin = UserWithToken.model_validate(crud.create_user_sample(db, 'admin'))
    regular = UserWithToken.model_validate(crud.create_user_sample(db, 'regular'))
    return HTMLResponse(content=f"""
    <form">
      <label for="admin">Admin token:</label></br>
      <input type="text" id="admin" size="{len(admin.session.token) + 30}" value={admin.session.token} disabled><br><br>
      <label for="regular">Regular user token:</label></br>
      <input type="text" id="admin" size="{len(regular.session.token) + 30}" value={regular.session.token} disabled><br><br>
    </form>
    """)


@app.get(API_ENDPOINT)
def read_users(db: Session = Depends(get_db),
               show_jwt: bool = False,
               auth: str = Depends(security)) -> list[User] | list[UserWithToken]:
    users = crud.get_users(db)
    if not show_jwt:
        return [User.model_validate(user) for user in users]

    return [UserWithToken.model_validate(user) for user in users]


@app.post(API_ENDPOINT)
def create_user(user: User, db: Session = Depends(get_db), auth: str = Depends(security)) -> UserWithToken:
    user = crud.create_user(db, user)
    return UserWithToken.model_validate(user)
