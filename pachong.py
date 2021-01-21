import requests
from bs4 import BeautifulSoup
import re
import json
import random
import pandas as pd

USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,likeGecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
        'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
        'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
        'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
        'UCWEB7.0.2.37/28/999',
        'NOKIA5700/ UCWEB7.0.2.37/28/999',
        'Openwave/ UCWEB7.0.2.37/28/999',
        'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999']

user_agent = random.choice(USER_AGENTS)
headers = {
        'user-agent': user_agent,
        'referer': 'https://www.bilibili.com/',
        'Host': 'www.bilibili.com'

}


Byear = ['1980', '1990', '2000', '2005', '2010','2015', '2016', '2017', '2018', '2019', '2020']  # 番剧索引页开始的年份
Cyear = ['1990', '2000', '2005', '2010', '2015','2016', '2017', '2018', '2019', '2020', '2021']   # 番剧索引页结束的年份
# Byear = ['2021']  # 2021年新番信息爬取
# Cyear = ['2022']


def Fans_rank(fpath):
        df = pd.read_csv(fpath, encoding='utf-8')
        fansrank = df.sort_values(by=['追番人数'],  ascending=False)
        rank = fansrank.head(100)
        df1 = pd.DataFrame(rank)
        df1.to_csv('1980-2020年追番数TOP100.csv')


def Play_rank(fpath):
        df = pd.read_csv(fpath, encoding='utf-8')
        playrank = df.sort_values(by=['播放量'], ascending=False)
        rank = playrank.head(100)
        df1 = pd.DataFrame(rank)
        df1.to_csv('1980-2020年播放量TOP100.csv')


def Getyear_url():
    for i in range(len(Byear)):
        text_url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1' \
                 '&season_status=-1&season_month=-1&year=%5B'+Byear[i]+'%2C'+Cyear[i]+')&style_id=-1&order=3&st=1&sort=0' \
                '&page=1&season_type=1&pagesize=20&type=1'  # b站番剧索引页面api链接# 番剧索引页该年总页数
        total = json.loads(requests.get(text_url).text)['data']['total']  # 获取番剧索引页该年总番剧数
        if (total % 20) == 0:  # 获取该年番剧页面数
            page = int(total / 20)
        else:  # 向上取整
            page = int(total / 20) + 1
        for j in range(page):
            url ='https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1' \
              '&season_status=-1&season_month=-1&year=%5B'+Byear[i]+'%2C'+Cyear[i]+')&style_id=-1&order=3&st=1&sort=0&page=' +str(j+1)+ \
              '&season_type=1&pagesize=20&type=1'  # 爬取索引页面每一部番剧的media号
            items = json.loads(requests.get(url).text)['data']['list']  # 获取json对象并转为字典
            for item in items:
                md = item['media_id'] # 提取media_id
                #ss_link = item['link']  # 番剧播放页面
                GetData(md, movieInfo)   # 进入相应的media号的番剧详细页面爬取数据
        print(Byear[i], "-", Cyear[i], '年的番剧信息爬取完毕！')


