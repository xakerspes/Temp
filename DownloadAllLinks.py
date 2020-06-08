#year_links = ['2007/', '2008/', '2009/', '2010/', '2011/', '2012/', '2013/', '2014/', '2015/', '2016/', '2017/', '2018/', '2019/', '2020/']
import logging,re,requests
logging.basicConfig(format = '%(message)s',filename = 'URLS.txt',level=logging.INFO,filemode='w')
base = "http://amk030.imces.ru/meteodata/AMK_030_BIN/"
year_links  =  re.findall('"(\d+.*\d+\/)"', requests.get("http://amk030.imces.ru/meteodata/AMK_030_BIN/").text)
month_links =[]
file_links  =[]
for i in year_links:
    url_1 = f"http://amk030.imces.ru/meteodata/AMK_030_BIN/{i}"
    folders = re.findall('"(\d+.*\d+\/)"', requests.get(url_1).text)
    for j in folders:
        month_links.append(j)
        url_2 = f"{url_1}{j}"
        for k in month_links:
            files = re.findall('"(\d+.*B)"', requests.get(url_2).text)
            file_links.append(files)
            for l in files:
                logging.info(str(base+i+k+l))
#             break
#         break
#     break
