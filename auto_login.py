#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:secoba
'''
Use selenium module to auto login website
'''
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver

driver = webdriver.Firefox()
driver.maximize_window()


# ------------------------------------------
def login_github(uname, pwd):
    '''
    login github auto
    '''
    
    driver.get('https://github.com/login')
    
    username = driver.find_element_by_id('login_field')
    password = driver.find_element_by_id('password')
    
    username.send_keys(uname)
    password.send_keys(pwd)
    
    submit_btn = driver.find_element_by_xpath("//*[@type='submit']")
    submit_btn.submit()
    
    pass


if __name__ == '__main__':
    login_github('username', 'password')
