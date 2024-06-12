from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT=10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser=webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element(By.ID,'id_list_table')
                rows=table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_layout_and_styling(self):
        # 张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # 他看到输入框居中显示
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
            )
        
        # 他新建了一个清单，看到输入框仍居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
            )
    
    def test_can_start_a_list_and_retrieve_it_later(self):

        # 张三听说有一个在线待办事项的应用
        # 应用首页
        self.browser.get(self.live_server_url)

        # 网页"To-Do"
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)

        # 应用有输入待办事项的文本框
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 文本框输入"Buy flowers"
        inputbox.send_keys('Buy flowers')

        # 回车页面更新
        # 待办事项表格显示了"1: Buy flowers"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy flowers')
        

        # 页面又显示了文本框，可以输其他待办事项
        # 输入"Give a gift to Lisi"
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，现在有两个待办事项
        self.wait_for_row_in_list_table('1:Buy flowers')
        self.wait_for_row_in_list_table('2:Give a gift to Lisi')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 张三新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy flowers')

        # 他注意到清单有一个唯一url
        zhangsan_list_url=self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')

        # 现在有一个新用户王五访问网站
        # 我们使用一个新的浏览器会话
        # 确保张三的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser=webdriver.Chrome()

        # 王五访问首页
        # 页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('BGive a gift to Lisi',page_text)

        # 王五输入了一个新待办事项，新建一个清单
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')

        # 王五获得了他的唯一url
        wangwu_list_url=self.browser.current_url
        self.assertRegex(wangwu_list_url,'/lists/.+')
        self.assertNotEqual(wangwu_list_url,zhangsan_list_url)

        #这个页面还是没有张三的清单
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)

        #两人很满意        

        # 张三想知道这网站是否会记住他的清单
        # 网站生成了一个唯一的url
        self.fail('Finish the test!')
        # 访问url，发现待办事项列表还在