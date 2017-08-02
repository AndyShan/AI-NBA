# coding=utf-8
from bs4 import BeautifulSoup
import urllib2
import tools as tl
import time
import pandas as pd
TABLE1 = 'http://nba.sports.sina.com.cn/match_result.php?'
TABLE_PLAYER = 'http://nba.sports.sina.com.cn/'


def get_table1(year, months):
    url = TABLE1 + 'day=0&years=' + year + '&months=' + months + '&teams='
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    tr = soup.find_all('table')[1].find_all('tr')
    date = ''
    tabel1_data = []
    for i in tr:
        if (i['bgcolor'] == '#FFD200'): # 字段名栏
            td = i.find_all('td')
            # print td[0].string # 日期
            date = year + '年' + td[0].string
        else:
            cur_data= [date]
            td = i.find_all('td')
            index = 0
            for j in td:
                a = j.find_all('a')
                if index < 7:
                    if len(a) == 0:
                        # print j.string
                        cur_data.append(j.string)
                    else:
                        # print a[0].string.strip()
                        cur_data.append(a[0].string.strip())
                elif index < 9:
                    # print a[0]['href']
                    cur_data.append(a[0]['href'])
                index += 1
            tabel1_data.append(cur_data)
    return tabel1_data


def get_tabel_player(u, tid):
    url = TABLE_PLAYER + u
    # print url
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    # print soup.prettify()
    tr = soup.find_all('tr')
    data = []
    for i in tr:
        if i.has_attr('align') and i.string != None and '技术统计' in i.string:
            # print str(i.string).strip()
            team_name = str(i.string).strip().replace('技术统计', '')
        if i.has_attr('bgcolor') and i['bgcolor'] == '#FFEFB6':
            td = i.find_all('td')
            index = 0
            if len(td) == 14:
                cur_data = [str(tid), team_name]
                for j in td:
                    # print str(j.string).strip()
                    # if index in [0, 2, 3, 4]:
                    cur_data.append(str(j.string).strip())
                    # else:
                    #     cur_data.append(int(str(j.string).strip()))
                    index += 1
                cur_data.append('正常')
                # print cur_data
                data.append(cur_data)
            elif len(td) == 2:
                cur_data = [str(tid), team_name]
                cur_data.append(str(td[0].string).strip())
                for x in range(13):
                    if x in [1,2,3]:
                        cur_data.append('')
                    else:
                        cur_data.append('0')
                cur_data.append(str(td[1].string).strip())
                # print cur_data
                data.append(cur_data)
    return data


def sina_table1(begin=2014, end=2018):
    tl.header2csv('table1', ['tid', 'date', 'time', 'type', 'away', 'score', 'home',
                             'away_star', 'home_star', 'news', 'player_score'])
    for i in range(begin, end):
        for j in range(1, 13):
            try:
                print 'begin'
                year = str(i)
                if j < 10:
                    month = '0' + str(j)
                else:
                    month = str(j)
                table1_data = get_table1(year, month)
                tl.data2csv('table1', table1_data, True)
                print year + month + 'complete'
            except:
                print 'error occur, sleep 5 min'
                time.sleep(5 * 60)


def sina_table_player():
    tl.header2csv('table_player', ['tid', 'tn', 'n', 't', 's', '3ps'
        , 'fts', 'off', 'def', 'rebs', 'asts', 'stls', 'blks', 'tos', 'fouls', 'pts', 'status'])
    df = pd.read_csv('table1.csv')
    player_score_list = list(df.player_score)
    for u in range(len(player_score_list)):
        try:
            print u
            data = get_tabel_player(player_score_list[u], u + 1)
            tl.data2csv('table_player', data)
        except BaseException, e:
            print e.message
            time.sleep(3 * 60)




# sina_table1(begin=2009, end=2018)
sina_table_player()
