import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import os
from logger import Logger
import configparser

class Download():
    def __init__(self,url_list,output_dir,max_workers=20,file_name="ts") -> None:
        self.url_list=url_list
        self.max_workers=max_workers
        self.file_name=file_name
        self.output_dir=output_dir
        #create ConfigParser object
        self.config = configparser.ConfigParser(interpolation=None)
        #read configuration file
        self.config.read('./config.ini')
        #create a logger object
        self.logger=Logger(self.config.get('log','log_path')) 
    def __start_one(self,url):
        response=requests.get(url)
        match = re.search(r'/([^/]+\.'+self.file_name+r').*?', url)
        if match:
            name=match.group(1)
        else:
            self.logger.logger.error("match failed")
        fp=open(os.path.join(self.output_dir,name), 'wb')
        fp.write(response.content)
        if response.status_code==200:
            self.logger.logger.info(f"{name} has been downloaded")
        elif response.status_code==404:
            self.logger.logger.error(f"{url} does not exist")
            exit()
        else:
            self.logger.logger.error(f"the status code of {url} is {response.status_code}")
            exit()
        return response.status_code
    
    def start_download(self):
        obj_list = []
        # if the output directory does not exist, create it
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"the folder '{self.output_dir}' has been created.")
        else:
            print(f"the folder '{self.output_dir}' already exists.")
        with ThreadPoolExecutor(max_workers=self.max_workers) as t:
            for url in self.url_list:
                obj = t.submit(self.__start_one, url)
                print(f"the task of {url} has been submitted")
            for future in as_completed(obj_list):
                data = future.result()
                print(f"the task of {data} has been completed")
            

          
if __name__=="__main__":
    ts_dir="D:\\OneDrive - 中山大学\\桌面\\工作区\\crawler\\project_1\\video"
    m3u8_dir="D:\\OneDrive - 中山大学\\桌面\\工作区\\crawler\\project_1"
    # url_list=[
    #     "https://n45lxpvts.com/videos/df2252ba94b149abaeca0c0b7c86f5f8/si/-1300eKCg0-4K-DmcaMS7BDXkQvrAbgqjJcXhn3EXte0Af0SxTs.ts?mm=NDRjZDM5M2Q2ODkwNmM2YTE3NzNmNWM5NWVmNWMwOTA&t=1723164300410&d=n45lxpvts.com&e=1723185900410&ip=54.199.156.37&gap=c458e046a8f2f52ab96aca75f92067c5&ic=JP&slot=e141a58d5d2a9b777f1bdd03cc11655c",
    #     "https://n45lxpvts.com/videos/df2252ba94b149abaeca0c0b7c86f5f8/si/kemP_UX6ElLOTkLTX5l1lukj7WCEGs6WPscJp0n_uieAd8ExpNQ.ts?mm=NDRjZDM5M2Q2ODkwNmM2YTE3NzNmNWM5NWVmNWMwOTA&t=1723164300410&d=n45lxpvts.com&e=1723185900410&ip=54.199.156.37&gap=c4e0e80c73367f696ae4f57b72733e12&ic=JP&slot=6d6b1f53043a469df034605554c966aa"
    # ]
    # download=Download(url_list)
    # download.start_download()
    m3u8_list=['https://api.heimuer.app/play/df2252ba94b149abaeca0c0b7c86f5f8.m3u8']
    download_m3u8=Download(m3u8_list,m3u8_dir,file_name="m3u8")  
    download_m3u8.start_download()
    