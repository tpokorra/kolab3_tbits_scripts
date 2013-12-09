#!/usr/bin/env python

import unittest
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helperKolabWAP import KolabWAPTestHelpers

# assumes password for cn=Directory Manager is test
# will create 2 new user, and send an email via roundcube from one user to the other
# will login to roundcube and check for the new email
class KolabWAPSendAndReceiveEmail(unittest.TestCase):

    def setUp(self):
        self.kolabWAPhelper = KolabWAPTestHelpers()
        self.driver = self.kolabWAPhelper.init_driver()

    # edit yourself; testing bug https://issues.kolab.org/show_bug.cgi?id=2414
    def helper_user_edits_himself(self):
        driver = self.driver
        elem = driver.find_element_by_xpath("//div[@class=\"settings\"]")
        elem.click()
        self.kolabWAPhelper.wait_loading()
        elem = driver.find_element_by_name("initials")
        elem.send_keys("T")
        elem = driver.find_element_by_xpath("//input[@value=\"Submit\"]")
        elem.click()
        self.kolabWAPhelper.wait_loading()
        elem = driver.find_element_by_xpath("//div[@id=\"message\"]")
        self.assertEquals("User updated successfully.", elem.text, "User was not saved successfully, message: " + elem.text)
        
        self.kolabWAPhelper.log("User has updated his own data successfully")


    def test_send_and_receive_email(self):
        kolabWAPhelper = self.kolabWAPhelper
        kolabWAPhelper.log("Running test: test_send_and_receive_email")
        
        # login Directory Manager, create 2 users
        kolabWAPhelper.login_kolab_wap("/kolab-webadmin", "cn=Directory Manager", "test")
        username1, emailLogin1, password1 = kolabWAPhelper.create_user()
        username2, emailLogin2, password2 = kolabWAPhelper.create_user()
        kolabWAPhelper.logout_kolab_wap()

        # login user1 to roundcube and send email
        kolabWAPhelper.login_roundcube("/roundcubemail", emailLogin1, password1)
        emailSubjectLine = kolabWAPhelper.SendEmail(emailLogin2)
        kolabWAPhelper.logout_roundcube()

        # login user2 to roundcube and check for email
        kolabWAPhelper.login_roundcube("/roundcubemail", emailLogin2, password2)
        kolabWAPhelper.CheckEmailReceived(emailSubjectLine)
        kolabWAPhelper.logout_roundcube()

    def tearDown(self):
        
        # write current page for debugging purposes
        self.kolabWAPhelper.log_current_page()
        
        self.driver.close()

if __name__ == "__main__":
    unittest.main()


