import click, allure, pytest, os


@click.command()
@click.option("-m",help= "输入run表示运行模式， 输入debug表示调试模式")
def run(m):
    if m == "run":
        print("run运行：")
        pytest.main(["--reruns", "3", "--reruns-delay", "1", "-s", "-W", "ignore:Module already imported:pytest.PytestWarning",
                     "。/action_word.py", "--clean-alluredir", "--alluredir", "./report/allure_results"])

    elif m =="debug":
        pass

if __name__ == '__main__':
    run()
