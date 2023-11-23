import json
import asyncio
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("file:///Users/libojian/Desktop/yshome.html", timeout=4000000)

    page.get_by_placeholder("Agent Code").click()
    page.get_by_placeholder("Agent Code").fill("uhojes")

    # 遍历所有的option元素，获取value和text
    houseList = []

    # 获取所有的option元素
    page.wait_for_selector('#suite')
    options = page.query_selector_all('#city option')

    for option in options:
        city = page.evaluate('(option) => option.value', option)
        city_name = page.evaluate('(option) => option.textContent', option)
        page.locator("#city").select_option(city)

        print(city, city_name)
        page.wait_for_selector('#suite')
        # 获取所有的option元素
        options = page.query_selector_all('#suite option')

        # 遍历所有的option元素，获取value和text
        for opt in options:
            suite_id = page.evaluate('(option) => option.value', opt)
            property_name = page.evaluate('(option) => option.textContent', opt)
            print(suite_id, property_name)
            houseList.append(
                {'city_code': city, 'city_name': city_name, 'suite_id': suite_id, 'property_name': property_name})


    # 将列表转换为JSON格式，并写入到一个文件中
    with open('YSuitesHouse.json', 'w') as f:
        json.dump(houseList, f)

    # 将列表转换为DataFrame
    df = pd.DataFrame(houseList)

    # 将DataFrame写入到Excel文件
    df.to_excel('YSuitesHouse.xlsx', index=False)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    run('PyCharm');
