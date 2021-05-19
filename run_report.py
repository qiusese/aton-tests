from Common.AppiumServer import AppiumServer
import pytest
import os


class RunReport(AppiumServer):
    """运行 & 产生报告"""

    def __init__(self, root='./testcase'):
        # 默认testcase中所有含有test的py脚本
        self.root = root

    def terminal_report(self):
        # 执行测试用例
        pytest.main(['-s', '-v', self.root])  # 在终端运行报告

    def generate_report(self):
        """生成allure报告数据，放到./report/xml下"""
        pytest.main(['-s', '-v', self.root, '--alluredir', './reports/xml'])  # 在终端运行报告
        os.system('allure generate ./reports/xml -o ./reports/html --clean')  # --clean清除上一期数据
        return self

    def open_report(self):
        """生成报告，且用浏览器打开allure报告"""
        # self.generate_report()
        os.system('allure open ./reports/html')  # 启动服务器用allure serve
        return self


if __name__ == '__main__':
    R = RunReport(root=r'C:\Users\juzix\PycharmProjects\ATON-Tests\testcase\z_mock_test.py')
    R.generate_report().open_report()
