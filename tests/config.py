import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración del framework de pruebas, leída de variables de entorno.

    En local usa el valor por defecto (servidor arrancado a mano).
    En CI/CD y en contenedor, BASE_URL se sobreescribe (ver .env, GitHub Actions, Jenkinsfile).
    """

    base_url: str = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    timeout: float = float(os.getenv("TEST_TIMEOUT", "5"))


settings = Settings()
