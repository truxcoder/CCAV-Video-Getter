#央视剧集获取

import re
from getvideo import getVideo
from bs4 import BeautifulSoup
from selenium import webdriver
# browser = webdriver.Chrome()
# browser = webdriver.Firefox()
browser = webdriver. PhantomJS()
#随便给一集的播放页面URL
givenURL = 'http://tv.cctv.com/2019/05/12/VIDEygQeHtiXuAZmucVUBWIr190512.shtml?spm=C55899450127.PFyu6F5ngUYu.0.0'
try:
	browser.get(givenURL)
	#urls:每个视频的播放页面集合
	urls = []
	errors = []
	soup = BeautifulSoup(browser.page_source,'lxml')
	movies = soup.find(id="prolist").find_all(name='li')
	for m in movies:
		a = m.find_all(name='a')[1]
		title = a.attrs['title']
		url = a.attrs['href']
		urls.append(url)	
	index = 1
	if len(urls):
		for i in urls:
			try:
				print('正在处理视频',i)
				browser.get(i)
				result=re.search(r'var guid = \"(.*?)(\";\n.*?var barrageApp)',browser.page_source)
				videoid = result.group(1)
				getVideo(videoid)
				print("已处理第",index,"个视频")
			except Exception as e:
				errors.append({'集数':i,'错误':e,'url':urls[index-1]})
			finally:
				index+=1
	else:
		errors.append('未获得视频列表')
	with open('error.log','w',encoding='utf8') as f:
		if len(errors):
			f.writelines(errors)
		else:
			f.write('No Error!')
finally:
	browser.close()

# 	https://hls.cntv.baishancdnx.cn/asp/hls/1200/0303000a/3/default/b7aef8afa43d4fdd980e3a22218a624c/1200.m3u8?maxbr=2048
# 	http://hls.cntv.myalicdn.com/asp/hls/1200/0303000a/3/default/b7aef8afa43d4fdd980e3a22218a624c/1200.m3u8
# 	http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=b7aef8afa43d4fdd980e3a22218a624c