import json
import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    SENSITIVE_FIELDS = {"password", "otp_code", "token", "secret", "api_key"}

    def _mask_sensitive_data(self, data: dict) -> dict:
        masked = data.copy()
        for key in masked:
            if any(sensitive in key.lower() for sensitive in self.SENSITIVE_FIELDS):
                masked[key] = "***MASKED***"
        return masked

    async def _get_request_body(self, request: Request, debug: bool) -> dict | None:
        if not debug or request.method not in ("POST", "PUT", "PATCH"):
            return None

        try:
            body = await request.body()
            if not body:
                return None

            body_json = json.loads(body.decode("utf-8"))
            return self._mask_sensitive_data(body_json)
        except Exception:
            return None

    async def dispatch(self, request: Request, call_next) -> Response:
        correlation_id = str(uuid.uuid4())
        start_time = time.time()

        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

        logger = structlog.get_logger()

        from app.infrastructure.config.EnvConfig import EnvConfig
        config = EnvConfig.load()

        request_body = await self._get_request_body(request, config.debug)

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
            "query_params": str(request.query_params) if request.query_params else None,
        }

        if request_body:
            log_data["request_body"] = request_body

        logger.info("request_started", **log_data)

        try:
            response = await call_next(request)

            duration_ms = int((time.time() - start_time) * 1000)

            logger.info(
                "request_completed",
                status_code=int(response.status_code),
                duration_ms=duration_ms
            )

            response.headers["X-Correlation-ID"] = correlation_id
            return response

        except Exception as exc:
            duration_ms = int((time.time() - start_time) * 1000)

            logger.exception(
                "request_failed",
                duration_ms=duration_ms,
                exc_info=exc
            )
            raise

        finally:
            structlog.contextvars.unbind_contextvars("correlation_id")
