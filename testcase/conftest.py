import string
import random
import pytest


@pytest.fixture()
def random_text():
    return ''.join(random.sample(string.ascii_letters + string.digits, 6))
