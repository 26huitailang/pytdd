from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_url, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## 为了设定cookie，我们要先访问网站
        ## 而404页面是加载最快的
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/")
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = "edith@example.com"

        # 伊迪丝是已登陆用户
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Reticualte splines')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.get_item_input_box().send_keys('Immanentize eschaton')
        self.get_item_input_box().send_keys(Keys.ENTER)
        first_list_url = self.browser.current_url

        # 她第一次看到My Lists链接
        self.browser.find_element_by_link_text('My Lists').click()

        # 她看到这个页面中有她创建的清单
        # 而且清单根据第一个待办事项命名
        self.browser.find_element_by_link_text('Reticualte splines').click()
        self.assertEqual(self.browser.current_url, first_list_url)

        # 她决定再建一个清单试试
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Click cows')
        self.get_item_input_box().send_keys(Keys.ENTER)
        second_list_url = self.browser.current_url

        # 在My Lists页面，这个新建的清单也显示出来了
        self.browser.find_element_by_link_text('My Lists').click()
        self.browser.find_element_by_link_text('Click cows').clikc()
        self.assertEqual(self.browser.current_url, second_list_url)

        # 她退出后，My Lists链接不见了
        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
            self.browser.find_element_by_link_text('My Lists'),
            []
        )