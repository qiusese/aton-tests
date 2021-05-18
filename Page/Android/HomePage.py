import time

from Page.basePage import Base
from selenium.webdriver.common.by import By


class HomePage(Base):
    """
    首页页面元素
    """

    manage_wallet_btn = (By.ID, 'iv_manage_wallet')
    wallet_address_text = (By.ID, 'tv_address')
    export_privatekey_btn = (By.ID, 'rl_private_key')
    export_keystore_btn = (By.ID, 'rl_keystore')
    wallet_list_btn = (By.ID, 'iv_wallet_switch')
    all_btn = (By.ID, 'btn_all')
    HD_btn = (By.ID, 'btn_hd')
    # normal_btn = (By.ID, 'btn_ordinary')
    wallet_item_btn = (By.ID, 'rl_item')
    edit_name_btn = (By.ID, 'tv_rename')
    pwd_btn = (By.ID, 'et_password')
    confirm_btn = (By.ID, 'button_confirm')
    keystore_text = (By.ID, 'tv_keystore')
    back_btn = (By.ID, 'iv_left')
    privatekey_text = (By.ID, 'tv_private_key')
    edit_name_input = (By.ID, 'et_input_info')
    more_btn = (By.ID, 'iv_assets_add')
    create_wallet_btn = (By.ID, 'll_create_wallet')
    import_wallet_btn = (By.ID, 'll_import_wallet')
    complete_wallet_btn = (By.ID, 'sbtn_finish')
    privatekey_input = (By.ID, 'et_private_key')
    keystore_input = (By.ID, 'et_keystore')
    wallet_name_input = (By.ID, 'et_name')
    pwd_input = (By.ID, 'et_password')
    observer_input = (By.ID, 'et_observed')
    wallet_name_text = (By.ID, 'tv_wallet_name')
    switch_envi_btn = (By.ID, 'iv_node_change')
    envi_name_btn = (By.ID, 'tv_node_name')
    edit_pwd_btn = (By.ID, 'rl_change_password')
    home_backup_wallet_btn = (By.ID, 'rtv_backup_wallet')
    edit_repeat_pwd_input = (By.ID, 'et_repeat_password')
    backup_wallet_btn = (By.ID, 'tv_backup_title')
    next_step_btn = (By.ID, 'sc_next')
    submit_btn = (By.ID, 'sbtn_submit')
    delete_wallet_btn = (By.ID, 'tv_delete')
    cancel_install_btn = (By.ID, 'text_cancel')
    observer_text = (By.ID, 'tv_observed_wallet_tag')

    def cancel_install(self):
        self.click_element(self.cancel_install_btn, mark='跳过升级')

    def get_wallet_msg(self, pwd) -> dict:
        # 获取钱包的地址、私钥、keystore、助记词
        wallet_msg = {'address': '', 'private_key': '', 'keystore': '', 'mnen': ''}

        self.click_element(self.manage_wallet_btn, mark='钱包管理')
        wallet_msg['address'] = self.get_text(self.wallet_address_text)
        self.click_element(self.back_btn, mark='返回')
        wallet_msg['private_key'] = self.export_private_key(pwd)
        wallet_msg['keystore'] = self.export_keystore(pwd)
        wallet_msg['mnen'] = self.export_mnemonic(pwd)
        return wallet_msg

    def export_mnemonic(self, pwd) -> list:
        # 导出助记词
        if self.element_display(self.home_backup_wallet_btn):  # 如果首页有备份按钮
            self.click_element(self.home_backup_wallet_btn, mark='点击首页的备份按钮')
        else:
            self.click_element(self.manage_wallet_btn, mark='钱包管理')
            self.click_element(self.backup_wallet_btn, mark='点击备份助记词')
        self.pwd_author(pwd)

        words = []  # 收集助记词
        for i in range(1, 13):
            mnemonic = (By.ID, f'tv_mnemonic{i}')
            loc_text = self.get_text(mnemonic)  # 获取助记词的值
            words.append(loc_text)
        self.click_element(self.next_step_btn, mark='下一步')
        time.sleep(1)
        return words

    def delete_wallet(self, pwd):
        # 删除钱包
        self.click_element(self.delete_wallet_btn, mark='删除钱包')
        self.pwd_author(pwd)

    def backup_wallet(self, pwd):
        # 备份钱包
        words = self.export_mnemonic(pwd)

        for i in words:
            self.click_text(i)  # 点击助记词
            time.sleep(0.2)
        self.click_element(self.submit_btn, mark='完成备份')
        self.click_element(self.confirm_btn, mark='我知道了')

    def export_private_key(self, pwd) -> str:
        # 导出私钥
        try:
            self.wait_element(el=self.manage_wallet_btn, duration=10, frequency=0.4).click()
            self.wait_element(el=self.export_privatekey_btn, duration=10, frequency=0.4).click()
        except:
            self.click_element(self.manage_wallet_btn, mark='钱包管理')
            self.click_element(self.export_privatekey_btn, mark='导出keystore')
        self.pwd_author(pwd)
        text_loc = self.get_text(self.privatekey_text)
        self.back_homepage()
        return text_loc

    def export_keystore(self, pwd) -> str:
        # 导出keystore
        self.click_element(self.manage_wallet_btn, mark='钱包管理')
        self.click_element(self.export_keystore_btn, mark='导出keystore')
        self.pwd_author(pwd)
        text_loc = self.get_text(self.keystore_text)
        self.back_homepage()
        return text_loc

    def pwd_author(self, pwd):
        # 输入密码验证
        self.input_element(self.pwd_btn, pwd, mark='输入密码')
        self.click_element(self.confirm_btn, mark='确认')
        time.sleep(1)
        if self.element_display(self.confirm_btn):
            self.click_element(self.confirm_btn, mark='我知道了')

    def back_homepage(self):
        # 返回主页
        self.click_element(self.back_btn, mark='返回')
        time.sleep(0.5)
        self.click_element(self.back_btn, mark='返回')

    def traverse_HDwallet_privatekey(self, pwd):
        """遍历HD钱包的私钥"""
        for i in range(6):
            self.click_element(self.wallet_list_btn, mark='选择钱包')
            self.wait_element(el=self.HD_btn, duration=2, frequency=0.4).click()
            try:
                hd_list = self.find_Elements(self.wallet_item_btn, mark='找出当前页面的HD钱包list')
                hd_list[i].click()
            except IndexError:
                pass
            # time.sleep(1)
            yield self.export_private_key(pwd)

    def traverse_HDwallet_keystore(self, pwd):
        """遍历HD钱包的keystore"""
        for i in range(6):
            self.click_element(self.wallet_list_btn, mark='选择钱包')
            self.wait_element(el=self.HD_btn, duration=2, frequency=0.4).click()
            try:
                hd_list = self.find_Elements(self.wallet_item_btn, mark='找出当前页面的HD钱包list')
                hd_list[i].click()
            except IndexError:
                pass
            # time.sleep(1)
            yield self.export_keystore(pwd)

    def swipe_wallet_list(self):
        """HD钱包地址列表下，滑动"""
        self.click_element(self.wallet_list_btn, mark='选择钱包')
        self.wait_element(el=self.HD_btn, duration=2, frequency=0.4).click()
        self.swipe_up(duration=1000)
        time.sleep(2)

    def import_by_privatekey(self, pkey):
        # 导入私钥
        self.import_wallet()
        self.click_text('私钥')
        self.input_element(self.privatekey_input, pkey, mark='输入私钥')

    def import_by_keystore(self, name, keystore, pwd):
        # 导入keystore
        self.import_wallet()
        self.click_text('钱包文件(.json)')
        self.input_element(self.keystore_input, keystore, mark='输入keystore')
        self.input_element(self.wallet_name_input, name, mark='输入钱包名')
        self.input_element(self.pwd_input, pwd, mark='输入密码')

    def import_by_observer(self, addr):
        # 导入观察者钱包
        self.click_text('观察钱包')
        self.input_element(self.observer_input, addr, mark='输入观察者地址')
        self.click_element(self.complete_wallet_btn, mark='点击完成')
        if self.is_toast_exist('钱包已存在'):
            print('钱包已存在！！！请勿重复导入.')
            self.click_element(self.back_btn, mark='返回首页')

    def create_wallet(self):
        # 首页-创建钱包
        self.click_element(self.more_btn, mark='点击更多')
        self.click_element(self.create_wallet_btn, mark='创建钱包')

    def import_wallet(self):
        # 首页-导入钱包
        self.click_element(self.more_btn, mark='点击更多')
        self.click_element(self.import_wallet_btn, mark='导入钱包')

    def edit_name(self, name):
        # 修改钱包名字
        self.click_element(self.manage_wallet_btn, mark='钱包管理')
        self.click_element(self.edit_name_btn, mark='修改钱包名字')
        self.input_element(self.edit_name_input, name, mark='输入钱包名')
        self.click_element(self.confirm_btn, mark='确认')
        self.click_element(self.back_btn, mark='返回')

    def get_wallet_name(self):
        # 返回钱包名字
        return self.get_text(self.wallet_name_text)

    def edit_password(self, old_pwd, new_pwd):
        # 修改钱包密码
        self.click_element(self.manage_wallet_btn, mark='钱包管理')
        self.click_element(self.edit_pwd_btn, mark='修改密码')
        self.input_element(self.pwd_btn, old_pwd, mark='输入老的密码')
        self.click_element(self.confirm_btn, mark='确认')

        self.input_element(self.pwd_btn, new_pwd, mark='输入新的密码')
        self.input_element(self.edit_repeat_pwd_input, new_pwd, mark='确认密码')
        self.click_element(self.confirm_btn, mark='确认')

    def cancel_backup(self):
        # 取消备份钱包
        self.click_element(self.back_btn, mark='返回')
        self.click_element(self.confirm_btn, mark='确定')

    def check_observer_tag(self):
        # 检测是否是观察者钱包
        return self.element_display(self.observer_text)

    # def switch_envi(self, enviroment):
    #     """切换环境，默认platon主网"""
    #     time.sleep(1)
    #     self.click_element(self.switch_envi_btn, mark='切换环境')
    #     env_list = self.find_Elements(self.envi_name_btn, mark='环境列表')
    #     try:
    #         if enviroment == 1:
    #             env_list[0].click()
    #             self.click_element(self.back_btn, mark='返回')
    #         elif enviroment == 3:
    #             env_list[2].click()
    #         else:
    #             env_list[1].click()
    #     except BaseException:
    #         pass
