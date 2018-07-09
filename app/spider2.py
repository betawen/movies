# -*- coding: utf-8 -*-

from lxml import etree

import requests

from chardet import detect

import string

import operator


#分类电影爬虫（可以只有一次爬取存储至数据库中）
class ListSpider():

	#所有免费电影信息
	all_movie = []

	all_movie_name = []

	all_movie_id = []

	all_movie_message = []

	all_movie_pic = []


	#获取网站内容--------这里暂时默认首先爬取优酷免费电影首页
	url = 'http://list.youku.com/category/show/c_96_s_1_d_1_pt_1.html?spm=a2h1n.8251845.filterPanel.5!6~1~3!2~A'



	def  __init__(self):
		
		#测试
		'''
		all_info = self.get_all_movie_infos(2)
		for info in all_info:
			print(info)
		'''



	#所有电影的信息
	#n是要爬取的电影页数-----每页25部电影
	def get_all_movie_infos(self,n):

		#所有电影的信息------存放为二维数组的形式------与数据库对接
		all_movie_info = []

		#获取所有页的网址
		all_page_links = self.get_all_page_links(self.url)
		
		for i in range(n):

			#获取每页所有电影信息
			page_tree = self.analysis_html(all_page_links[i])
			movie_infos = self.get_page_movies_info(page_tree)

			#放入二维数组all_movie_info
			for movie_info in movie_infos:
				all_movie_info.append(movie_info)

		return all_movie_info
	

	#获取一页的所有电影信息
	def get_page_movies_info(self,tree):

		movie_infos = []
		
		#当前页所有网址链接（字符串）
		movie_links = self.get_movie_link(tree)
		
		for movie_link in movie_links:
			#获得电影所有信息
			movie_info = self.get_movie_info(movie_link)
			
			if movie_info != None:
				movie_infos.append(movie_info)

		return movie_infos



	#获得每部电影的所有信息,输入为详情页网址
	def get_movie_info(self,movie_link):

		#将电影网址解析,将详情页解析为html
		movie_tree = self.get_movie_tree(movie_link)

		if movie_tree == None:
			return None

		#获取电影的所有信息
		#播放id（链接）
		id = self.get_movie_id(movie_tree)
		#print('电影播放id：	%s' %id)
		#电影名
		name = self.get_movie_name(movie_tree)
		#print('电影名：	%s' %name)
		#图片
		pic = self.get_movie_pic(movie_tree)
		#print('电影海报图片网址：	%s' %pic)
		#类型
		tag = self.get_movie_tag(movie_tree)
		#print('电影类型：	%s' %tag)
		#地区
		area = self.get_movie_area(movie_tree)
		#print('电影地区：	%s' %area)
		#评分
		score = self.get_movie_score(movie_tree)
		#print('电影豆瓣评分：	%s' %score)
		#时长(无)
		time = self.get_movie_time(movie_tree)
		#print(time)
		#简介
		intro = self.get_movie_intro(movie_tree)
		#print('电影简介：	%s' %intro)


		#存储电影信息的数组
		info = [id,name,pic,tag,area,score,time,intro]

		return info



	#html网站解析


	#解析html，并设置好编码格式，输出html(可以用xpath解析抓取内容)
	def analysis_html(self,url):
		
		response = requests.get(url,stream = True)

		#查看请求是否成功----------测试，200请求成功
		#print(response)

		html = response.content

		#识别编码
		code = detect(html)
		html = html.decode(code.get('encoding'))
		tree = etree.HTML(html)

		return tree


	#所有页的网址------（不断获得下一页的网址）
	def get_all_page_links(self,url):

		pages = []

		#不断获取下一页的网址，直到最后一页，从而实现爬取所有的电影页，并通过处理是网址可读存放在pages数组中
		while url:
			tree = self.analysis_html(url)
			a_s = tree.xpath('/descendant-or-self::li[@class = "next"]/a')

			if a_s:
				next_page = a_s[0].get('href')
				#为网址添加"http:"，使成为可访问的网址
				next_page = self.add_http(next_page)
				url = next_page
				pages.append(next_page)

			else:
				break


		return pages


	#获得所有免费首页每个地区分类网址，并进行解析为html
	def get_all_areatype_html(self,tree):

		all_areatype_html = []

		#找到标签为-----地区-----的标签，其对应的父div下放有地区分类电影网址的li标签
		area_a_s = tree.xpath(u'/descendant-or-self::div/label[text() = "地区："]/parent::div/ul/li/a')

		for a in area_a_s:
			if a != None:
				all_areatype_html.append(self.analysis_html(self.add_http(a.get('href'))))

		return all_areatype_html


	#为网址添加"http:"，使成为可访问的网址
	def add_http(self,url):

		#字符串首部插入-------http:-------使其成为可读取的网址
		if url.rfind('http:') == -1:
			#转换为数组进行插入
			str = list(url)
			str.insert(0,'http:')
			#转换回字符串
			url = ''.join(str)
			#print(url)
		else:
			return url
		
		return url



	#电影网址解析


	#得到当前页所有电影的网址链接
	def get_movie_link(self,tree):

		#所有电影的彼方链接，用于进一步爬取电影标签信息
		movie_links = []

		#a_s是存放每部电影播放链接和电影名字的标签
		a_s = tree.xpath('/descendant-or-self::div[@class = "yk-pack pack-film"]/descendant-or-self::li[@class = "title"]/a')

		for a in a_s:
			movie_links.append(self.add_http(a.get('href')))

		return movie_links


	#得到电影网址的可解析html，然后进入电影详情页，进一步解析该页为html，用于后续爬取
	def get_movie_tree(self,movie_link):

		#调用analysis_html函数解析电影播放网站，使其可爬取
		movie_tree = self.analysis_html(movie_link)
		#print(movie_tree)


		#解析电影详情页网址
		info_page_link_a = movie_tree.xpath('/descendant-or-self::code[@id = "bpmodule-playpage-righttitle-code"]/div/h2/a')

		if len(info_page_link_a) == 0:
			return None

		info_page_link = info_page_link_a[0].get('href')
		info_page_link = self.add_http(info_page_link)

		#------debug
		#print(info_page_link)

		info_page_tree = self.analysis_html(info_page_link)

		return info_page_tree


	#电影资源爬取，tree参数为每部电影的详情页解析html


	#获取电影的名字
	def get_movie_name(self,tree):

		#电影名所在的a标签
		name_a = tree.xpath('/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-thumb"]/a')
		#title属性存放电影名
		name = name_a[0].get('title')

		return name


	#获取电影的id
	def get_movie_id(self,tree):

		#id所在的a标签
		id_a = tree.xpath('/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-thumb"]/a')
		#href属性存放电影id，截取出来
		str = id_a[0].get('href')
		#分割字符串得到电影播放id
		id = str.split('/')[-1].split('_')[-1].split('.')[0]

		return id


	#获取电影图片链接
	def get_movie_pic(self,tree):

		#img所在的img标签
		img_s = tree.xpath('/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-thumb"]/img')
		#src属性存放电影的图片链接
		img = img_s[0].get('src')
		#网址补全
		img = self.add_http(img)

		return img


	#获取电影的上映时间
	def get_movie_time(self,tree):

		#电影上映时间所在的span标签
		timeplus_span = tree.xpath('/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-base"]/descendant-or-self::span[@class = "pub"]')
		#text()存放电影的上映事件信息
		timeplus = timeplus_span[0].xpath('string(.)').strip()
		#截取有效信息
		time = timeplus.split(':')[-1]

		return time


	#获取电影的豆瓣评分
	def get_movie_score(self,tree):

		#电影豆瓣评分所在的span标签
		score_span = tree.xpath('/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-base"]/descendant-or-self::li[@class = "p-score"]/span[@class = "star-num"]')

		if len(score_span) == 0:
			return '无'

		#text()存放电影的豆瓣评分
		score = score_span[0].text

		return score


	#获取电影的地区
	def get_movie_area(self,tree):

		area_s = ['中国','中国香港','中国台湾','韩国','日本','美国','法国','英国','德国','意大利','加拿大','印度','俄罗斯','泰国','其他']

		area = []

		for _area in area_s:
			#查找电影地区所在的a标签
			area_a_s = tree.xpath(u'/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-base"]/ul/descendant-or-self::a[@target = "_blank"]')
			
			for area_a in area_a_s:
				if area_a.text == _area:
					area.append(_area)

		return area



	#获取电影的类型
	def get_movie_tag(self,tree):

		#所有的电影标签
		tag_s = ['武侠','警匪','犯罪','科幻','战争','恐怖','惊悚','纪录片','西部','戏曲','歌舞','奇幻','冒险','悬疑','历史','动作','传记','动画','儿童','喜剧','爱情','剧情','运动','短片']

		#当前电影的所有标签（一部电影有多个标签）
		tags = []

		for _tag in tag_s:
			#查找电影类型所在的a标签
			tag_a = tree.xpath(u'/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-base"]/ul/descendant-or-self::a[@target = "_blank"]')

			for tag in tag_a:
				if tag.text == _tag:
					tags.append(_tag)
					continue

		return tags

		
	def get_movie_intro(self,tree):

		#获取电影简介所在的span标签
		intro_span = tree.xpath('/descendant-or-self::div[@class = "s-body"]/descendant-or-self::div[@class = "p-base"]/descendant-or-self::li[@class = "p-row p-intro"]/span[@class = "text"]')
		#获取电影简介
		intro = intro_span[0].xpath('string(.)').strip()

		return intro



#测试
#spider = ListSpider()