import time

from Page.basePage import Base
from selenium.webdriver.common.by import By


class TransferPage(Base):
    """
    转账首页页面元素
    """

    assets_id = (By.XPATH,"//*[@resource-id='com.platon.aton:id/tv_assets_name' and @text='LAT']")
    transaction_list = (By.ID,'layout_item_parent')
    send_transaction_btn = (By.ID, 'rtv_send_transaction')
