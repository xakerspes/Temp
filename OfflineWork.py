import requests,shutil
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sys,os,glob,re
from datetime import  datetime,timedelta

#obyazatelnie peremennie (vvedite nije)
width = 13
base_link =  "http://amk030.imces.ru/meteodata/AMK_030_BIN/"
start_date = 2007,8,2,0,0 # nado menyat month to day
end_date   = 2007,8,9,0,0 # nado menyat month to day

freq='1min' #выбирайте частота повторения

class obrabotka_danniy():
    
    def __init__(self, base_link=base_link, 
                  count=10):
        self.base_link  = base_link
        self.url_count  = count
        self.dir_name   = None
        self.type_files = None
        self.urls       = None
        self.file_names = None
        self.start      = start_date
        self.end        = end_date
        self.UrlsFile   = "URLS.txt"
        self.start_str, self.end_str =['{:02d}'.format(x) for x in self.start] , ['{:02d}'.format(x) for x in self.end]
      
        self.base_link =  "http://amk030.imces.ru/meteodata/AMK_030_BIN/"
        
        self.run_code2()
        
    def run_code2(self):
        
        self.urls = self.getLinksWithoutWebsite()
#         self.urls = self.getfileLinks()

        self.create_dir_for_downloading_files()
        self.download_files()
        self.get_file_names_in_dir()
        
        
    def get_all_links_file(self):
        page = requests.get(self.base_link)
        soup = BeautifulSoup(page.content)
        result = []
        for link in soup.find_all('a', href=True):
            if (link['href'][-4]=='.' and link['href'][-1]=='B'):
                result.append(self.base_link + link['href'])
        if len(result)>1:
            self.type_files = result[0][-3:]
        self.urls = result[:self.url_count]
     
    def create_dir_for_downloading_files(self):
        path = os.path.abspath('') + '\\' + str(self.base_link.split('/')[-2])
        if not os.path.isdir(path):
            os.mkdir(path)
            self.dir_name = path
        else:
            shutil.rmtree(path)
            os.mkdir(path)
            self.dir_name = path
            
     
    def download_files(self):
        for i,j in enumerate(self.urls):
            handle      =   requests.get(self.urls[i])
            full_name   =   os.path.join(self.dir_name,os.path.basename(self.urls[i]))
            with open(full_name, "wb") as f_handler:
                chunk = handle.content
                f_handler.write(chunk)
                    
     
    def get_file_names_in_dir(self):
        file_names  =   []
        file_name   =   os.path.join(os.path.abspath(''),self.dir_name,"*")
        for i in glob.glob(file_name):
            file_names.append(i)
        self.file_names = file_names
        return file_names
    
    
    def function_obrabotka(self):
        width = 13
        data_frame_list = []
        file_names = self.get_file_names_in_dir()
        for i,j in enumerate(file_names):
            with open(j, "rb") as file:
                content = file.read()
                data_dopolnitelniy = np.frombuffer(content[:17], dtype=np.dtype('i1'))
                data_dopolnitelniy = np.frombuffer(data_dopolnitelniy[:16], dtype=np.dtype('i2'))
                date_temp = data_dopolnitelniy[:-1]
                date_time = datetime(*date_temp).strftime("%d.%m.%Y %H:%M:%S")
                numpy_data_polojitelnie = np.frombuffer(content, dtype=np.dtype('B'))[17:-14]
                numpy_data_polojitelnie = numpy_data_polojitelnie.reshape(int(len(numpy_data_polojitelnie) / width), width)
                numpy_data_polojitelnie = np.delete(numpy_data_polojitelnie,12,1)
                numpy_data_polojitelnie = np.frombuffer(numpy_data_polojitelnie, dtype=np.dtype('i2'))
                numpy_data_polojitelnie = numpy_data_polojitelnie.reshape(int(len(numpy_data_polojitelnie)/6),6)
                row = numpy_data_polojitelnie.shape[0]
                column = numpy_data_polojitelnie.shape[1] + 1
                zero = np.zeros((row,1))
                numpy_data_polojitelnie = np.append(numpy_data_polojitelnie,zero,axis=1) 
                for i in range(len(numpy_data_polojitelnie)):
                    numpy_data_polojitelnie[i,0] = numpy_data_polojitelnie[i,0] / 100
                    numpy_data_polojitelnie[i,1] = numpy_data_polojitelnie[i,1] / 100
                    numpy_data_polojitelnie[i,2] = numpy_data_polojitelnie[i,2] / 100
                    numpy_data_polojitelnie[i,3] = numpy_data_polojitelnie[i,3] / 100
                    numpy_data_polojitelnie[i,4] = numpy_data_polojitelnie[i,4] / 10
                    numpy_data_polojitelnie[i,5] = numpy_data_polojitelnie[i,5] / 100
                datelist = pd.date_range(date_time, periods=len(numpy_data_polojitelnie), freq='12.5ms').to_pydatetime()
                data_frame = pd.DataFrame({'Time': datelist, 'Температура': numpy_data_polojitelnie[:,0], 'Южный компонент': numpy_data_polojitelnie[:,1],
                              'Восточный компонент': numpy_data_polojitelnie[:,2], 'Вертикальный компонент': numpy_data_polojitelnie[:,3],
                              'Атмосферное давление': numpy_data_polojitelnie[:,4], 'Влажность воздуха': numpy_data_polojitelnie[:,5],
                              'Признак ошибки': numpy_data_polojitelnie[:,6]})
                data_frame_list.append(data_frame)
        data_frame = pd.concat(data_frame_list, ignore_index=False)
        df = data_frame.groupby(pd.Grouper(key='Time',freq=freq,sort=True)).mean().round(2)
        df.dropna(subset=['Атмосферное давление'],inplace=True)
        return  df
        
    def getLinks(self,url,directory=None):
        result = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content)
        if not directory:
            for link in soup.find_all('a', href=True):
                if (link['href'][-4]=='.' and link['href'][-1]=='B'):
                    result.append(link['href'])
        else:
            for link in soup.find_all('a', href=True):
                if (link['href'][-1] == '/'):
                    result.append(link['href'])
        return result

    def getLinksWithoutWebsite(self):
        with open(self.UrlsFile) as file:
            f=file.read()
        links =np.genfromtxt(self.UrlsFile,dtype='str')

        a=np.array(re.findall(r'\/\d+',f)).reshape(-1,3)
        b=np.char.add(a[:,0], a[:,1])
        c=np.char.add(b,a[:,2])
        d=np.char.replace(c, '/', '')
        start = ''.join(['{:02d}'.format(x) for x in self.start])
        end = ''.join(['{:02d}'.format(x) for x in  self.end])
        start = int(start[:6] +  start[4:6] + start[6:]) 
        end   = int(  end[:6] +    end[4:6] +   end[6:])
        arrayLinks = []
        for i,j in enumerate(d):
            if  start <= int(d[i]) <= end:
                arrayLinks.append(links[i])
        if not arrayLinks: print('INCORRECT DATE')
        else: return arrayLinks
        
    def getLinksinDir(self):
        year_url = os.path.join(base_link,self.start_str[0])   #'http://amk030.imces.ru/meteodata/AMK_030_BIN / +  '2008'
        month_urls       = [x for x in self.getLinks(year_url,1) if x[-5:]==self.start_str[0]+'/' and x[0] != '/']
        month_year_urls  = [x.split('_') for x in month_urls] #[['01', '2008/'], ['02', '2008/'],
        index = None
        for i,j in enumerate(month_year_urls):
            if self.start_str[0]==month_year_urls[0][-1][:-1] and self.start_str[1]==month_year_urls[i][0]:
                if len(month_year_urls[i])==3:
                    days_period= [int(x) for x in re.findall(r'\d+', month_urls[i])]
                    if int(self.start_str[1])==(days_period[0]) and  days_period[1] <= int(self.start_str[2]) <= days_period[2]:
                        index = i
                        break
                else: index = i
        if index is not None: 
            self.base_url = year_url +'/'+ month_urls[index]
            return self.getLinks(self.base_url)
        else: print('no files') 
            
    def getfileLinks(self):
       
        url_files = []
        urls =  self.getLinksinDir()
        find_from = ''.join(self.start_str[1:])
        find_to   = ''.join(  self.end_str[1:])

        if urls:
            for i in urls:
                if int(find_from) <= int(i[:len(find_from)]) < int(find_to):
                    url_files.append(self.base_url + i)
            if not url_files: print('no files') 
#             else: return url_files
            else: return [url_files[i] for i,j in enumerate(url_files) if not i%10]
    
if __name__ == '__main__':
    obrabotka_danniy=obrabotka_danniy()
    df = obrabotka_danniy.function_obrabotka()
    df=df.reset_index()

    print(obrabotka_danniy.urls)
    df.to_csv('dataframe.txt')
