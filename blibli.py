import time
import random
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CrackGeetest():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = 'your username'
        self.password = 'your password'

    def __del__(self):
        self.browser.close()

    def open(self):
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        self.cur_url = self.browser.current_url

    def get_slider(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
        return slider

    def get_img_position(self):
        time.sleep(3)
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_box')))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_geetest_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_img_position()
        # print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left*1.25, top*1.25, right*1.25, bottom*1.25))
        # captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 80
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        left = 80
        time.sleep(1)
        for i in range(left, image1.size[0]):
            for j in range(10, image1.size[1]-10):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        print('diatance:', distance)
        track = []
        current = 0
        mid = distance * 5/6
        t = 0.3
        v = 0
        while distance > current:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += round(move)
            track.append(round(move))
        if current > distance:
            track.append(distance - current)
        print('current:', current)
        print('sumtrack:', sum(track))
        return track

    def move_to_gap(self, slider, track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for num in range(len(track)):
            # ActionChains(self.browser).move_by_offset(xoffset=track[num], yoffset=0).perform()
            if len(track) - num <= 2:
                time.sleep(random.uniform(0, 0.3))
                ActionChains(self.browser).move_by_offset(xoffset=track[num], yoffset=0).perform()
            else:
                ActionChains(self.browser).move_by_offset(xoffset=track[num], yoffset=0).perform()
            # print(track[num], slider.location['x'])
        time.sleep(random.uniform(0.2, 0.5))
        ActionChains(self.browser).release().perform()

    # def login(self):
    #     submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
    #     submit.click()
    #     time.sleep(1)
    #     print('登录成功')

    def crack(self):
        self.open()
        slider = self.get_slider()
        ActionChains(self.browser).move_to_element(slider).perform()
        image1 = self.get_geetest_image('captcha1.png')
        slider.click()
        # ActionChains(self.browser).click_and_hold(slider).perform()
        image2 = self.get_geetest_image('captcha2.png')
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        gap -= 6
        track = self.get_track(gap/1.25)
        print('滑动轨迹', track)
        self.move_to_gap(slider, track)
        time.sleep(5)
        if self.cur_url == self.browser.current_url:
            return False
        else:
            return True

if __name__ == "__main__":
    for i in range(3):
        crack = CrackGeetest()
        result = crack.crack()
        if result:
            print('SUCCESS')
            break
        else:
            print('FAIL', str(i+1), 'TIMES')