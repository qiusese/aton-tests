from appium import webdriver
from Page.Android.HomePage import HomePage
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
from data.data import password
from Common.other import set_global_atrr
import pytest
import os
import allure


@allure.feature('Aton项目')
@allure.story('Aton导入回归测试')
class TestMock:
    """
    自动化第一期
    ：：37条testcase，耗时45mins左右
    """

    def setup_method(self):
        # Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.home_page = HomePage(self.driver)
        self.genesis_page = GenesisPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("HD,w_name,clear,env", [
        (True, 'mainnet_HD', True, 1), (False, 'mainnet', False, 1),
        (True, 'dev_HD', False, 2), (False, 'dev', False, 2),
        (True, 'alaya_HD', False, 3), (False, 'alaya', False, 3)],
                             ids=['platon主网-HD钱包', 'platon主网-普通钱包',
                                  'platon测试网-HD钱包', 'platon测试网-普通钱包',
                                  'alaya网-HD钱包', 'alaya网-普通钱包'])
    def test_01_get_wallet_msg(self, HD, w_name, clear, env):
        """
        三种不同的环境下
        1.获取老版本HD钱包的地址、私钥、助记词、keystore;写入到data.global_var中
        2.获取老版本普通钱包的地址、私钥、助记词、keystore;写入到data.global_var中
        """
        try:
            # 第一步创建一个HD钱包
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.create_wallet()
            self.genesis_page.wallet_msg('test', password, HD=HD)  # 是否硬钱包
            self.genesis_page.finish_create_wallet()
            self.genesis_page.backup_wallet()
            self.home_page.cancel_install()  # 取消升级
            assert self.genesis_page.check_login_success() is True

            # 第二步获取钱包的信息，并写入
            wallet_messages = self.home_page.get_wallet_msg(password)
            set_global_atrr(w_name, wallet_messages, truncate=clear)  # 设置全局变量
        except:
            self.genesis_page.allure_save_img('test_01')

    def test_02_reinstall(self):
        """升级为新版本，覆盖安装"""
        try:
            # self.driver.remove_app(Base.android_driver_caps['appPackage'])
            self.driver.install_app(os.path.abspath(os.path.join(os.getcwd(), "./data/Aton1.0.1.apk")))
            assert self.genesis_page.is_toast_exist('正在自动升级')
        except:
            self.genesis_page.allure_save_img('test_02')

    from data import global_var as g  # 导入全局变量

    @pytest.mark.parametrize("env,source", [
        (1, g.mainnet_HD), (2, g.mainnet_HD),
        (2, g.dev_HD), (1, g.dev_HD),
        (3, g.alaya_HD)],
                             ids=['platon主网->platon主网', 'platon主网->platon开发网',
                                  'platon开发网->platon开发网', 'platon开发网->platon主网',
                                  'alaya网->alaya网'])
    def test_03_import_wallet_by_mnemonic(self, random_text, env, source):
        """
        1.新版本，通过老版本HD钱包的助记词导入(普通)钱包
        预期结果：新老钱包的私钥一致
        """
        try:
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.import_wallet()
            self.genesis_page.input_mnemonics(source['mnen'])
            self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=False)  # 普通钱包
            self.genesis_page.finish_import()
            assert self.home_page.export_private_key(password) == source['private_key']
        except:
            self.home_page.allure_save_img('test_03')

    @pytest.mark.parametrize("env,source", [
        (1, g.mainnet_HD), (2, g.mainnet_HD),
        (2, g.dev_HD), (1, g.dev_HD),
        (3, g.alaya_HD)],
                             ids=['platon主网->platon主网', 'platon主网->platon开发网',
                                  'platon开发网->platon开发网', 'platon开发网->platon主网',
                                  'alaya网->alaya网'])
    def test_04_import_wallet_by_privatekey(self, random_text, env, source):
        """
        1.新版本，通过老版本HD钱包的私钥导入钱包
        预期结果：新老钱包的私钥一致
        """
        try:
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.import_wallet()
            self.genesis_page.input_privatekey(pkey=source['private_key'])
            self.genesis_page.wallet_msg(random_text, password)
            self.genesis_page.finish_import()
            assert self.home_page.export_private_key(password) == source['private_key']
        except:
            self.home_page.allure_save_img('test_04')

    @pytest.mark.parametrize("env,source", [
        (1, g.mainnet_HD), (2, g.mainnet_HD),
        (2, g.dev_HD), (1, g.dev_HD),
        (3, g.alaya_HD)],
                             ids=['platon主网->platon主网', 'platon主网->platon开发网',
                                  'platon开发网->platon开发网', 'platon开发网->platon主网',
                                  'alaya网->alaya网'])
    def test_05_import_wallet_by_keystore(self, random_text, env, source):
        """
        1.新版本，通过老版本HD钱包的keystore导入钱包
        预期结果：新老钱包的私钥一致
        """
        try:
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.import_wallet()
            self.genesis_page.input_keystore(source['keystore'].strip('/'))
            self.genesis_page.wallet_msg(random_text, password, keystore=True)
            self.genesis_page.finish_import()
            assert self.home_page.export_private_key(password) == source['private_key']
        except:
            self.genesis_page.allure_save_img('test_05')

    @pytest.mark.parametrize("env,source", [
        (1, g.mainnet_HD), (2, g.mainnet_HD),
        (2, g.dev_HD), (1, g.dev_HD),
        (3, g.alaya_HD)],
                             ids=['platon主网->platon主网', 'platon主网->platon开发网',
                                  'platon开发网->platon开发网', 'platon开发网->platon主网',
                                  'alaya网->alaya网'])
    def test_06_import_wallet_by_observer(self, env, source):
        """
        1.新版本，通过老版本HD钱包的地址导入观察者钱包
        预期结果：首页备注观察者钱包
        """
        try:
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.import_wallet()
            self.home_page.import_by_observer(addr=source['address'])
            assert self.home_page.check_observer_tag() is True
        except:
            self.genesis_page.allure_save_img('test_06')

    @pytest.mark.parametrize("env,source", [
        (1, g.mainnet_HD), (2, g.mainnet_HD),
        (2, g.dev_HD), (1, g.dev_HD),
        (3, g.alaya_HD)],
                             ids=['platon主网->platon主网', 'platon主网->platon开发网',
                                  'platon开发网->platon开发网', 'platon开发网->platon主网',
                                  'alaya网->alaya网'])
    def test_07_import_HDwallet_by_mnemonic(self, random_text, env, source):
        """
        1.新版本，通过老版本HD钱包的助记词导入成HD钱包(耗时较久)
        2.遍历HD地址的私钥
        TODO：遍历时有问题，会重复1-15两次
        """
        try:
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.import_wallet()
            self.genesis_page.input_mnemonics(source['mnen'])
            self.genesis_page.wallet_msg(name=random_text, pwd=password, HD=True)
            self.genesis_page.finish_import()
            assert self.genesis_page.check_login_success() is True

            for j in range(5):
                for i in self.home_page.traverse_HDwallet_privatekey(password):
                    set_global_atrr(key=f'pri_{i[0:4]}', value=i, truncate=False)
                self.home_page.swipe_wallet_list()
        except:
            self.genesis_page.allure_save_img('test_07')

    @pytest.mark.parametrize("env,source", [
        (1, g.mainnet), (2, g.mainnet),
        (2, g.dev), (1, g.dev),
        (3, g.alaya)],
                             ids=['platon主网->platon主网', 'platon主网->platon开发网',
                                  'platon开发网->platon开发网', 'platon开发网->platon主网',
                                  'alaya网->alaya网'])
    def test_08_normalwallet_to_HDwallet(self, random_text, env, source):
        """
        1.老版本的普通钱包助记词
        2.导入到新版本HD钱包
        预期结果：新老钱包的私钥一致
        """
        try:
            self.genesis_page.finish_contract()
            self.genesis_page.switch_env(enviroment=env)
            self.genesis_page.import_wallet()
            self.genesis_page.input_mnemonics(source['mnen'])
            self.genesis_page.wallet_msg(random_text, password, HD=True)  # 是否硬钱包
            self.genesis_page.finish_import()
            assert self.home_page.export_private_key(password) == source['private_key']
        except:
            self.genesis_page.allure_save_img('test_08')
