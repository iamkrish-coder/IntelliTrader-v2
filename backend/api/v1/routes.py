from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional, List
from backend.domain.schemas.user_schema import UserSchema
from backend.domain.schemas.account_schema import AccountSchema
from backend.domain.schemas.session_schema import SessionSchema, SessionAndUserSchema
from backend.domain.schemas.verification_token_schema import (
    VerificationTokenSchema,
    UseVerificationTokenSchema
)
from backend.services.user_service import UserService
from backend.services.account_service import AccountService
from backend.services.session_service import SessionService
from backend.services.verification_token_service import VerificationTokenService
from backend.core.exceptions import ApiException
from backend.utils.logging_utils import *
from backend.database.managers.database_manager import DatabaseManager

router = APIRouter()

# --- User Endpoints ---
@router.post("/auth/users", response_model=UserSchema)
async def create_user(user: UserSchema):
    """Create a new user."""
    try:
        db_manager = DatabaseManager.get_instance()
        user_service = UserService(db_manager, user.model_dump())
        response = await user_service.create_new_user_account()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Create user error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in create user: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing create user request", data=str(e)
        ).to_http_exception()


@router.get("/auth/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: str):
    """Get a user by ID."""
    try:
        db_manager = DatabaseManager.get_instance()
        user_service = UserService(db_manager, {"id": user_id})
        response = await user_service.get_user_by_id()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Get user error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in get user: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing get user request", data=str(e)
        ).to_http_exception()


@router.get("/auth/users/email/{email}", response_model=UserSchema)
async def get_user_by_email(email: str):
    """Get a user by email."""
    try:
        db_manager = DatabaseManager.get_instance()
        user_service = UserService(db_manager, {"email": email})
        response = await user_service.get_user_by_email()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Get user by email error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in get user by email: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing get user by email request", data=str(e)
        ).to_http_exception()


@router.get("/auth/users/account/{provider}/{providerAccountId}", response_model=UserSchema)
async def get_user_by_account(provider: str, providerAccountId: str):
    """Get a user by account provider and ID."""
    try:
        db_manager = DatabaseManager.get_instance()
        user_service = UserService(
            db_manager, {"provider": provider, "providerAccountId": providerAccountId}
        )
        response = await user_service.get_user_by_account()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Get user by account error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in get user by account: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing get user by account request",
            data=str(e),
        ).to_http_exception()


@router.patch("/auth/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user: UserSchema):
    """Update an existing user."""
    try:
        db_manager = DatabaseManager.get_instance()
        user_service = UserService(db_manager, user.model_dump())
        response = await user_service.update_user(user_id)
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Update user error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in update user: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing update user request", data=str(e)
        ).to_http_exception()


# --- Account Endpoints ---
@router.post("/auth/accounts", response_model=AccountSchema)
async def link_account(account: AccountSchema):
    """Link an account to a user."""
    try:
        db_manager = DatabaseManager.get_instance()
        account_service = AccountService(db_manager, account.model_dump())
        response = await account_service.link_account()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Link account error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in link account: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing link account request", data=str(e)
        ).to_http_exception()


# --- Session Endpoints ---
@router.post("/auth/sessions", response_model=SessionSchema)
async def create_session(session: SessionSchema):
    """Create a new session."""
    try:
        db_manager = DatabaseManager.get_instance()
        session_service = SessionService(db_manager, session.model_dump())
        response = await session_service.create_session()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Create session error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in create session: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing create session request", data=str(e)
        ).to_http_exception()


@router.get("/auth/sessions/{session_token}", response_model=SessionAndUserSchema)
async def get_session_and_user(session_token: str):
    """Get a session and its associated user."""
    try:
        db_manager = DatabaseManager.get_instance()
        session_service = SessionService(db_manager, {"sessionToken": session_token})
        response = await session_service.get_session_and_user()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Get session and user error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in get session and user: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing get session and user request", data=str(e)
        ).to_http_exception()


@router.patch("/auth/sessions/{session_token}", response_model=SessionSchema)
async def update_session(session_token: str, session: SessionSchema):
    """Update an existing session."""
    try:
        db_manager = DatabaseManager.get_instance()
        session_service = SessionService(db_manager, session.model_dump())
        response = await session_service.update_session(session_token)
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Update session error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in update session: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing update session request", data=str(e)
        ).to_http_exception()


@router.delete("/auth/sessions/{session_token}")
async def delete_session(session_token: str):
    """Delete a session."""
    try:
        db_manager = DatabaseManager.get_instance()
        session_service = SessionService(db_manager, {"sessionToken": session_token})
        response = await session_service.delete_session()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Delete session error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in delete session: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing delete session request", data=str(e)
        ).to_http_exception()


# --- Verification Token Endpoints ---
@router.post("/auth/verification-tokens", response_model=VerificationTokenSchema)
async def create_verification_token(token: VerificationTokenSchema):
    """Create a new verification token."""
    try:
        db_manager = DatabaseManager.get_instance()
        token_service = VerificationTokenService(db_manager, token.model_dump())
        response = await token_service.create_verification_token()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Create verification token error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in create verification token: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing create verification token request",
            data=str(e),
        ).to_http_exception()


@router.post("/auth/verification-tokens/use")
async def use_verification_token(body: UseVerificationTokenSchema):
    """Use and delete a verification token."""
    try:
        db_manager = DatabaseManager.get_instance()
        token_service = VerificationTokenService(db_manager, body.model_dump())
        response = await token_service.use_verification_token()
        return response.to_http_response()
    except ApiException as error:
        log_error(f"Use verification token error: {str(error)}")
        raise error.to_http_exception()
    except Exception as e:
        log_error(f"Unexpected error in use verification token: {str(e)}")
        raise ApiException.internal_server_error(
            message="Unexpected error processing use verification token request",
            data=str(e),
        ).to_http_exception()
