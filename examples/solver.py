#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/2/12 11:20
@Author  : 余半盏
@Email   : 2466857975@@qq.com
@File    : rotate_captcha.py
@Software: PyCharm
"""
import time
import os
import random
import cv2 as cv
import math
import numpy as np


def circle_point_px(img, accuracy_angle, r=None):
    rows, cols, channel = img.shape
    assert 360 % accuracy_angle == 0
    x0, y0 = r0, _ = (rows // 2, cols // 2)
    if r:
        r0 = r
    circle_px_list = []
    for angle in np.arange(0, 360, accuracy_angle):
        # 圆上点 x=x0 + r*cosθ; y=y0 + r*sinθ
        x = x0 + r0 * math.cos(angle / 180 * math.pi)
        y = y0 + r0 * math.sin(angle / 180 * math.pi)
        circle_px_list.append(img[int(x)][int(y)])
    return circle_px_list


def rotate(image, angle, center=None, scale=1.0):  # 1
    (h, w) = image.shape[:2]  # 2
    if center is None:  # 3
        center = (w // 2, h // 2)  # 4

    M = cv.getRotationMatrix2D(center, angle, scale)  # 5

    rotated = cv.warpAffine(image, M, (w, h))  # 6
    return rotated


def HSVDistance(c1, c2):
    y1 = 0.299 * c1[0] + 0.587 * c1[1] + 0.114 * c1[2]
    u1 = -0.14713 * c1[0] - 0.28886 * c1[1] + 0.436 * c1[2]
    v1 = 0.615 * c1[0] - 0.51498 * c1[1] - 0.10001 * c1[2]
    y2 = 0.299 * c2[0] + 0.587 * c2[1] + 0.114 * c2[2]
    u2 = -0.14713 * c2[0] - 0.28886 * c2[1] + 0.436 * c2[2]
    v2 = 0.615 * c2[0] - 0.51498 * c2[1] - 0.10001 * c2[2]
    rlt = math.sqrt(
        (y1 - y2) * (y1 - y2) + (u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2)
    )
    return rlt


def discern(inner_image_brg, outer_image_brg, result_img=None, angle=4, default_dis=5):
    inner_image_brg = cv.imread(inner_image_brg)
    outer_image_brg = cv.imread(outer_image_brg)
    inner_image = cv.cvtColor(inner_image_brg, cv.COLOR_BGR2HSV)
    outer_image = cv.cvtColor(outer_image_brg, cv.COLOR_BGR2HSV)
    all_deviation = []
    for result in range(0, 180):
        inner = rotate(inner_image, -result)  # 顺时针
        outer = rotate(outer_image, result)
        inner_circle_point_px = circle_point_px(
            inner, angle, (inner.shape[0] // 2) - default_dis
        )
        outer_circle_point_px = circle_point_px(
            outer, angle, (inner.shape[0] // 2) + default_dis
        )
        total_deviation = 0
        for i in range(len(inner_circle_point_px)):
            in_px = inner_circle_point_px[i]
            out_px = outer_circle_point_px[i]
            deviation = HSVDistance(in_px, out_px)
            total_deviation += deviation
        all_deviation.append(total_deviation)
    result = all_deviation.index(min(all_deviation))
    print(result)

    if result_img:
        inner = rotate(inner_image_brg, -result)  # 顺时针
        outer = rotate(outer_image_brg, result)
        left_point = outer.shape[0] / 2 - inner.shape[0] / 2
        right_point = outer.shape[0] / 2 + inner.shape[0] / 2
        replace_area = outer[
            int(left_point) : int(right_point), int(left_point) : int(right_point)
        ]
        outer[
            int(left_point) : int(right_point), int(left_point) : int(right_point)
        ] = (replace_area + inner)
        cv.imwrite(result_img, outer)
    return result


def solve_captcha_tiktok(self, code_path, count=0):
    # get inner /outer images
    self.page.goto("https://www.tiktok.com/login/phone-or-email/email")
    self.page.get_by_placeholder("电子邮件或用户名").click()
    self.page.get_by_placeholder("电子邮件或用户名").fill("unboxdoctor@outlook.com")
    self.page.get_by_placeholder("密码").click()
    self.page.get_by_placeholder("密码").click(modifiers=["Control"])
    self.page.get_by_placeholder("密码").fill("95Qa*G*za5Gb")
    self.page.get_by_role("button", name="登录").click()

    # cal rotate angle
    # cal drager distance
    # lets say total drage bar length ==360 rotation angle,
    # self.page.reload()
    t = self.page.locator('img[class^="captcha_verify_img_slide"]')
    if os.path.exists(code_path):
        os.remove(code_path)
    print("detected captcha", t)
    # time.sleep(0.02)
    if count > 8:  # 约15次错误尝试 会报频繁
        self.browser.close()
        self.open_driver()
        return
    try:
        print(
            "detected capatcha image",
        )

        # time.sleep(0.03)

        img = self.page.locator("#captcha_container")
        # ""加不加一样
        print("detected capatcha image", img.get_attribute("src"))
        outerimg = self.page.locator(
            " # captcha_container > div > div.sc-jTzLTM.irVQmi > img.sc-fjdhpX.bKqdsG"
        )

        innerimg = self.page.locator(
            " # captcha_container > div > div.sc-jTzLTM.irVQmi > img.sc-cSHVUG.hmxWbL"
        )

        if img.get_attribute("src"):
            # time.sleep(1)
            # self.page.screenshot(path=code_path, clip=clip)

            print("finished screenshot of slide")

        offsetlist = sorted(list(set(offsetlist)))

        if len(offsetlist) == 0:
            return {"success": 0}
        else:
            source = self.page.locator(".secsdk-captcha-drag-icon").bounding_box()

            for x_offset in offsetlist:
                print("offset is", x_offset)
                x_offset = x_offset - 3
                y_offset = 0
                # action = ActionChains(self.driver)
                steps_count = 5
                box_pos_x = source["x"] + source["width"] / 2
                box_pos_y = source["y"] + source["height"] / 2
                self.page.mouse.move(box_pos_x, box_pos_y)
                # self.page.locator(".secsdk-captcha-drag-icon").click()
                print("move mouse to dragon icon and hold")

                # self.page.mouse.click(box_pos_x, box_pos_y)

                self.page.mouse.down()
                print("holding", x_offset, y_offset)
                L1 = [0.3, 0.24, 0.21, 0.14, 0.11]
                step = (x_offset + source["width"] / 2 - source["x"]) / steps_count
                for x in range(0, steps_count):
                    tmp_x = source["x"] + step * (x)
                    #   move x  是绝对坐标值 不是offset  起点相当于是盒子的中心点 由于不是整除 每次移动可能会与最终的框有一定匹配上的偏移 要么多了 要么少了
                    self.page.mouse.move(
                        tmp_x + random.choice(L1) * source["width"], box_pos_y
                    )
                    time.sleep(random.randint(20, 40) * 0.01)
                self.page.mouse.move(x_offset + source["width"] / 2, box_pos_y)

                print("release dragon icon")
                self.page.mouse.up()
                # self.page.reload()
                # time.sleep(3)

                t = self.page.locator(".captcha_verify_container").is_visible()
                print("check captcha still exist", t)
                # time.sleep(20)
                if t:
                    print("still exist")
                    return {"success": 0}
                else:
                    print("well done")
                    return {"success": 1}
    except Exception as e:
        print("pass very.....")
        return {"success": 1}


def solve_captcha_douyin(self, code_path, count=0):
    # self.page.reload()
    t = self.page.locator('img[class^="captcha_verify_img_slide"]')
    if os.path.exists(code_path):
        os.remove(code_path)
    print("detected captcha", t)
    # time.sleep(0.02)
    if count > 8:  # 约15次错误尝试 会报频繁
        self.browser.close()
        self.open_driver()
        return
    try:
        print(
            "detected capatcha image",
        )

        # time.sleep(0.03)
        img = self.page.locator('img[id="captcha-verify-image"]')
        # ""加不加一样
        print("detected capatcha image", img.get_attribute("src"))
        # slide = self.page.locator("//html/body/div[4]/div/div[2]/img[2]").bounding_box()
        self.page.wait_for_selector(".captcha_verify_img_slide")

        slide = self.page.locator(".captcha_verify_img_slide").bounding_box()
        #   only crop quekou area
        clip = {
            "x": 0,
            "y": slide["y"] - 2,
            "width": self.page.viewport_size["width"],
            "height": slide["height"] + 1,
        }
        if img.get_attribute("src"):
            # time.sleep(1)
            self.page.screenshot(path=code_path, clip=clip)
        print("finished screenshot of slide")
        print("==", slide)

        print("finding offset to move")
        img = cv.imread(code_path)
        card_img = img
        img_blur = cv.GaussianBlur(card_img, (7, 7), 1)
        img = cv.medianBlur(img, 5)
        img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
        ret2, thresh = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        img_canny = cv.Canny(thresh, 50, 190)

        kernel = np.ones((3))
        # erosion = cv.erode(img_canny, kernel, iterations=1)
        img_dilated = cv.dilate(img_canny, kernel, iterations=1)
        # cv.imshow('img_dilated', img_dilated)
        # cv.waitKey(0)
        contours, hierarchy = cv.findContours(
            img_dilated, cv.RETR_LIST, cv.CHAIN_APPROX_NONE
        )
        e2 = []
        offsetlist = []
        # for contour in contours:

        for i, cnt in enumerate(contours):
            # if the contour has no other contours inside of it
            if hierarchy[0][i][2] == -1:
                # if the size of the contour is greater than a threshold
                # if  cv.contourArea(cnt) > 10000:
                x, y, w, h = cv.boundingRect(cnt)
                print(x, y, w, h)
                if cnt.size > 160 and w > 40 and h > 40 and x - slide["x"] > 60:  # TUNE
                    offsetlist.append(x)
                    e2.append(cnt)
        print(offsetlist, "======!")
        final = cv.drawContours(card_img, e2, -1, (0, 255, 0), 3)

        offsetlist = sorted(list(set(offsetlist)))

        if len(offsetlist) == 0:
            return {"success": 0}
        else:
            source = self.page.locator(".secsdk-captcha-drag-icon").bounding_box()

            for x_offset in offsetlist:
                print("offset is", x_offset)
                x_offset = x_offset - 3
                y_offset = 0
                # action = ActionChains(self.driver)
                steps_count = 5
                box_pos_x = source["x"] + source["width"] / 2
                box_pos_y = source["y"] + source["height"] / 2
                self.page.mouse.move(box_pos_x, box_pos_y)
                # self.page.locator(".secsdk-captcha-drag-icon").click()
                print("move mouse to dragon icon and hold")

                # self.page.mouse.click(box_pos_x, box_pos_y)

                self.page.mouse.down()
                print("holding", x_offset, y_offset)
                L1 = [0.3, 0.24, 0.21, 0.14, 0.11]
                step = (x_offset + source["width"] / 2 - source["x"]) / steps_count
                for x in range(0, steps_count):
                    tmp_x = source["x"] + step * (x)
                    #   move x  是绝对坐标值 不是offset  起点相当于是盒子的中心点 由于不是整除 每次移动可能会与最终的框有一定匹配上的偏移 要么多了 要么少了
                    self.page.mouse.move(
                        tmp_x + random.choice(L1) * source["width"], box_pos_y
                    )
                    time.sleep(random.randint(20, 40) * 0.01)
                self.page.mouse.move(x_offset + source["width"] / 2, box_pos_y)

                print("release dragon icon")
                self.page.mouse.up()
                # self.page.reload()
                # time.sleep(3)

                t = self.page.locator(".captcha_verify_container").is_visible()
                print("check captcha still exist", t)
                # time.sleep(20)
                if t:
                    print("still exist")
                    return {"success": 0}
                else:
                    print("well done")
                    return {"success": 1}
    except Exception as e:
        print("pass very.....")
        return {"success": 1}


if __name__ == "__main__":
    # discern(
    #     "../tests/b8f374292c5249d2b441813000802779~tplv-71rtze2081-1.png",
    #     "../tests/7e7bc2d3c90d4df5b1e8c569242b328b~tplv-71rtze2081-1.png",
    #     "./result.png",
    # )
    solve_captcha_tiktok()
