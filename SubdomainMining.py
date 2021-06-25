import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys


def bing_search(site, pages):
    Subdomain = []
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        'Accept': "*/*",
        'Referer': "https://cn.bing.com/",
        'Cookie': "_EDGE_V=1; MUID=2E4F69B1B8D76FA31AD46647B9F96E9F; MUIDB=2E4F69B1B8D76FA31AD46647B9F96E9F; SRCHD=AF=MOZLBR; SRCHUID=V=2&GUID=161412FA8942413FB6286026B15ABB70&dmnchg=1; SRCHUSR=DOB=20210310&T=1618712884000; SRCHHPGUSR=SRCHLANGV2=zh-Hans&HV=1618712887&WTS=63754309684&BRW=XW&BRH=S&CW=1536&CH=360&DPR=1.25&UTC=480&DM=1&EXLTT=31&PLTL=1359&PLTA=875&PLTN=278; ABDEF=V=13&ABDV=11&MRNB=1616813927802&MRB=0; _tarLang=default=en; _TTSS_OUT=hist=WyJlbiJd; imgv=lodlg=1&gts=20210325; SNRHOP=I=&TS=; _EDGE_S=SID=28B7EBD33B8C6C2C0B08FBCE3AA26D17; _SS=SID=28B7EBD33B8C6C2C0B08FBCE3AA26D17&bIm=039; ipv6=hit=1618716486813&t=4"
    }
    for i in range(1, int(pages) + 1):
        url = "https://cn.bing.com/search?q=site%3a" + site + "&go=Search&qs=ds&first=" + str(
            (int(i) - 1) * 10) + "&FORM=PERE"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        job_bt = soup.findAll('h2')
        for i in job_bt:
            link = i.a.get('href')
            domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            if domain in Subdomain:
                pass
            else:
                Subdomain.append(domain)
                print(domain)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        site = sys.argv[1]
        page = sys.argv[2]
    else:
        print("用法: %s baidu.com 10" % sys.argv[0])
        sys.exit(-1)
    Subdomain = bing_search(site,page)
