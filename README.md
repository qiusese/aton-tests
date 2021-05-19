## 注意
> 当直接运行run_report.py时，文件的相对路径会更改，如

- z_mock_test.py：：test_02  函数
- basePage.py::save_img 函数
- other.py::set_global_atrr 函数
> 反之，如直接运行z_mock_test.py时，需要更改上述函数的文件路径（'../'）

1. 修改pytest.ini中的--reruns可触发失败用例重跑