from fastapi import FastAPI
from app.infrastructure.config.server.Settings import settings as AppSetting
from app.infrastructure.config.server.CorsMiddlewareSettings import setup_cors
import uvicorn

app = FastAPI(
    title=AppSetting.app_name,
    debug=AppSetting.debug
)
setup_cors(app)

@app.get("/$>c2saae)(}info")
def get_root():
    return {
        "app_name": AppSetting.app_name,
        "environment": AppSetting.environtment,
        "debug": AppSetting.debug,
        "database_url": str(AppSetting.database_url),
        "redis_url": str(AppSetting.redis_url),
        "jwt_algorithm": AppSetting.jwt_algorithm,
        "jwt_secret_key": AppSetting.jwt_secret_key,
        "encryption_key": AppSetting.encryption_key,
        "salt_secret": AppSetting.salt_secret
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=AppSetting.server_host,
        port=AppSetting.server_port,
        reload=AppSetting.debug
    )