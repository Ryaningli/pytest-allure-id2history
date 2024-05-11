from pytest_allure_id2history.listener import AllureOverwriteListener
import pytest


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    allure_listener = config.pluginmanager.get_plugin('allure_listener')
    if allure_listener:
        config.pluginmanager.register(
            AllureOverwriteListener(config, allure_listener),
            'allure_overwrite_history_id_listener'
        )
