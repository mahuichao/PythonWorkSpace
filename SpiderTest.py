# encoding=utf-8
import urllib2
import re
import thread
import time
import os.path


class mySpider:
    def __init__(self):
        self.page = 1
        self.enable = True
        self.finalPage = 20
        self.file_all_location = "/Users/mahuichao/Downloads/ip_all.txt"

    # 开始任务
    def load_page(self):
        while self.enable:
            page = self.page
            myUrl = "http://www.xicidaili.com/nn/" + str(page)
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            req = urllib2.Request(myUrl, headers=headers)
            myResponse = urllib2.urlopen(req)
            myPage = myResponse.read()
            unicodePage = myPage.decode('utf-8')
            self.saveIps(unicodePage)
            self.page += 1
            # 如果页数小于我们的所需
            if self.page <= self.finalPage:
                print "爬取中。。。请稍等"
                time.sleep(2)
            else:
                self.enable = False

    # 判断文件是否已经存在
    def judgeIfExis(self):
        result = os.path.isfile(self.file_all_location)
        return result

    # 保存到本地文件
    def saveFile(self, page, content):
        file = open("/Users/mahuichao/Downloads/" + str(page) + ".html", 'w')
        file.write(content)
        file.close()

    # 保存ip到相应的文件中
    def saveIps(self, content):
        result = self.judgeIfExis()
        # 文件存在
        if result == True:
            file = open(self.file_all_location, "a")
            items = self.re(content)
            for item in items:
                file.write(item + "\n")
            file.close()
        else:
            file = open(self.file_all_location, "w")
            items = self.re(content)
            for item in items:
                file.write(item + "\n")
            file.close()

    # 拿取IP地址
    def re(self, content):
        myItems = re.findall("<td>(\d+\.\d+\.\d+\.\d+)</td>", content)
        items = []
        for item in myItems:
            items.append(item)
        return items

    # 程序入口
    def start(self):
        print "spide begin"
        thread.start_new_thread(self.load_page, ())
        while self.enable == True:
            time.sleep(2)
        print "spide over"


spide = mySpider()
spide.start()
