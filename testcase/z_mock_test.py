from appium import webdriver
from Page.Android.HomePage import HomePage
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
from data.data import password
from Common.other import set_global_atrr
import pytest
import os


class TestMock:
    """自动化第一期"""

    def setup_method(self):
        # Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.home_page = HomePage(self.driver)
        self.genesis_page = GenesisPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("HD,w_name,clear", [(True, 'name', True), (False, 'dev_name', False)],
                             ids=['HD钱包', '普通钱包'])
    def test_01_get_wallet_msg(self, HD, w_name, clear):
        """
        platon主网
        1.获取新版本HD钱包的地址、私钥、助记词、keystore;写入到data.global_var.name中
        2.获取新版本普通钱包的地址、私钥、助记词、keystore;写入到data.global_var.dev_name中
        """
        # 第一步创建一个HD钱包
        self.genesis_page.finish_contract()
        self.genesis_page.create_wallet()
        self.genesis_page.wallet_msg('test', password, HD=HD)  # 是否硬钱包
        self.genesis_page.finish_create_wallet()
        self.genesis_page.backup_wallet()

        # 第二步获取钱包的信息，并写入
        wallet_messages = self.home_page.get_wallet_msg(password)
        set_global_atrr(w_name, wallet_messages, truncate=clear)  # 全局名

    def test_02_reinstall(self):
        """
        platon主网
        1.卸载新版本
        2.安装老版本
        """
        self.driver.remove_app(Base.android_driver_caps['appPackage'])
        self.driver.install_app(os.path.abspath(os.path.join(os.getcwd(), "../data/Aton1.0.0.apk")))

    @pytest.mark.parametrize("env", [1, 2], ids=['platon主网', 'platon开发网'])
    def test_03_import_wallet_by_mnemonic(self, random_text, env):
        """
        1.platon主网-老版本，通过助记词导入钱包
        2.platon开发-老版本，通过助记词导入钱包
        """
        from data.global_var import name
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.import_wallet()
        self.genesis_page.input_mnemonics(name['mnen'])
        self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=False)
        self.genesis_page.finish_import()
        self.home_page.cancel_install()
        assert self.genesis_page.check_login_success() is True

    @pytest.mark.parametrize("env", [1, 2], ids=['platon主网', 'platon开发网'])
    def test_04_import_wallet_by_privatekey(self, random_text, env):
        """
        1.platon主网-老版本，通过私钥导入钱包
        2.platon开发网-老版本，通过私钥导入钱包
        """
        from data.global_var import name
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.import_wallet()
        self.genesis_page.input_privatekey(pkey=name['private_key'])
        self.genesis_page.wallet_msg(random_text, password)
        self.genesis_page.finish_import()
        self.home_page.cancel_install()
        assert self.genesis_page.check_login_success() is True

    @pytest.mark.parametrize("env", [1, 2], ids=['platon主网', 'platon开发网'])
    def test_05_import_wallet_by_keystore(self, random_text, env):
        """
        1.platon主网-老版本，通过keystore导入钱包
        2.platon开发网-老版本，通过keystore导入钱包
        """
        from data.global_var import name
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.import_wallet()
        self.genesis_page.input_keystore(name['keystore'].strip('/'))
        self.genesis_page.wallet_msg(random_text, password)
        self.genesis_page.finish_import()
        self.home_page.cancel_install()
        assert self.genesis_page.check_login_success() is True

    @pytest.mark.parametrize("env", [1, 2], ids=['platon主网', 'platon开发网'])
    def test_06_import_wallet_by_observer(self, env):
        """
        1.platon主网-老版本，通过地址导入观察者钱包
        2.platon测试网-老版本，通过地址导入观察者钱包
        """
        from data.global_var import name
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.import_wallet()
        self.home_page.import_by_observer(addr=name['address'])
        self.home_page.cancel_install()
        assert self.genesis_page.check_login_success() is True

    @pytest.mark.parametrize("env", [1, 2], ids=['platon主网', 'platon开发网'])
    def test_07_import_HDwallet_by_mnemonic(self, random_text, env):
        """
        1.platon主网-老版本，通过助记词导入成HD钱包
        2.platon测试网-老版本，遍历HD30个钱包地址的私钥
        """
        from data.global_var import name
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.import_wallet()
        self.genesis_page.input_mnemonics(name['mnen'])
        self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=True)
        self.genesis_page.finish_import()
        self.home_page.cancel_install()
        assert self.genesis_page.check_login_success() is True

        for j in range(5):
            for i in self.home_page.traverse_HDwallet_privatekey(password):
                set_global_atrr(key=f'pri_{i[0:4]}', value=i, truncate=False)
            self.home_page.swipe_wallet_list()

    @pytest.mark.parametrize("env", [1, 2], ids=['platon主网', 'platon开发网'])
    def test_08_normalwallet_to_HDwallet(self, random_text, env):
        """
        1.platon主网-老版本，创建一个普通钱包
        1.platon测试网-老版本，创建一个普通钱包
        """
        from data.global_var import dev_name
        self.genesis_page.finish_contract()
        self.genesis_page.switch_env(enviroment=env)
        self.genesis_page.import_wallet()
        self.genesis_page.input_mnemonics(dev_name['mnen'])
        self.genesis_page.wallet_msg(random_text, password, HD=True)  # 是否硬钱包
        self.genesis_page.finish_import()