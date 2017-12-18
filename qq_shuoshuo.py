# coding=utf-8
from selenium import webdriver
import time
from lxml import etree
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

class qqss_spider:
    def __init__(self,uname,pwd):
        self.uname = uname
        self.pwd = pwd
        self.driver = webdriver.Firefox()

    def login(self):
        login_url = 'https://qzone.qq.com/'
        self.driver.get(login_url)
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[@id='login_frame']"))

        self.driver.find_elements_by_xpath("//a[@id='switcher_plogin']")[0].click()
        self.driver.find_element_by_id("u").send_keys(self.uname)    
        self.driver.find_element_by_id("p").send_keys(self.pwd)
        self.driver.find_element_by_id("login_button").click()
        self.driver.switch_to.default_content()
        time.sleep(3)

    def crawqq(self):
        # 切换到说说
        self.driver.find_elements_by_xpath("//div[@id='menuContainer']/div/ul/li[5]/a")[0].click()
        time.sleep(3)

        allpage = self.getAllpage()
        for page in xrange(1,allpage+1):
            print 'page',page,allpage
            # 下滑
            for i in xrange(1,30):
                # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)"）
                js = "var q=document.documentElement.scrollTop=%s"%(500*i)
                self.driver.execute_script(js)
                time.sleep(0.5)
            # 切换到内部
            self.driver.switch_to.frame(self.driver.find_element_by_xpath("//div[@id='app_container']/iframe"))
            time.sleep(1)

            # 保存结果
            with open("%s.html"%page,'w') as fw:
                fw.write(self.driver.page_source)

            self.getData(self.driver.page_source)

            # 翻页
            self.driver.find_elements_by_xpath("//div[@id='pager']/div/p/a[last()]")[0].click()
            time.sleep(3)
            
            self.driver.switch_to.default_content()
        self.close()


    def getAllpage(self):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//div[@id='app_container']/iframe"))
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        pagenum = soup.select('div[id="pager"] div p a span')[-2].string
        self.driver.switch_to_default_content()
        return int(pagenum)

    def getData(self,html):
        soup = BeautifulSoup(html, "html.parser") 

        for con in soup.select('ol[id="msgList"] > li'):
            res = {}
            print '======'
            # 获取说说
            said = con.select('pre[class="content"]')[0].getText()
            if len(said) == 0:
                try:
                    said = u'转载:' + con.select('div[class="md rt_content"]')[0].getText()
                except Exception as e:
                    said = ''
            print said
            res['said'] = said

            # zan 
            # res['zan'] = []
            # zans = con.select('div[class="box_extra bor3 "] a[class="c_tx"]')
            # for zan in  zans:
            #     zan = zan.string
            #     if zan and u'人' not in zan  and zan != u'置顶':
            #         print zan
            #         res['zan'].append(zan)

            
            # comments
            res['comments'] = []
            comments = con.select('li[class="comments_item bor3"]')
            for comment in comments:
                con = comment.select('div[class="comments_content"]')[0].getText().split('回复')
                # print con
                who = con[0]
                whocon = con[1].strip().strip('undefined')
                print who+'replay'+whocon
                res['comments'].append(who+whocon)
            self.tofile(res)

    def tofile(self,data):
        with open('results.txt','a') as fw:
            fw.write(data['said']+'\n')
            fw.write('comments:'+'\n'.join(data['comments'])+'\n')
            fw.write('=============\n')

    def close(self):
        self.driver.quit()


qqcraw = qqss_spider('aaa','aaa')
qqcraw.login()
qqcraw.crawqq()
print 'ok'