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
    transaction_status_text = (By.ID , 'tv_transaction_status_desc')
    delegation_value_text = (By.ID, 'tv_value')
    rewards_amount_text = (By.ID, 'tv_claim_amount')
    spread_reward_btn = (By.ID, 'iv_spread')
    back_btn = (By.ID, 'iv_back')
    confirm_btn = (By.ID, 'button_confirm')

    def choose_index(self, index):
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