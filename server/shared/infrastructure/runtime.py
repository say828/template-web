from config import get_settings


def build_runtime_metadata() -> dict[str, str]:
    settings = get_settings()
    return {"app_name": settings.app_name, "environment": settings.environment}
