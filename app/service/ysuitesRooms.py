import json
import asyncio
import pandas as pd
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # 定义传参数据
    timeout = 30000
    agent_code = 'uhomes'
    # url = 'https://www.ysuites.co/agent-login/'
    # url = 'file:///Users/libojian/Desktop/house.html'

    print('step:0.start')
    # 打开第一个页面
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # page.goto(url, timeout=timeout)

    # page.fill('#agent_code', agent_code)
    # 等待元素出现并可见
    # with page.expect_navigation(timeout=timeout):
    #     page.click('.agent_submit_button')

    # page.goto("https://www.ysuites.co/suites/y-suites-on-moore/")

    # 获取房型信息
    houses = [
        {'city_name': 'Adelaide ', 'property_name': 'Y Suites City Gardens',
         'property_url': 'https://www.ysuites.co/suites/y-suites-city-gardens/'},
        {'city_name': 'Canberra ', 'property_name': 'Y Suites on Moore',
         'property_url': 'https://www.ysuites.co/suites/y-suites-on-moore/'},
        {'city_name': 'Sydney ', 'property_name': 'Y Suites on Gibbons',
         'property_url': 'https://www.ysuites.co/suites/y-suites-on-gibbons/'},
        {'city_name': 'Melbourne ', 'property_name': 'Y Suites on A’Beckett',
         'property_url': 'https://www.ysuites.co/suites/y-suites-on-abeckett/'},
        {'city_name': 'Adelaide ', 'property_name': 'Y Suites on Waymouth',
         'property_url': 'https://www.ysuites.co/suites/y-suites-waymouth/'}
    ]

    house_rooms = []
    # step:2.check room-types
    # page.wait_for_selector('#page_id')
    # options = page.query_selector_all('#page_id option')
    # for option in options:
    #     property_url = page.evaluate('(option) => option.value', option)
    #     property_name = page.evaluate('(option) => option.textContent', option)
    #     if property_url == '':
    #         property_url = page.url
    #     houses.append({'property_name': property_name, 'property_url': property_url})

    # 循环房源
    for house in houses:
        # 获取房源名称
        property_name = house['property_name']
        # 获取房源URL
        property_url = house['property_url']
        city_name = house['city_name']
        print(property_name, property_url)
        # 打开房源页面
        page.goto(property_url, timeout=timeout)
        page.get_by_role("tab", name="Room Types").click()
        # 获取所有的.cell.room元素
        rooms = page.query_selector_all('.cell.room')
        # 遍历所有的.cell.room元素，获取每个元素的信息
        for room in rooms:
            room_title = page.evaluate('(room) => room.querySelector(".room-title").textContent', room)
            room_detail_btn = page.evaluate('(room) => room.querySelector(".room-detail-btn a").href', room)
            # 将数据压入列表
            room_json = {'city_name': city_name, 'property_name': property_name, 'room_title': room_title,
                         'room_url': room_detail_btn,
                         'property_url': property_url}
            print(room_json)
            house_rooms.append(room_json)
        print(property_name, 'end...')

    # 将列表转换为JSON格式，并写入到一个文件中
    with open('YSuitesRooms.json', 'w') as f:
        json.dump(house_rooms, f)

    # 将列表转换为DataFrame
    df = pd.DataFrame(house_rooms)

    # 将DataFrame写入到Excel文件
    df.to_excel('YSuitesRooms.xlsx', index=False)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    run('PyCharm');
