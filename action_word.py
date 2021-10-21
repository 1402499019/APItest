import pytest, os, allure, configparser, time
from config.logConfig import logger
from config.httpConfig import HttpConfig
from utils import excelUtil
from pytest_assume.plugin import assume

config = configparser.ConfigParser()
config.read("./config/config.ini", encoding="utf-8")

logger = logger()

excel = excelUtil.Excel(filepath=config["filepath"]["testcase_filepath"])

# 读取一个测试用例，斌以list形式返回

def read_one_line(row):

    # 行、列都是从1开始的
    api_name = excel.get_cell(row=row, col=int(config["excel_col"]["api_name_col"]))
    method = excel.get_cell(row=row, col=int(config["excel_col"]["method_col"]))
    if method.lower() not in ["post", "get", "put", "delete"]:
        logger.error(f"接口{api_name}请求方法：{method}错误！")
    api_url = excel.get_cell(row=row, col=int(config["excel_col"]["api_url_col"]))
    headers = excel.get_cell(row=row, col=int(config["excel_col"]["headers_col"]))
    body = excel.get_cell(row=row, col=int(config["excel_col"]["body_col"]))

    return [api_name, method, api_url, headers, body]

# 读取所有用例，放在列表data中，工参数化
def data_list():
    data = []
    for module_row in range(2,5): # 写死模块行数，后期也可写活
        excel.get_sheet(sheetname="模块")
        module_name = excel.get_cell(row=module_row, col=1)
        if module_name is None:
            break
        # 打开模块sheet页
        excel.get_sheet(sheetname=module_name)
        rows = excel.get_rows()

        # 单个用例，包含：module_name, row, api_url, method, api_url, headers, body
        for row in range(2,rows + 1):
            data.append([module_name,row] + read_one_line(row))
        return data

# 写结果
def write_result(module_name, row, resp, code):
    try:
        status = resp.status_code
        # 写入状态码
        excel.set_cell(module_name,row,col=int(config["excel_col"]["act_status_code_col"]), value=status)

        # 写入code值
        excel.set_cell(module_name, row, col=int(config["excel_col"]["act_code_col"]), value=code)

        # 写入执行结果
        excel.set_cell(module_name, row, col=int(config["excel_col"]["result_col"]), value="PASS" if code == "1" else "FAILED")

        # 写入执行人
        excel.set_cell(module_name, row, col=int(config["excel_col"]["tester_col"]), value=code)
        # 写入返回值
        excel.set_cell(module_name, row, col=int(config["excel_col"]["resp_text_col"]), value=resp.text)
    except Exception:
        raise Exception("系统异常！")

# 参数化
@allure.feature("机器人")
@allure.title("接口{api_name}通过性验证")
@pytest.mark.parametrize("module_name, row, api_name, method, api_url, headers, body",data_list())
def test_num(module_name, row, api_name, method, api_url, headers, body):
    http = HttpConfig()
    with allure.step(f"执行模块\"{module_name}\"用例{row-1}:{api_name}"):
        logger.info(f"执行模块\"{module_name}\"用例{row-1}:{api_name}")
        exec = f"http.{method}(api_url=\"{api_name}\", headers={headers}, body={body})"

        # 执行用例
        resp = eval(exec)

        if resp.status_code == 200:
            code = resp.json()["code"]
        else:
            code = "105"

        # 断言
        assume(code == "1")

        # 写结果
        write_result(module_name,row, resp, code)