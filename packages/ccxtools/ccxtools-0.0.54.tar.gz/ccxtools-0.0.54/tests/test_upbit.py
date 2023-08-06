import pytest

from src.ccxtools.tools import get_env_vars
from src.ccxtools.upbit import Upbit


@pytest.fixture
def config():
    return get_env_vars()


@pytest.fixture
def upbit(config):
    return Upbit('', '', config)


def test_get_last_price(upbit):
    price = upbit.get_last_price('BTC')
    assert isinstance(price, float)


def test_get_best_book_price(upbit):
    assert isinstance(upbit.get_best_book_price('BTC', 'ask'), float)
    assert False
