# -*- coding:utf-8 -*-

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Actions action = new Actions(driver);
# action .sendKeys(Keys.ENTER).perform();

option = webdriver.ChromeOptions()
option.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=option)
driver.get("http://47.110.127.110:8090/user/node/data")
username ="njfd"
pwd ="888888"
ele_username = driver.find_element_by_id("username")
ele_username.clear()
ele_username.send_keys(username)
ele_pwd =driver.find_element_by_id("password")
ele_pwd.clear()
ele_pwd.send_keys(pwd)
ele_yanz = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/form/div[3]/button/span')
yanz = ele_yanz.text
ele_yz = driver.find_element_by_id("captcha")
ele_yz.clear()
ele_yz.send_keys(yanz)
ele_login = driver.find_element_by_xpath("//button[@type='submit']")
ele_login.click()
# windowhadls = driver.window_handles
# count = len(windowhadls)
# driver.switch_to.window(windowhadls[count-1])
time.sleep(3)
page_source = driver.page_source
print page_source
pro_manage = driver.find_element_by_xpath("//li[text()='项目管理']")
pro_manage.click()
time.sleep(3)
pro_check = driver.find_element_by_xpath("//a[text()='查看']")
pro_check.click()
pro_device_manage = driver.find_element_by_xpath("//span[text()='设备管理']")
pro_device_manage.click()
time.sleep(3)
pro_device1 = driver.find_element_by_xpath("//a[text()='004A7700660018DA']")
pro_device1.click()
time.sleep(3)

while True:
    refresh = driver.find_element_by_xpath("//span[text()='下行统计']")
    refresh.click()
    pro_data_check = driver.find_element_by_xpath("//span[text()='查看数据']")
    pro_data_check.click()
    try:
        all_check = driver.find_element_by_xpath("//div[@class='ant-table-selection']")
        time.sleep(3)
        all_check.click()
        #保留前2个
        chebox1= driver.find_element_by_xpath("//tbody[@class='ant-table-tbody']/tr[1]/td[1]/span")
        chebox1.click()
        time.sleep(3)
        chebox2= driver.find_element_by_xpath("//tbody[@class='ant-table-tbody']/tr[2]/td[1]/span")
        chebox2.click()
        #删除
        delete =driver.find_element_by_xpath("//div[@class='actions']/a[text()='删除']")
        delete.click()
        time.sleep(3)
        title = driver.find_element_by_xpath("//span[text()='确定要删除吗？']")
        driver.switch_to.window(title)


    except:
        pass
    time.sleep(60)


