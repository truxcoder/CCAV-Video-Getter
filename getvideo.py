import json,requests,re,os
# try:
# 	browser.get('https://tv.cctv.com/2017/07/10/VIDEZ9o0BScBhcvtfwz58c67170710.shtml?spm=C55899450127.PGm7WxgwlTKs.0.0')
# finally:
# 	browser.close()
def getVideo(videoid):
	print('开始获取ID为：',videoid,'的数据')
	#获取json文件链接
	json_url="http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid="+videoid
	json_str = requests.get(json_url)
	#json_str.content是bytes对象，需要用decode方法转成str
	json_dict = json.loads(json_str.content.decode('UTF-8'))
	title = json_dict['title'].replace(" ","")
	hls_url = json_dict['hls_url']
	m3u8 = hls_url.replace('main','1200')[:-11]
	# print('已获取的m3u8地址为：',m3u8)
	# print('开始请求ts数据')
	# 获取m3u8文件
	r = requests.get(m3u8)
	pattern = re.compile(r'\\n(\d*?\.ts)\\n', re.I)
	result = pattern.findall(str(r.content))
	for i in result:
		#获取每个ts文件
		res = requests.get(m3u8[:-9]+i)
		filename = '0'+i if len(i)<5 else i
		with open(filename,"wb") as f:
			# print('正在下载：',i)
			f.write(res.content)
	cmd = "copy/b *.ts "+title+".mp4"
	os.system(cmd)
	os.system("del *.ts")


