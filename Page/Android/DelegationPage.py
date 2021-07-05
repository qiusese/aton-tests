from Page.basePage import Base
from selenium.webdriver.common.by import By
import time


class DelegationPage(Base):
    """
    委托页面
    """

    index_btn = (By.ID, 'iv_navigation')
    total_delegation_amount_text = (By.ID, 'tv_total_delegated_amount')
    unclaim_reward_amount_text = (By.ID, 'tv_total_unclaimed_reward_amount')
    delegation_records_btn = (By.ID, 'tv_delegation_rec')
    claim_records = (By.ID, 'tv_claim_rec')
    delegation_tips_btn = (By.ID, 'tv_no_data_tips')
    delegator_detail_btn = (By.ID, 'tv_delegate_detail')
    single_delegation_amount_text = (By.ID, 'tv_delegated_amount')
    single_rewarded_text = (By.ID, 'tv_total_reward_amount')
    single_unclaim_reward_text = (By.ID, 'tv_unclaimed_reward_amount')
    claim_btn = (By.ID, 'layout_claim_reward')
    left_btn = (By.ID, 'iv_left')
    problem_btn = (By.ID, 'll_problem')
    tutorial_btn = (By.ID, 'll_tutorial')
    records_btn = (By.ID, 'll_record_shade')
    delegation_recordes_status_text = (By.ID, 'll_record_shade')
    transaction_status_text = (By.ID, 'tv_transaction_status_desc')
    delegation_value_text = (By.ID, 'tv_value')
    rewards_amount_text = (By.ID, 'tv_claim_amount')
    spread_reward_btn = (By.ID, 'iv_spread')
    back_btn = (By.ID, 'iv_back')
    confirm_btn = (By.ID, 'button_confirm')
    validator_cells_btn = (By.ID, 'cl_shade')
    delegate_btn = (By.ID, 'sbtn_delegate')
    switch_addr_btn = (By.ID, 'iv_arrow')
    delegate_amount_input = (By.ID, 'et_delegate_amount')
    delegate_all_btn = (By.ID, 'tv_all_amount')
    pwd_input = (By.ID, 'et_password')
    delegate_status_text = (By.ID, 'tv_transaction_status_desc')
    claim_rewards_btn = (By.ID, 'tv_claim_reward')
    undelegate_btn = (By.ID, 'tv_undelegate')
    claim_rewards_input = (By.ID, 'et_withdraw_amount')
    withdraw_btn = (By.ID, 'btn_withdraw')
    cofirm_btn = (By.ID, 'sbtn_confirm')

    def choose_index(self, index=1):
        # 点击底部的index
        page_index = self.find_Elements(self.index_btn, mark='底部index')
        page_index[index].click()
        time.sleep(0.5)

    def enter_problem(self):
        # 进入常见问题
        self.click_element(self.problem_btn, mark='点击常见问题')

    def enter_tutorial(self):
        # 进入使用教程
        self.click_element(self.tutorial_btn, mark='进入使用教程')

    def h5page_back(self):
        # 在H5页面返回
        self.click_element(self.back_btn, mark='进入h5页面后，返回')

    def firsttime_into_delegate(self):
        # 第一次进入委托页面
        # self.sys_back()  # 跳过“知道了”提示
        self.driver.tap([(100, 20), (100, 60), (100, 100)], 500)  # 点击屏幕，跳过“知道了”提示
        self.click_element(self.delegation_tips_btn, mark='参与委托')  # 首次点击参与委托
        # self.sys_back()  # 跳过“知道了”提示
        self.driver.tap([(100, 20), (100, 60), (100, 100)], 500)  # 点击屏幕，跳过“知道了”提示

    def findall_validators(self, index='all'):
        # 返回验证人列表
        validators = self.find_Elements(self.validator_cells_btn, mark='验证人列表')
        if index == 'all':
            return validators
        else:
            return validators[index]

    def into_validator_detail(self, index=0):
        # 进入验证人详情页
        self.findall_validators(index).click()

    def delegate(self):
        # 委托
        self.into_validator_detail()
        self.click_element(self.delegate_btn, mark='委托')
        self.driver.tap([(100, 20), (100, 60), (100, 100)], 500)  # 点击屏幕，跳过“知道了”提示

    def delegate_amount(self, amount, pwd, addr=None):
        # 输入委托金额
        # TODO:切换地址
        if addr:
            pass

        if amount == 'all':
            self.click_element(self.delegate_all_btn, mark='委托全部')
            self.click_element(self.confirm_btn, mark='保留余额')
        else:
            self.input_element(self.delegate_amount_input, amount, mark='委托金额')
        self.click_element(self.delegate_btn, mark='委托')
        self.input_element(self.pwd_input, pwd, mark='输入密码')
        self.click_element(self.confirm_btn, mark='确认')

    def get_delegate_result(self):
        # 获取委托后的订单结果
        return self.get_element_value(el=self.delegate_status_text)

    def claim_rewards(self, amount, pwd, index=1):
        # 验证人详情页--领取奖励
        claim_list = self.find_Elements(self.claim_rewards_btn)
        claim_list[index].click()
        time.sleep(0.5)
        self.driver.tap([(100, 20), (100, 60), (100, 100)], 500)  # 点击屏幕，跳过“知道了”提示
        self.input_element(self.claim_rewards_input, mark='领取委托奖励金额')
        self.click_element(self.withdraw_btn, mark='提取奖励')
        self.input_element(self.pwd_input, pwd, mark='输入密码')
        self.click_element(self.confirm_btn, mark='确认')

    def claim_all_rewards(self, pwd, index=1):
        # 验证人详情页--领取奖励（all）
        claim_list = self.find_Elements(self.claim_rewards_btn)
        claim_list[index].click()
        self.click_element(self.confirm_btn, mark='确认')
        self.click_element(self.withdraw_btn, mark='提取奖励')
        self.input_element(self.pwd_input, pwd, mark='输入密码')
        self.click_element(self.confirm_btn, mark='确认')

    def into_validator_node(self):
        # 右划到验证人节点页面
        self.driver.tap([(100, 20), (100, 60), (100, 100)], 500)  # 点击屏幕，跳过“知道了”提示
        self.Swipe(x1=1 / 4, y1=1 / 2, x2=3 / 4, y2=1 / 2)
