# -*- coding:utf-8 -*-
#
# 2016-06-17

import os
import urllib2
import random
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PROXY_LIST = []


with open('./ip_pools.txt') as ip_pools:
    # ip_dict = {}
    for line in ip_pools:
        ip_info = line.strip().strip('{').strip('}')
        # print ip_info
        key = ip_info.split(': ')[0].strip("'")
        value = ip_info.split(': ')[1].strip("'")
        # print key 
        # print value 
        ip_dict = {key:value}
        # ip_dict[key] = "http://" + value
        # print ip
        PROXY_LIST.append(ip_dict)

print PROXY_LIST

USER_AGENT_LIST = [
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                'Opera/9.25 (Windows NT 5.1; U; en)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
            ]

# 使用代理访问网站 - GET方式实现
def spider_url_by_get(proxy=None):

    # url = 'http://home.ustc.edu.cn/~sa614214/'
    url = "http://juku.yicool.cn/fn/ajax/ajax_SentenceInfo.ashx?word=%E8%AE%BD&page=1"
    print 'proxy : ', proxy
 
    try:
        proxyHandler = urllib2.ProxyHandler(proxy)
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies, proxyHandler, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        # print req

        user_agent = random.choice(USER_AGENT_LIST)
        req.add_header('User-Agent', user_agent)
        html = urllib2.urlopen(req, timeout=3).read()
        # print html
        # print 'spider_url_by_get（） +++++++++ ', data
        return True

    except Exception, ex:
        print 'spider_url_by_get（） -------- ', str(ex)
        return False

# 使用代理访问网站 - POST方式实现
def spider_url_by_post():
    pass

def ping_ip(ip=None):
    
#     ping_cmd = 'ping -c 2 -w 5 %s' % ip
     
#     ping_result = os.system(ping_cmd)
#     print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)
#     
#     if ping_result == 0:
#         print 'ping %s ok' % ip
#         return True
#     else:
#         print 'ping %s fail' % ip
         
    ping_cmd = 'ping -c 2 %s' %ip     
    ping_result = os.popen(ping_cmd).read()
    print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)
    
    # with open('./ip_pool_accessible.txt', 'a') as fout:
    if ping_result.find('100% packet loss') < 0:
        print 'ping %s ok' % ip
        # fout.write(ip + '\n')
        return True
    else:
        print 'ping %s fail' % ip


def main():
    
    os.remove('./ip_pools.txt')
    
    for proxy in PROXY_LIST:
        for key in proxy.keys():
            
            print proxy

            value = proxy.get(key, '')
            # print key, value
            ip = value.split("//")[1].split(":")[0].strip()
            # print ip
            with open('./ip_pools.txt', 'a') as fout :
                if ping_ip(ip):
                    if( spider_url_by_get(proxy) ):
                        print ip + ' is accessible'
                        fout.write(str(proxy) + '\n')
                    else : 
                        print ip +' is un-accessible'


if __name__ == '__main__':
    main()


