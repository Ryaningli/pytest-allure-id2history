from typing import TYPE_CHECKING
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
        if hasattr(item, 'callspec'):
            case_id = item.callspec.id
            # noinspection PyProtectedMember
            uuid = self._allure_listener._cache.get(item.nodeid)
            test_result = self._allure_listener.allure_logger.get_test(uuid)
            if hasattr(test_result, 'historyId'):
                from allure_commons.utils import md5
                test_result.historyId = md5(test_result.fullName, case_id)
