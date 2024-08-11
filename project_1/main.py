from download import Download
from logger import Logger
import os
import re
import time
import configparser

#read configuration file
config=configparser.ConfigParser(interpolation=None)
config.read('./config.ini')
cache_path=config.get('download','cache_path')
m3u8_url=config.get('download','m3u8_url')
output_path=config.get('download','output_path')
host_name=config.get('download','host_name')
max_thread=config.getint('download','max_thread')
output_path=config.get('download','output_path')
video_format=config.get('download','video_format')
# create a logger object
logger=Logger(config.get('log','log_path'))

#download m3u8 file
logger.logger.info("start the process of downloading m3u8 file")
m3u8_list=[m3u8_url]
download_m3u8=Download(m3u8_list,cache_path,file_name="m3u8",max_workers=max_thread)  
download_m3u8.start_download()
logger.logger.info("the process of downloading m3u8 file has been completed")

# #download ts file according to m3u8 file
logger.logger.info("start the process of downloading ts file")
url_list=[]
result_dir_list=os.listdir(cache_path)
match = re.search(r'/([^/]+\.'+"m3u8"+r').*?', m3u8_url)
if match:
    m3u8_file_name=match.group(1)
while True:
    n=0
    with open(os.path.join(cache_path,m3u8_file_name), 'r') as f:
        
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            else:
                if line.startswith('http'):
                    match = re.search(r'/([^/]+\.'+"ts"+r').*?', line)
                    if match:
                        name=match.group(1)
                        if name not in result_dir_list:
                            url_list.append(line)
                            n+=1
                    else:
                        logger.logger.error("match failed")
                else:
                    url_list.append(host_name+line)
                    n+=1
    Download(url_list,cache_path,max_workers=max_thread).start_download()
    if n==0:
        break  
logger.logger.info("the process of downloading ts file has been completed")

#merge ts files
logger.logger.info("start the process of merging ts files")
n=0
with open(os.path.join(cache_path,m3u8_file_name), 'r') as m3u8_file:
    for line in m3u8_file:
        line = line.strip()
        if line.startswith("#"):
            continue
        match = re.search(r"/([^/]+\." + "ts" + r").*?", line)
        if match:
            name = match.group(1)
            os.rename(cache_path+str(n)+".ts",os.path.join(cache_path,f"{str(n).zfill(6)}.ts"))
            n+=1
            logger.logger.info(f"{name} has been renamed)")
        else:
            logger.logger.error("match failed")
os.system('copy /b ' + os.path.join(cache_path,"*.ts") +" result.ts")
logger.logger.info("the ts files have been merged into result.ts")
if video_format =="mp4":
    os.system('ffmpeg -i result.ts -c copy result.mp4')
    logger.logger.info("the result.ts has been converted into result.mp4")
logger.logger.info("the process of merging ts files has been completed")