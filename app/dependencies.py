from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud, User, GetDB
from app.db.models import Service
from app.models.admin import Admin, oauth2_scheme
from app.utils.auth import get_admin_payload


def get_db():
    with GetDB() as db:
        yield db


def get_admin(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    payload = get_admin_payload(token)
    if not payload:
        return

    dbadmin = crud.get_admin(db, payload["username"])
    if not dbadmin:
        return

    if dbadmin.password_reset_at:
        created_at = payload.get("created_at")
        if not created_at or dbadmin.password_reset_at > created_at:
            return

    if not dbadmin.is_sudo and not dbadmin.enabled:
        return

    return Admin.model_validate(dbadmin)


def get_current_admin(admin: Annotated[Admin, Depends(get_admin)]):
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return admin


def sudo_admin(admin: Annotated[Admin, Depends(get_current_admin)]):
    if not admin.is_sudo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied",
        )
    return admin


def get_subscription_user(
    username: str, key: str, db: Annotated[Session, Depends(get_db)]
):
    try:
        int(key, 16)
    except ValueError:
        raise HTTPException(status_code=404)

    db_user = crud.get_user(db, username)
    if db_user and db_user.key == key:
        return db_user
    else:
        raise HTTPException(status_code=404)


def get_user(
    username: str,
    admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    db_user = crud.get_user(db, username)
    if not (
        admin.is_sudo or (db_user and db_user.admin.username == admin.username)
    ):
        raise HTTPException(status_code=403, detail="You're not allowed")

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


def add_users_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.add_users_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def edit_users_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.edit_users_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def delete_users_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.delete_users_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def delete_expired_users_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.delete_expired_users_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def reset_users_usage_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.reset_users_usage_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def toggle_users_status_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.toggle_users_status_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def revoke_users_sub_access(
    admin: Annotated[Admin, Depends(get_current_admin)]
):
    if not admin.is_sudo and not admin.revoke_users_sub_access:
        raise HTTPException(status_code=403, detail="You're not allowed")


def parse_start_date(start: str | None = None):
    if not start:
        return datetime.fromtimestamp(
            datetime.utcnow().timestamp() - 30 * 24 * 3600
        )
    else:
        return datetime.fromisoformat(start)


def parse_end_date(end: str | None = None):
    if not end:
        return datetime.utcnow()
    else:
        return datetime.fromisoformat(end)


def get_service(id: int, db: Annotated[Session, Depends(get_db)]):
    service = crud.get_service(db, id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


SubUserDep = Annotated[User, Depends(get_subscription_user)]
UserDep = Annotated[User, Depends(get_user)]
AdminDep = Annotated[Admin, Depends(get_current_admin)]
SudoAdminDep = Annotated[Admin, Depends(sudo_admin)]
DBDep = Annotated[Session, Depends(get_db)]
StartDateDep = Annotated[datetime, Depends(parse_start_date)]
EndDateDep = Annotated[datetime, Depends(parse_end_date)]
AddUsersAccess = Annotated[None, Depends(add_users_access)]
EditUsersAccess = Annotated[None, Depends(edit_users_access)]
DeleteUsersAccess = Annotated[None, Depends(delete_users_access)]
DeleteExpiredUsersAccess = Annotated[None, Depends(delete_expired_users_access)]
ResetUsersUsageAccess = Annotated[None, Depends(reset_users_usage_access)]
ToggleUsersStatusAccess = Annotated[None, Depends(toggle_users_status_access)]
RevokeUsersSubAccess = Annotated[None, Depends(revoke_users_sub_access)]
ServiceDep = Annotated[Service, Depends(get_service)]
