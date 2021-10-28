from appium import webdriver
from Page.Android.DelegationPage import DelegationPage
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
from data.data import password
import time


class TestDelegation:
    """
    委托用例
    """

    def setup_class(self):
        Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.delegation_page = DelegationPage(self.driver)
        self.genesis_page = GenesisPage(self.driver)
        self.delegation_page.choose_delegate_index()


    def teardown_class(self):
        self.driver.quit()

    def test_01_no_delegation(self):
        """
        未进行过任何委托的用户
        预期结果：出现参与委托tips按钮
        """
        self.delegation_page.choose_index(1)
        assert self.delegation_page.element_display(self.delegation_page.delegation_tips_btn) is True

    def test_02_enter_problem(self):
        """进入常见问题页面"""
        self.delegation_page.choose_index(1)
        try:
            self.delegation_page.enter_problem()
            assert self.delegation_page.text_in_pagesource('委托人常见问题') is True
        finally:
            self.delegation_page.h5page_back()

    def test_03_enter_tutorial(self):
        """进入使用教程页面"""
        self.delegation_page.choose_index(1)
        try:
            self.delegation_page.enter_tutorial()
            assert self.delegation_page.text_in_pagesource('提交请求') is True
        finally:
            self.delegation_page.h5page_back()

    def test_04_delegate(self):
        """委托"""
        self.delegation_page.choose_nodelist_tab()
        self.delegation_page.findall_validators()
        self.delegation_page.into_validator_detail()
        self.delegation_page.delegate()
        self.delegation_page.delegate_amount(amount=10, pwd=password)
        msg = self.delegation_page.get_transaction_status_text()
        assert msg == "确认中"

    def test_05_claim_rewards(self):
        """领取委托奖励"""
        self.delegation_page.claim_all_rewards(password)
        time.sleep(5)

    def test_06_withdraw(self):
        """赎回委托"""
        self.delegation_page.withdraw(password)
        msg = self.delegation_page.get_transaction_status_text()
        assert msg == "确认中"
