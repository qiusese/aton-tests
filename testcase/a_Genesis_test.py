from appium import webdriver
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
import pytest
from data.data import password, words, keystore, privatekey, observer_address


class TestGenesis:
    """
    初始界面用例
    """

    def setup_method(self):
        # Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.genesis_page = GenesisPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("HD", [False, True])
    def test_01_create_wallet_HD(self, random_text, HD):
        """
        1.创建普通钱包
        2.创建HD钱包
        """
        self.genesis_page.finish_contract()
        self.genesis_page.create_wallet()
        self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=HD)
        self.genesis_page.finish_create_wallet()
        self.genesis_page.backup_wallet(password, skip=True)
        assert self.genesis_page.check_login_success() is True

    @pytest.mark.parametrize("HD", [False, True])
    def test_02_import_mnemonic_HD(self, random_text, HD):
        """
        通过助记词words
        1.导入普通钱包
        2.导入HD钱包
        """
        self.genesis_page.finish_contract()
        self.genesis_page.import_wallet()
        self.genesis_page.input_mnemonics(list(words))
        self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=HD)
        self.genesis_page.finish_import()
        assert self.genesis_page.check_login_success() is True

    def test_03_import_keystore(self, random_text):
        """
        通过keysore钱包文件导入钱包
        """
        self.genesis_page.finish_contract()
        self.genesis_page.import_wallet()
        self.genesis_page.input_keystore(keystore)
        self.genesis_page.wallet_msg(name=random_text, pwd=password, source=True)
        self.genesis_page.finish_import()
        # assert self.genesis_page.check_login_success() is True

    def test_04_import_privatekey(self, random_text):
        """
        通过私钥导入钱包
        """
        self.genesis_page.finish_contract()
        self.genesis_page.import_wallet()
        self.genesis_page.input_privatekey(privatekey)
        self.genesis_page.wallet_msg(name=random_text, pwd=password)
        self.genesis_page.finish_import()
        # assert self.genesis_page.check_login_success() is True

    def test_05_import_observer(self):
        """
        导入观察钱包
        """
        self.genesis_page.finish_contract()
        self.genesis_page.import_wallet()
        self.genesis_page.input_observer(observer_address)
        self.genesis_page.finish_import()

    @pytest.mark.parametrize("HD,env", [(False, 1), (False, 2), (False, 3)])
    def test_06_switch_wallet_env(self, random_text, HD, env):
        """
        切换环境，创建钱包
        """
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.create_wallet()
        self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=HD)
        self.genesis_page.finish_create_wallet()
        self.genesis_page.backup_wallet(skip=True)
        assert self.genesis_page.check_login_success() is True
