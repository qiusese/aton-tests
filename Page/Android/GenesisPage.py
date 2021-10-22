from Page.basePage import Base
from selenium.webdriver.common.by import By
import time


class GenesisPage(Base):
    """
    创建钱包页面
    """

    check_contract_btn = (By.ID, 'ck_agreement')
    confirm_contract_btn = (By.ID, 'sbtn_next')
    switch_env_btn = (By.ID, 'layout_node_setting')
    env_btn = (By.ID, 'tv_node_name')
    observer_input = (By.ID, 'et_observed')
    collect_btn = (By.ID, 'tv_title')
    create_wallet_btn = (By.ID, 'sc_create_wallet')
    import_wallet_btn = (By.ID, 'sc_import_wallet')
    wallet_type_btn = (By.ID, 'tv_wallet_type')
    normal_wallet_btn = (By.ID, 'tv_switch_ordinary')
    HD_wallet_btn = (By.ID, 'tv_switch_hd')
    left_back_btn = (By.ID, 'iv_left')
    wallet_name_input = (By.ID, 'et_name')
    privatekey_input = (By.ID, 'et_private_key')
    pwd_input = (By.ID, 'et_password')
    confirm_pwd_input = (By.ID, 'et_repeat_password')
    set_address_btn = (By.ID, 'iv_wallet_address_select')
    complete_create_btn = (By.ID, 'sbtn_create')
    complete_import_btn = (By.ID, 'sbtn_import')
    keystore_input = (By.ID, 'et_keystore')
    start_backup_btn = (By.ID, 'sc_start_backup')
    skip_backup_btn = (By.ID, 'll_skip')
    confirm_btn = (By.ID, 'button_confirm')
    next_step_btn = (By.ID, 'sc_next')
    complete_wallet_btn = (By.ID, 'sbtn_finish')
    mnemonic_btn = (By.ID, 'et_mnemonic1')
    iv_guide_btn = (By.ID, 'iv_guide')

    def finish_contract(self, con=True):
        # 第一步：勾选协议
        time.sleep(3)
        if con:
            self.click_element(self.check_contract_btn, mark='勾选协议')
            self.click_element(self.confirm_contract_btn, mark='继续')

    def create_wallet(self):
        # 第二步：创建钱包
        time.sleep(0.5)
        self.click_element(self.create_wallet_btn, mark='创建钱包')

    def import_wallet(self):
        # 第二步：导入钱包
        self.click_element(self.import_wallet_btn, mark='导入钱包')
        time.sleep(0.5)
        # self.driver.tap([(234, 324), (438, 561)], 500)  # 点击屏幕
        self.click_element(self.iv_guide_btn, mark='点击引导图蒙层-知道了')

    def wallet_msg(self, name, pwd, HD=False, book=True, source=False):
        """
        :param HD: 是否硬钱包
        :param book: 是否加入地址簿
        :param source: 是否从首页添加
        :return:
        """
        # 第三步：钱包信息
        self.select_wallet_type(HD)
        self.input_element(self.wallet_name_input, name, mark='输入钱包名')
        self.input_element(self.pwd_input, pwd, mark='输入密码')
        if not source:
            self.input_element(self.confirm_pwd_input, pwd, mark='确认密码')
        self.add_address_book(book)

    def finish_create_wallet(self):
        # 第四步：完成创建
        self.click_element(self.complete_create_btn, mark='完成创建钱包')

    def select_wallet_type(self, HD):
        # 选择钱包类型
        if HD:
            self.click_element(self.wallet_type_btn, mark='选择钱包类型')
            self.click_element(self.HD_wallet_btn, mark='选择HD钱包')

    def add_address_book(self, book):
        # 添加到钱包地址簿
        if not book:
            self.click_element(self.set_address_btn, mark='不存入地址簿')

    def backup_wallet(self, pwd=None, skip=True):
        # 备份钱包
        if skip:
            self.click_element(self.skip_backup_btn, mark='跳过备份钱包')
        else:
            self.click_element(self.start_backup_btn, mark='备份钱包')
            self.input_element(self.pwd_input, pwd, mark='输入密码')
            self.click_element(self.confirm_btn, mark='确认')
            self.click_element(self.confirm_btn, mark='我知道了')
            self.click_element(self.next_step_btn, mark='下一步')
            # 输入助记词

    def input_mnemonics(self, words: list):
        # 输入助记词
        # self.click_element(self.import_wallet_btn, mark='导入钱包')
        # self.click_element(self.iv_guide_btn, mark='点击引导图蒙层-知道了')
        for i in range(len(words)):
            mnemonic = (By.ID, f'et_mnemonic{i + 1}')
            self.input_element(mnemonic, words[i], mark='输入12个助记词')
            time.sleep(0.2)

    def input_privatekey(self, pkey):
        # 输入私钥
        self.click_text('私钥')
        self.input_element(self.privatekey_input, pkey, mark='输入私钥')

    def input_keystore(self, ks):
        # 输入Keystore
        self.click_text('钱包文件')
        self.input_element(self.keystore_input, ks, mark='输入keystore')

    def input_observer(self, addr):
        # 导入观察者钱包
        self.click_text('观察钱包')
        self.input_element(self.observer_input, addr, mark='输入观察者地址')
        self.click_element(self.complete_wallet_btn, mark='点击完成')
        if self.is_toast_exist('钱包已存在'):
            print('钱包已存在！！！请勿重复导入.')
            self.click_element(self.left_back_btn, mark='返回首页')

    def finish_import(self):
        # 第四步：完成导入
        self.swipe_up()
        self.click_element(self.complete_import_btn, mark='完成导入')
        if self.is_toast_exist('钱包已存在'):
            print('钱包已存在！！！请勿重复导入.')
            self.click_element(self.left_back_btn, mark='返回首页')

    def switch_env(self, enviroment=1):
        """切换环境，默认platon主网"""
        time.sleep(1)
        self.click_element(self.switch_env_btn, mark='切换环境')
        env_list = self.find_Elements(self.env_btn, mark='环境列表')
        try:
            if enviroment == 1:  # platon主网
                env_list[0].click()
                self.click_element(self.left_back_btn, mark='返回')
            elif enviroment == 3:
                env_list[2].click()  # Alaya主网
            else:
                env_list[1].click()  # platon开发网
        except BaseException:
            pass

    def check_login_success(self):
        # 检测登录成功
        time.sleep(1)
        return self.element_display(self.collect_btn)
