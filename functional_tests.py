from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser=webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):

        # 张三听说有一个在线待办事项的应用
        # 应用首页
        self.browser.get('http://localhost:8000')

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
        time.sleep(2)
        
        table=self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1:Buy flowers', [row.text for row in rows])

        # 页面又显示了文本框，可以输其他待办事项
        # 输入"Send a gift to Lisi"
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新，现在有两个待办事项
        table=self.browser.find_element(By.ID,'id_new_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1:Buy flowers',[row.text for row in rows])
        self.assertIn('2:Give a gift to Lisi',[row.text for row in rows])

        # 张三想知道这网站是否会记住他的清单
        # 网站生成了一个唯一的url
        self.fail('Finish the test!')
        # 访问url，发现待办事项列表还在

if __name__=='__main__':
    unittest.main()        