def GetData(media_id, movieInfo):  # 抓取番剧各种数据
        media_id_url = 'https://www.bilibili.com/bangumi/media/md' + str(media_id)  # 番剧详细信息界面str(j)
        r = requests.get(media_id_url, headers=headers)  # 解析网页
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('span', class_='media-info-title-t').string  # 番剧名
        title1 = re.sub(',', '，', title).strip()  # 去掉换行符，将英文逗号改为中文
        x = soup.find(name='script', string=re.compile('window.__INITIAL_STATE__')).string  # 找到script标签
        evaluate = re.sub('"evaluate":"', '', x[x.find('"evaluate":"'): x.find('",', x.find('"evaluate":"'))].replace('\\n', '').replace(',', ''))  # 简介
        staff_start = x.find('"staff":')  # 在script标签里找到staff的Tag
        staff_end = x.find(',', staff_start)
        staff = x[staff_start: staff_end]  # 字典提取
        if staff[staff.find('原作：'):staff.find('\\n', staff.find('原作：'))]:  # 正则提取原作的值(字体为简体,':'为英文)
                author = re.sub("原作：", '',
                                staff[staff.find('原作：'):staff.find('\\n', staff.find('原作：'))].replace('\\u002F', '/'))
        elif staff[staff.find('原作:'):staff.find('\\n', staff.find('原作:'))]:
                author = re.sub("原作:", '',
                                staff[staff.find('原作:'):staff.find('\\n', staff.find('原作:'))].replace('\\u002F',
                                                                                                        '/'))  # 正则提取原作的值
        elif staff[staff.find('原著：'):staff.find('\\n', staff.find('原著：'))]:
                author = re.sub("原著：", '',
                                staff[staff.find('原著：'):staff.find('\\n', staff.find('原著：'))].replace('\\u002F', '/'))
        elif staff[staff.find('原著:'):staff.find('\\n', staff.find('原著:'))]:
                author = re.sub("原著:", '',
                                staff[staff.find('原著:'):staff.find('\\n', staff.find('原著:'))].replace('\\u002F', '/'))
        else:
                author = 'NULL'
        if staff[staff.find('导演：'):staff.find('\\n', staff.find('导演：'))]:
                director = re.sub("导演：", '',
                                  staff[staff.find('导演：'):staff.find('\\n', staff.find('导演：'))].replace('\\u002F',
                                                                                                        '/'))  # 导演
        elif staff[staff.find('导演:'):staff.find('\\n', staff.find('导演:'))]:
                director = re.sub("导演:", '',
                                  staff[staff.find('导演:'):staff.find('\\n', staff.find('导演:'))].replace('\\u002F', '/'))
        elif staff[staff.find('導演：'):staff.find('\\n', staff.find('導演：'))]:
                director = re.sub("導演：", '',
                                  staff[staff.find('導演：'):staff.find('\\n', staff.find('導演：'))].replace('\\u002F', '/'))
        elif staff[staff.find('導演:'):staff.find('\\n', staff.find('導演:'))]:
                director = re.sub("導演:", '',
                                  staff[staff.find('導演:'):staff.find('\\n', staff.find('導演:'))].replace('\\u002F', '/'))
        else:
                director = 'NULL'
                # 正则提取动画制作公司的值
        if staff[staff.find('动画制作：'):staff.find('\\n', staff.find('动画制作：'))]:
                company = re.sub("动画制作：", '',
                                 staff[staff.find('动画制作：'):staff.find('\\n', staff.find('动画制作：'))].replace('\\u002F',
                                                                                                           '/'))
        elif staff[staff.find('动画制作:'):staff.find('\\n', staff.find('动画制作:'))]:
                company = re.sub("动画制作:", '',
                                 staff[staff.find('动画制作:'):staff.find('\\n', staff.find('动画制作:'))].replace('\\u002F',
                                                                                                           '/'))
        elif staff[staff.find('動畫製作：'):staff.find('\\n', staff.find('動畫製作：'))]:
                company = re.sub("動畫製作：", '',
                                 staff[staff.find('動畫製作：'):staff.find('\\n', staff.find('動畫製作：'))].replace('\\u002F',
                                                                                                           '/'))
        elif staff[staff.find('動畫製作:'):staff.find('\\n', staff.find('動畫製作:'))]:
                company = re.sub("動畫製作:", '',
                                 staff[staff.find('動畫製作:'):staff.find('\\n', staff.find('動畫製作:'))].replace('\\u002F',
                                                                                                           '/'))
        else:
                company = 'NULL'
        time_start = x.find('"release_date_show":"')
        time_end = x.find('",', time_start)
        time = re.sub('"release_date_show":"', '', x[time_start:time_end])  # 开播时间
        time1 = re.sub('年+\w+', '', time)
        state_start = x.find('"time_length_show":"')
        state_end = x.find('"}', state_start)
        state = re.sub('"time_length_show":"', '', x[state_start:state_end])  # 番剧状态
        if re.search('已完结|连载中', state):
                state = re.sub('[^已完结|连载中]', '', state)  # 只需要已完结或连载中，不需要更新至几集
        elif re.search('分钟', state):
                state = '已上映'  # 电影
        else:
                state = '未开播'  # 2021年新番
        tags = ''  # 标签
        for tag in soup.find_all('span', class_='media-tag'):
                tags = str(tags + tag.string + ' ')
        fans = soup.find('span', class_='media-info-count-item media-info-count-item-fans').find('em').string  # 追番人数
        if re.search(r'万|亿', fans) != None:  # 单位是万或者是亿
                if re.search(r'万', fans) == None:  # 单位是亿
                        if re.search(r'\.', fans) != None:  # 有小数点
                                fans1 = re.sub("[^0-9]", '', fans) + '0000000'  # 有小数点就加7个0
                        else:
                                fans1 = re.sub("[^0-9]", '', fans) + '00000000'  # 没有小数点就加8个
                else:  # 单位是万
                        if re.search(r'\.', fans) != None:  # 有小数点
                                fans1 = re.sub("[^0-9]", '', fans) + '000'  # 有小数点就加3个0
                        else:
                                fans1 = re.sub("[^0-9]", '', fans) + '0000'  # 没有小数点就加4个
        else:
                fans1 = fans
        play = soup.find('span', class_='media-info-count-item media-info-count-item-play').find('em').string  # 播放量
        if re.search(r'万|亿', play) != None:  # 单位是万或者是亿
                if re.search(r'万', play) == None:  # 单位是亿
                        if re.search(r'\.', play) != None:  # 有小数点
                                play1 = re.sub("[^0-9]", '', play) + '0000000'  # 有小数点就加7个0
                        else:
                                play1 = re.sub("[^0-9]", '', play) + '00000000'  # 没有小数点就加8个
                else:  # 单位是万
                        if re.search(r'\.', play) != None:  # 有小数点
                                play1 = re.sub("[^0-9]", '', play) + '000'  # 有小数点就加3个0
                        else:
                                play1 = re.sub("[^0-9]", '', play) + '0000'  # 没有小数点就加4个
        else:
                play1 = play
        label = soup.find('span', class_='media-info-count-item media-info-count-item-review').find('em').string  # 弹幕数量
        if re.search(r'万|亿', label) != None:  # 单位是万或者是亿
                if re.search(r'万', label) == None:  # 单位是亿
                        if re.search(r'\.', label) != None:  # 有小数点
                                label1 = re.sub("[^0-9]", '', label) + '0000000'  # 有小数点就加7个0
                        else:
                                label1 = re.sub("[^0-9]", '', label) + '00000000'  # 没有小数点就加8个
                else:  # 单位是万
                        if re.search(r'\.', label) != None:  # 有小数点
                                label1 = re.sub("[^0-9]", '', label) + '000'  # 有小数点就加3个0
                        else:
                                label1 = re.sub("[^0-9]", '', label) + '0000'  # 没有小数点就加4个
        else:
                label1 = label
        if soup.find('div', class_='media-info-score-content') != None:
                score = soup.find('div', class_='media-info-score-content').string  # 评分
                num = soup.find('div', class_='media-info-review-times').string  # 评分人数
                num1 = re.sub('人评', ' ', num).strip()
        else:  # 没人评分
                score = '0'
                num1 = '0'
        if x[x.find('"shortTotal":'):x.find(',', x.find('"shortTotal":'))]:  # 评论人数
                Total = re.sub('"shortTotal":', '', x[x.find('"shortTotal":'):x.find(',', x.find('"shortTotal":'))])
        else:
                Total = '0'
        movieInfo.append([title1, evaluate, time1, state, tags, author, director, company, fans1, play1, label1, Total, score, num1])  # 将爬取的数据加入append列表


def writeFile(fpath, movieInfo):
        with open(fpath, 'w', encoding='utf-8') as f:
                for info in movieInfo:
                        f.write(','.join(info) + '\n')   # 将append列表内的数据写入csv文件


if __name__ == '__main__':
        movieInfo = [['番剧', '简介', '开播或上映时间', '番剧状态', '标签', '原作', '导演', '动画制作', '追番人数', '播放量', '弹幕数量', '评论人数', '评分', '评分人数']]
        Getyear_url()
        # 存入csv文件
        writeFile('1980-2020年B站番剧信息.csv', movieInfo)  # 1980-2020年番剧信息爬取
        # writeFile('2021年B站番剧信息.csv', movieInfo)  # 2021年新番信息爬取
        Fans_rank('1980-2020年B站番剧信息.csv')  # 追番数前一百的番剧
        Play_rank('1980-2020年B站番剧信息.csv')  # 播放量前一百的番剧
        print("爬取完毕!Master")



