# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re


# 获取html网页数据的程序
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        # 当返回Response这样的一个返回了所有的网页内容，也提供了一个方法
        # 叫raise_for_status()， 这个方法是专门与异常打交道的方法
        # 这个方法有这样一个有趣的功能，它能够判断返回的Response类型状态是不是200.
        # 如果是200，它将表示返回的内容是正确的，如果不是200，它将会产生一个HttpError的异常
        r.encoding = r.apparent_encoding
        # 使用apparent_encoding可以获得真实编码
        return r.text
    except:
        return ""

# html代码解析程序
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            # attrs[]我觉得是查找a元素中有href属性的元素
            lst.append(re.findall(r'[s][hz]\d{6}', href)[0])
        except:
            continue

def getStockInfo(lst, stockURL, fpath):
    count = 0  # 计数
    for stock in lst:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

            infoDict = {}
            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print("\r总当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'E:/新建文件夹/股票盘/BaiduStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)


main()

# try...except来对程序进行异常处理
