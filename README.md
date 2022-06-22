# 接口自动化测试示例

---

## 框架设计

- pytest
- request
- allure

---

## 目录结构

    common                 ——公共类
    config                 ——接口公共参数
    logs                   ——日志打印
    TestCase               ——测试用例
    conftest.py            ——pytest胶水文件
    pytest.ini             ——pytest配置文件

---

## 运行

### 安装依赖

```shell
pip install -r requirements.txt
```

### 执行主文件

* 在项目根目录执行`run_case.py`文件即可运行项目


# allure参数说明


- pytest --alluredir `result-path`
    - --clean-alluredir 清除历史生成记录
- allure generate `result-path`
    - -c 生成报告前删除上一次生成的报告
    - -o 指定生成的报告目录
- allure open `report-path`
- git remote set-url origin https://github.com/caowanliang/request_auto.git
