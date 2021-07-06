from appium import webdriver
from Page.Android.HomePage import HomePage
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
from data.data import password
from Common.other import set_global_atrr
import pytest
import os, random
import allure


@allure.feature('Aton项目')
@allure.story('Aton导入回归测试')
class TestMock:
    """
    自动化第二期
    """

    def setup_class(self):
        Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.home_page = HomePage(self.driver)
        self.genesis_page = GenesisPage(self.driver)

    def teardown_class(self):
        self.driver.quit()

    @allure.title('platon主网,创建5个普通钱包')
    @pytest.mark.parametrize("HD,w_name,clear,env", [(False, 'mainnet', False, 1)])
    def test_01_create_5wallet(self, random_text, HD, w_name, clear, env):
        """platon主网,创建5个普通钱包"""

        try:
            for i in range(5):
                if i == 0:
                    self.genesis_page.finish_contract()
                    self.genesis_page.switch_env(enviroment=env)
                    self.genesis_page.create_wallet()
                else:
                    self.home_page.create_wallet()
                self.genesis_page.wallet_msg(random_text, password, HD=HD)  # 是否硬钱包
                self.genesis_page.finish_create_wallet()
                self.genesis_page.backup_wallet()
                # self.home_page.cancel_install()  # 取消升级
            assert self.genesis_page.check_login_success() is True

            # 获取钱包的信息，并写入
            # wallet_messages = self.home_page.get_wallet_msg(password)
            # set_global_atrr(w_name, wallet_messages, truncate=clear)  # 设置全局变量
        finally:
            self.genesis_page.allure_save_img('test_01')

    from data import global_var as g  # 导入全局变量

    @allure.title('通过keystore导入成普通钱包')
    @pytest.mark.parametrize("env,source", [(1, g.mainnet_HD)])
    def test_02_import_wallet_by_keystore(self, random_text, env, source):
        """通过keystore导入成普通钱包"""

        try:
            self.home_page.import_by_keystore(random_text, source['keystore'].strip('/'), password)
            assert self.home_page.export_private_key(password) == source['private_key']
        finally:
            self.genesis_page.allure_save_img('test_02')
