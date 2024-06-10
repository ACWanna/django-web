from selenium import webdriver
import unittest
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
        self.assertIn('To-Do',self.browser.title), "browser title was:" + self.browser.title
        self.fail('Finish the test!')

        # 应用有输入待办事项的文本框

        # 文本框输入"Buy flowers"

        # 回车页面更新
        # 待办事项表格显示了"1: Buy flowers"

        # 页面又显示了文本框，可以输其他待办事项
        # 输入"Send a gift to Lisi"

        # 页面再次更新，现在有两个待办事项

        # 张三想知道这网站是否会记住他的清单
        # 网站生成了一个唯一的url

        # 访问url，发现待办事项列表还在

if __name__=='__main__':
    unittest.main()        