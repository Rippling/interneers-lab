from fastapi import APIRouter, HTTPException, Depends
from application.use_cases import GetUserUseCase
from infra.database_adapter import SQLiteUserAdapter

user_router = APIRouter()

# This is our "Factory" function. It builds the tools we need.
def get_user_use_case() -> GetUserUseCase:
    db_adapter = SQLiteUserAdapter()
    return GetUserUseCase(db_port=db_adapter)

# Notice the `Depends()` here. FastAPI automatically runs the factory 
# function and passes the ready-to-use Use Case into our endpoint!
@user_router.get("/api/users/{user_id}")
def get_user_endpoint(user_id: int, use_case: GetUserUseCase = Depends(get_user_use_case)):
    try:
        user = use_case.execute(user_id)
        return {"data": {"id": user.id, "name": user.name}}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))