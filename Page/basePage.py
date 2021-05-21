from Common.AndroidMessage import Android
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import selenium.common.exceptions as E
from selenium.webdriver.common.by import By
import time
import os
import allure
from loguru import logger
from selenium.webdriver.remote.webelement import WebElement

logger.add(os.path.abspath(os.path.join(os.path.dirname(__file__), f"../reports/log/auto.log")), encoding='utf-8')


class Base:
    """
    基本页，包含设备的所有所需信息（暂时只支持安卓）
    用来连接页面元素和操作过程的类
    """

    driver = None

    an = Android()  # 初始化设备数据
    android_driver_caps = {'platformName': an.platformName,
                           'platformVersion': an.get_device_version,
                           'deviceName': an.get_device_name[0],  # 第一个设备
                           'appPackage': an.get_app_name,
                           'appActivity': an.get_app_Activity,
                           # 'autoGrantPermissions': True,  # 获取默认权限
                           # "noReset": True,  # 不清空数据
                           # "automationName": "Uiautomator2"  # 使用Uiautomator2
                           }
    """
    ios_driver_caps = {"platformName": "iOS",
                       "platformVersion": "12.1",
                       "bundleId": "com.pundix.wallet",
                       "automationName": "XCUITest",
                       "udid": "72c8074b6e518ba2c4a462a5bbe169f90c802f8c",
                       "deviceName": "“PundiX051”的 iPhone"
                       }
    """

    def __init__(self, driver):
        self.driver = driver

    def find_Element(self, el, mark='') -> WebElement:
        logger.info(f'{mark} 查找元素 {el}')
        try:
            return self.driver.find_element(*el)
        except E.NoSuchElementException as e:
            logger.exception('查找元素失败.', e)
            self.allure_save_img(el[1])  # 找不到元素，截图
            raise

    def find_Elements(self, el, mark=None) -> WebElement:
        logger.info(f'{mark} 查找元素(s) {el}')
        try:
            logger.info(f'els == {self.driver.find_elements(*el)}')
            return self.driver.find_elements(*el)
        except E.NoSuchElementException as e:
            logger.exception('查找元素(s)失败.', e)
            raise

    def click_element(self, el, mark=None):
        try:
            self.find_Element(el).click()
            logger.info(f'{mark} 点击元素 {el}')
        except E.ElementClickInterceptedException as e:
            logger.exception('点击元素失败.', e)

    def input_element(self, el, text, mark=None):
        try:
            self.find_Element(el).send_keys(text)
            logger.info(f'{mark} 赋值元素 {el}：{text}')
        except:
            logger.exception('元素赋值失败.')

    def clear_element(self, el, mark=None):
        try:
            self.find_Element(el).clear()
            logger.info(f'{mark} 清除元素值 {el}')
        except:
            logger.exception('元素值清理失败.')
            logger.warning('尝试更改清理元素方法: self.clear_Text')
            self.clear_text(el)

    def sys_back(self):
        """点击系统返回键"""
        logger.info('点击系统返回键')
        self.driver.keyevent(4)

    def sys_home(self):
        """点击系统home键"""
        logger.info('点击系统home键')
        self.driver.keyevent(3)

    def sys_keycode(self, code):
        """点击系统按键"""
        logger.info(f'点击按键 {code}')
        self.driver.keyevent(code)

    def text_in_pagesource(self, text):
        """检查文本是否在page_source里"""
        if text in self.driver.page_source:
            logger.info(f'找到 {text} 文本在页面元素里.')
            return True
        else:
            return False

    def get_size(self):
        """获取屏幕分辨率大小"""
        size = self.driver.get_window_size()
        logger.info(f'屏幕宽度：{size["width"]}, 长度：{size["height"]}')
        return size['width'], size['height']

    def swipe_down(self, duration=500):
        """
        根据屏幕相对大小，向下滑动
        duration: 滑动时间间隔
        """
        logger.info('向下滑动.')
        x, y = self.get_size()
        self.driver.swipe(x / 2, y / 4, x / 2, y * 3 / 4, duration)

    def swipe_up(self, duration=500):
        """
        根据屏幕相对大小，向上滑动
        duration: 滑动时间间隔
        """
        logger.info('向上滑动.')
        x, y = self.get_size()
        self.driver.swipe(x / 2, y * 3 / 4, x / 2, y / 4, duration)

    def Swipe(self, x1, y1, x2, y2, duration=500):
        # 滑动
        x, y = self.get_size()
        self.driver.swipe(x * x1, y * y1, x * x2, y * y2, duration)

    def wait_element(self, duration, frequency, el) -> WebElement:
        """等待元素出现"""
        try:
            ele = WebDriverWait(self.driver, timeout=duration, poll_frequency=frequency).until(
                expected_conditions.presence_of_element_located(el))
            logger.info(f'等待元素{el}出现...时长:{duration}s,间隔:{frequency}s')
            return ele
        except TimeoutError as e:
            logger.exception('查找元素超时.', e)

    def clear_text(self, el):
        """第二种清楚元素的方法"""
        conn = self.find_Element(el)
        conn.click()
        self.driver.keyevent(123)  # 光标追尾
        text_Length = len(str(conn.text))
        logger.info('触发清除元素func 2.')
        for i in range(0, text_Length):
            self.driver.keyevent(67)  # 逐个删除已输入的内容

    def save_img(self, picname):
        """截图并保存"""
        filename = picname + '.png'
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../images/{filename}"))
        logger.exception(f'报错！！！截图路径：： {filepath}')
        self.driver.get_screenshot_as_file(filepath)
        return filepath

    def allure_save_img(self, name):
        """allure截图"""
        with open(self.save_img(name), 'rb') as f:
            file = f.read()
        allure.attach(file, name, allure.attachment_type.PNG)

    def ios_swipe_up(self):
        """iOS端向上滑动"""
        logger.info('向上滑动.')
        self.driver.execute_script('mobile: swipe', {'direction': 'up'})

    def ios_swipe_down(self):
        """iOS端向下滑动"""
        logger.info('向下滑动')
        self.driver.execute_script('mobile: swipe', {'direction': 'down'})

    def is_toast_exist(self, text, duration=5, frequency=0.1):
        """
        定位toast提示语
        :param text: 提示语内容（全部）
        :param duration: 多少秒后超时，不再监控
        :param frequency: 监控间隔
        :return:
        """
        logger.info(f'等待toast {text} 出现...时长:{duration}s,间隔:{frequency}s')
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, duration, frequency).until(
                expected_conditions.presence_of_element_located(toast_loc))
            logger.info(f'找到toast {text}.')
            return True
        except E.NoSuchElementException as n:
            logger.exception('找不到该toast提示.', n)
            return False
        except E.TimeoutException as t:
            logger.exception('等待超时，找不到该toast提示.', t)
            return False

    # def switch_to_view(self, target='H5'):
    #     """
    #     切换app视窗 或 h5视窗
    #     :target:目标视窗（app/H5），默认切换到H5
    #     """
    #
    #     view_list = self.driver.contexts
    #     logger.warning('当前页面的webview元素有：', view_list)
    #     webview = [i for i in view_list if 'app_name' in i]
    #     app = [a for a in view_list if 'APP' in a]
    #
    #     if target == 'H5':
    #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": webview[0]})
    #           logger.warning('切换到H5 view.')
    #     else:
    #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": app[0]})
    #           logger.warning('切换到app view.')
    #     logger.warning(self.driver.current_context)
    #     time.sleep(2)

    def authority(self):
        """授予app系统权限"""
        logger.info('授权弹窗')
        try:
            time.sleep(1)
            if self.find_Element('Allow'):  # 权限询问弹窗
                self.driver.switch_to.alert.accept()  # 系统弹窗默认允许
                self.driver.switch_to.alert.accept()  # 系统弹窗默认允许
            time.sleep(1)
        except:
            logger.warning('没有找到授权弹窗,跳过！')
            pass

    def get_text(self, el) -> str:
        """获取元素text"""
        text = self.find_Element(el).text
        logger.info(f'找到元素的文本：：{text}')
        return text

    def click_text(self, text):
        """点击文本"""
        loc = (By.XPATH, f'//android.widget.TextView[@text="{text}"]')
        self.click_element(loc)

    def element_display(self, el) -> bool:
        """检查元素是否可视"""
        try:
            result = self.find_Element(el).is_displayed()
            logger.info(f'元素 {el} 是否可视： {result}')
            return result
        except:
            return False

    def element_enable(self, el) -> bool:
        """检查元素是否可点击"""
        try:
            result = self.find_Element(el).is_enabled()
            logger.info(f'元素 {el} 是否可点击： {result}')
            return result
        except:
            return False


if __name__ == '__main__':
    print(Base(1).android_driver_caps)
