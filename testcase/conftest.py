import string
import random
import pytest


@pytest.fixture()
def random_text():
    return ''.join(random.sample(string.ascii_letters + string.digits, 6))


def pytest_collection_modifyitems(session: "Session", config: "Config", items) -> None:
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")
