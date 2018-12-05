import asyncio
import time
from pyppeteer.launcher import launch
from alifunc import mouse_slide, input_time_random
from exe_js import js1, js3, js4, js5


async def main(username, pwd, url):
    browser = await launch({'headless': False, 'args': ['--no-sandbox', '--disable-dev-shm-usage'], })
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')

    await page.goto(url)
    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)

    await page.click('#J_Quick2Static')

    await page.type('.J_UserName', username, {'delay': input_time_random() - 50})
    await page.type('#J_StandardPwd input', pwd, {'delay': input_time_random()})
    await page.screenshot({'path': './headless-test-result.png'})
    time.sleep(2)

    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块

    if slider:
        print('出现滑块情况判定')
        await page.screenshot({'path': './headless-login-slide.png'})
        flag = await mouse_slide(page=page)
        if flag:
            await page.click('#J_SubmitStatic')
            await page.waitForNavigation()
            await get_cookie(page)

    else:
        await page.keyboard.press('Enter')
        await page.waitFor(5)
        await page.waitForNavigation()
        try:
            global error
            error = await page.Jeval('.error', 'node => node.textContent')
        except Exception as e:
            error = None
        finally:
            if error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
                await get_cookie(page)
    await browser.close()


# 获取登录后cookie
async def get_cookie(page):
    res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    print(cookies)
    return cookies


if __name__ == '__main__':
    username = 'username'
    pwd = 'password'
    url = 'https://login.taobao.com/member/login.jhtml'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(username, pwd, url))
