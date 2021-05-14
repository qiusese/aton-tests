from appium import webdriver
from Page.Android.HomePage import HomePage
from Page.Android.GenesisPage import GenesisPage
from Page.basePage import Base
from data.data import password, privatekey, keystore, observer_address


class TestHome:
    """
    首页用例
    """

    def setup_class(self):
        Base.android_driver_caps["noReset"] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.android_driver_caps)  # 串联
        self.driver.implicitly_wait(5)  # 等待初始化完成
        self.home_page = HomePage(self.driver)
        self.genesis_page = GenesisPage(self.driver)

    def teardown_class(self):
        self.driver.quit()

    def test_01_export_privatekey(self):
        """
        导出钱包私钥
        TODO: 断言
        """
        private_key = self.home_page.export_private_key(password)

    def test_02_export_keystore(self):
        """
        导出助记词
        TODO: 断言
        """
        keystore = self.home_page.export_keystore(password)

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

    def test_05_import_privatekey(self, random_text):
        """首页-通过私钥导入钱包
        TODO： 断言
        """
        self.home_page.import_by_privatekey(pkey=privatekey)
        self.genesis_page.wallet_msg(random_text, password)
        self.genesis_page.finish_import()

    def test_06_import_keystore(self, random_text):
        """首页-通过keystore导入钱包
        TODO： 断言
        """
        self.home_page.import_by_keystore(random_text, dict(keystore), password)
        self.genesis_page.finish_import()

    def test_07_import_observer(self):
        """导入观察者钱包
        TODO： 断言
        """
        self.home_page.import_wallet()
        self.home_page.import_by_observer(addr=observer_address)

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

    def test_10_edit_wallet_pwd(self):
        """修改钱包密码"""
        self.home_page.edit_password(old_pwd=password, new_pwd=password)
        assert self.home_page.element_display(self.home_page.export_privatekey_btn) is True

    def test_11_backup_wallet(self):
        """备份钱包"""
        self.home_page.backup_wallet(password)
        assert self.home_page.element_display(self.home_page.delete_wallet_btn) is True

    def test_12_delete_wallet(self):
        """删除钱包
        TODO: 断言"""
        self.home_page.delete_wallet_btn()
