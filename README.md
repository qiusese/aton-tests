# 自动化工具

## 1.框架介绍

![image-20210706102811648](C:\Users\juzix\AppData\Roaming\Typora\typora-user-images\image-20210706102811648.png)

## 2.操作手册

基本只需变更Page文件夹和testcase文件夹的代码即可

### 2.1元素层-添加元素

- 打开appium-start server，点击![image-20210706103246338](C:\Users\juzix\AppData\Roaming\Typora\typora-user-images\image-20210706103246338.png)

- 设置初始设备信息，连接设备如下：

  ```{ "platformName": "Android",
  { "platformVersion": "10",
    "deviceName": "Q5S5T19409006974",
    "appActivity": "component.ui.view.SplashActivity",
    "appPackage": "com.platon.aton"
  }
  ```

- start session，点击![image-20210706103738624](C:\Users\juzix\AppData\Roaming\Typora\typora-user-images\image-20210706103738624.png)

- 鼠标点击对应需要定位的地方，即可看到元素的具体信息

  ```python
  check_contract_btn = (By.ID, 'ck_agreement')
  ```

![image-20210706103852449](C:\Users\juzix\AppData\Roaming\Typora\typora-user-images\image-20210706103852449.png)

### 2.2操作层-创建逻辑方法

常用的方法有：

- click_element(元素变量，mark=操作描述（可不填）)
- input_element(元素变量，输入内容，mark=操作描述（可不填）)
- click_text(需要点击的文本)
- is_toast_exist(toast提示文本)
- element_display(元素变量（判断元素是否显示）)
- swipe_up/swipe_down(（上下滑动屏幕）)

```python
    def finish_import(self):
        # 第四步：完成导入
        self.swipe_up()
        self.click_element(self.complete_import_btn, mark='完成导入')
        if self.is_toast_exist('钱包已存在'):
            print('钱包已存在！！！请勿重复导入.')
            self.click_element(self.left_back_btn, mark='返回首页')
```

### 2.3业务层

即组合操作层的方法，也建议使用链式调用方法方便编写

```python
@allure.title('通过助记词导入成普通钱包')
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
        finally:
            self.home_page.allure_save_img('test_03')
```

- @allure.title(用例名，可选)
- @pytest.mark.parametrize(变量，变量迭代器，ids=自定义用例名（可选）)

- finally：操作后截图（截图名字建议不要重复使用同一个）

## 3.需注意事项

- 3s以内的等待时间，建议使用time.sleep(x)，方便编写；需要轮询元素的则使用is_toast_exist()
- setup_method/teardown_method，每条用例case会先后执行一遍
- setup_class/teardown_class，每个待测试类会先后执行一遍

- testcase/*_mock_test.py主要存放一些需一系列业务操作的冒烟测试用例
- 失败需设置重跑次数时，修改pytest.ini --reruns 数值

## 4.项目完成进度

1. 初始页面元素层-操作层-业务层，100%
2. 首页元素层-操作层-业务层，100%
3. 委托页面元素层-操作层-业务层，20%
4. 冒烟case[z_mock_test.py]第一期，100%
5. 冒烟case[x_mock_test.py]期，15%