from appium import webdriver
from Page.Android.HomePage import HomePage
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
from data.data import password, privatekey, keystore, observer_address, observer_address1, words
import time


class TestHome:
    """
    首页用例
    """

    def setup_class(self):
        Base.android_driver_caps["noReset"] = False
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.home_page = HomePage(self.driver)
        self.genesis_page = GenesisPage(self.driver)
        # 导入观察钱包
        self.genesis_page.finish_contract()
        self.genesis_page.import_wallet()
        self.genesis_page.input_observer(observer_address)


    def teardown_class(self):
        self.driver.quit()

    def test_01_export_privatekey(self, random_text):
        """
        导入、导出钱包私钥
        """
        # 通过私钥导入钱包
        self.home_page.import_wallet()
        self.genesis_page.input_privatekey(privatekey)
        self.genesis_page.wallet_msg(name=random_text, pwd=password)
        self.genesis_page.finish_import()
        # 导出钱包私钥
        private_key = self.home_page.export_private_key(password)
        assert privatekey == private_key

    def test_02_export_keystore(self, random_text):
        """
        导入、导出钱包文件
        TODO: 断言
        """
        # 通过keystore导入钱包
        self.home_page.import_wallet()
        self.genesis_page.input_keystore(keystore)
        self.genesis_page.wallet_msg(name=random_text, pwd=password, source=True)
        self.genesis_page.finish_import()
        # 导出钱包文件
        keystore_export = self.home_page.export_keystore(password)
        # assert keystore == keystore_export

    def test_03_traverse_HDwallet_privatekey(self):
        """
        1.遍历HD钱包30个地址
        2.导出其地址的私钥
        TODO：滑动动作太大，导致会少遍历几个地址
        """
        for j in range(5):
            for i in self.home_page.traverse_HDwallet_privatekey(password):
                pass
            self.home_page.swipe_wallet_list()

    def test_04_traverse_HDwallet_keystore(self):
        """
        1.遍历HD钱包30个地址
        2.导出其地址的keystore
        TODO：滑动动作太大，导致会少遍历几个地址
        """
        for j in range(5):
            for i in self.home_page.traverse_HDwallet_keystore(password):
                pass
            self.home_page.swipe_wallet_list()

    def test_07_import_observer(self):
        """导入观察者钱包
        TODO： 断言
        """
        self.home_page.import_wallet()
        self.home_page.import_by_observer(addr=observer_address1)


    def test_08_create_without_name(self):
        """
        创建钱包，不输入钱包名字
        预期：创建按钮不可点击
        """
        try:
            self.home_page.create_wallet()
            self.genesis_page.wallet_msg(name='', pwd=password)
            assert self.genesis_page.element_enable(self.genesis_page.complete_create_btn) is False
        finally:
            self.home_page.sys_back()

    def test_09_edit_wallet_name(self):
        """修改钱包名字"""
        name = 'new'
        self.home_page.edit_name(name)
        assert self.home_page.get_wallet_name() == name

    def test_10_edit_wallet_pwd(self, random_text):
        """修改钱包密码"""
        # 通过私钥导入钱包
        self.home_page.import_wallet()
        self.genesis_page.input_privatekey(privatekey)
        self.genesis_page.wallet_msg(name=random_text, pwd=password)
        self.genesis_page.finish_import()

        self.home_page.edit_password(old_pwd=password, new_pwd=password)
        assert self.home_page.element_display(self.home_page.change_password_success_text) is True


    def test_11_backup_wallet(self, random_text):
        """备份钱包助记词"""
        self.home_page.import_wallet()
        self.genesis_page.input_mnemonics(list(words))
        self.genesis_page.wallet_msg(name=random_text, pwd=password)
        self.genesis_page.finish_import()
        assert self.genesis_page.check_login_success() is True
        self.home_page.backup_wallet(password)
        assert self.home_page.element_display(self.home_page.delete_wallet_btn) is True

    def test_12_delete_wallet(self, random_text):
        """删除钱包
        TODO: 断言"""
        # 通过私钥导入钱包
        self.home_page.import_wallet()
        self.genesis_page.input_privatekey(privatekey)
        self.genesis_page.wallet_msg(name=random_text, pwd=password)
        self.genesis_page.finish_import()
        time.sleep(2)

        self.home_page.delete_wallet(pwd=password)
