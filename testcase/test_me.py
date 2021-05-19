import allure
from appium import webdriver
from Page.Android.DelegationPage import DelegationPage
from Page.basePage import Base
import pytest


@allure.story('测试')
@pytest.mark.skip('测试')
class TestDelegation:
    """
    委托用例
    """

    def setup_class(self):
        Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.delegation_page = DelegationPage(self.driver)

    def teardown_class(self):
        self.driver.quit()

    def test_01(self):
        self.delegation_page.allure_save_img('测试截图')