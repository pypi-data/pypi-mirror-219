import os
from typing import Callable

import pytest
from loguru import logger


@pytest.fixture
def data_resolver() -> Callable[[str, str], str]:
    def inner(dir: str, file: str):
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, dir, file)
        return config_path

    return inner


@pytest.fixture(scope="session", autouse=True)
def disable_log(request):
    logger.disable("")

    def auto_resource_fin():
        logger.enable("")

    request.addfinalizer(auto_resource_fin)
