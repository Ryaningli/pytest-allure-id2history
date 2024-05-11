from typing import TYPE_CHECKING
from allure_commons.utils import md5
import pytest
if TYPE_CHECKING:
    from allure_pytest.listener import AllureListener


class AllureOverwriteListener:
    def __init__(self, config, allure_listener: 'AllureListener'):
        self.config = config
        self._allure_listener = allure_listener

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_teardown(self, item):
        yield
        # noinspection PyProtectedMember
        uuid = self._allure_listener._cache.get(item.nodeid)
        test_result = self._allure_listener.allure_logger.get_test(uuid)
        test_result.historyId = md5(test_result.fullName, item.callspec.id)
