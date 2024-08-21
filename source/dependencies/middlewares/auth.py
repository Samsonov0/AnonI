import datetime
import time
from typing import Dict

import bcrypt
import jwt

from source.dependencies import RequestData
from source.dependencies.exceptions import HTTPException
from source.dependencies.middlewares.default import AbstractMiddleware
from source.settings import SETTINGS
from source.utils.status_code import HTTP_403_FORBIDDEN


class JWTBearerMiddleware(AbstractMiddleware):
    def __init__(
        self,
        request_data: RequestData | None = None,
        response_data: None = None,
    ) -> None:
        super().__init__(request_data=request_data, response_data=response_data)

        self._check_settings()

    async def _processing(self) -> RequestData:
        headers = self.request_data.headers()
        authorization: str = headers.get("authorization", "")
        if "bearer" not in authorization.lower():
            raise HTTPException(
                status=HTTP_403_FORBIDDEN,
                message_type="message",
                message="Authorization header not found",
            )
        token = await self.decode_token(authorization.split(" ")[-1])
        if token:
            if token.get("type") == "access":
                if not await self.token_is_valid(token):
                    raise HTTPException(
                        status=HTTP_403_FORBIDDEN,
                        message_type="message",
                        message="Invalid token or expired token.",
                    )
                return self.request_data
            else:
                raise HTTPException(
                    status=HTTP_403_FORBIDDEN,
                    message_type="message",
                    message="Invalid token or expired token.",
                )

        raise HTTPException(
            status=HTTP_403_FORBIDDEN,
            message_type="message",
            message="Invalid authorization code.",
        )

    def get_hashed_password(self, plain_text_password):
        return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

    def check_password(self, plain_text_password, hashed_password):
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

    async def sign_jwt(self, user_id: str) -> Dict[str, str]:
        exp_time = time.time()
        payload_access = {
            "type": "access",
            "user_id": user_id,
            # 30 min by default
            "expires_datetime_ts": exp_time + int(SETTINGS.JWT_LIVE_TIME_SEC),
        }
        payload_refresh = {
            "type": "refresh",
            "user_id": user_id,
            # 180 min by default
            "expires_datetime_ts": exp_time + int(SETTINGS.JWT_REFRESH_LIVE_TIME_SEC),
        }

        token = jwt.encode(
            payload_access, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM
        )
        refresh_token = jwt.encode(
            payload_refresh, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM
        )

        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "expires_datetime_ts": payload_access["expires_datetime_ts"],
            "expires_datetime_dt": datetime.datetime.fromtimestamp(
                payload_access["expires_datetime_ts"]
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "auth_type_header": "Bearer",
        }

    async def decode_token(self, token: str) -> dict | None:
        try:
            decoded_token = jwt.decode(
                jwt=token, key=SETTINGS.JWT_SECRET, algorithms=[SETTINGS.JWT_ALGORITHM]
            )
            return decoded_token
        except Exception as e:
            return None

    async def token_is_valid(self, token: dict) -> bool:
        if token.get("expires_datetime_ts") >= time.time():
            return True
        return False

    def _check_settings(self) -> None:
        if getattr(SETTINGS, "JWT_SECRET") == "DEFAULT":
            raise ValueError("You have to set JWT_SECRET environment in your project")
        if not hasattr(SETTINGS, "JWT_ALGORITHM"):
            raise ValueError(
                "You have to set JWT_ALGORITHM environment in your project"
            )
