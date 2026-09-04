from collections.abc import Iterator

import httpx
import pytest

from tests.config import settings


@pytest.fixture(scope="session")
def api_client() -> Iterator[httpx.Client]:
    """Cliente HTTP compartido por toda la sesión de tests.

    Apunta a settings.base_url — local, contenedor o CI según BASE_URL.
    No importa nada de `app`: los tests son caja negra, tal y como se
    probaría una API ya desplegada.
    """
    limits = httpx.Limits(max_keepalive_connections=0)
    with httpx.Client(
        base_url=settings.base_url, timeout=settings.timeout, limits=limits
    ) as client:
        yield client
