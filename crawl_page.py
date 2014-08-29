#!/usr/bin/python
#-*- coding=utf-8 -*-

import weibologin as wl 
import requests
import re
import base62
from config import setting
from lxml import html
import json
import time
from db import Database


class Crawler(object):
	def __init__(self):
		super(Crawler, self).__init__()
		username = setting.get("username","")
		password = setting.get("password","")

		self.db = Database()

		self.cookie_file = setting.get("cookie_file","")
		self.cookie_jar = wl.login(username,password,self.cookie_file)

		self.access_token = setting.get("access_token","")
		#STK.pageletM.view({"pid":"pl_service_showcomplaint"
		self.uid_pattern = re.compile("[0-9]{4,10}")
		self.complain_pattern = re.compile("STK.pageletM.view\(({\"pid\":\"pl_service_showcomplaint\".*?)\)</script>")
		self.detail_pattern = re.compile("STK.pageletM.view\(({\"pid\":\"pl_service_common\".*?)\)</script>")
		
		self.domain_url = "https://api.weibo.com/2/users/domain_show.json?access_token={access_token}&domain={domain}"
		self.uid_url = "https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}"
		self.weibo_url = "https://api.weibo.com/2/statuses/show.json?access_token={access_token}&id={mid}"
		self.start_urls = [	
							#不实信息,内容抄袭,冒充他人
							("http://service.account.weibo.com/?type=5&status=1",5),
							("http://service.account.weibo.com/?type=9&status=1",9),
							("http://service.account.weibo.com/?type=10&status=1",10)
						  ]

		self.url_prefix = "http://service.account.weibo.com"

		if self.cookie_jar:
			self.rsession = requests.session()
			self.rsession.cookies = self.cookie_jar
			self.rsession.headers["user-agent"] = setting.get("User-Agent","")
		else:
			print "login failed"
			return None

	#get component html hidden in the script
	def get_script_component(self,pattern,content):
		match = pattern.search(content)
		if match:
			try:
				json_object = json.loads(match.group(1))
				if json_object:
					return json_object.get("html",None)
			except:
				return None
		return None

	def get_user_by_uid(self,uid="3529773021"):
		next_url = self.uid_url.format(access_token = self.access_token,uid = uid)
		resp = requests.get(url=next_url)
		json_object =  resp.json()
		self.save_user_info_to_db(json_object,uid)
		
	def get_user_by_domain(self,uname="openapi"):
		next_url = self.domain_url.format(access_token = self.access_token, domain= uname)
		resp = requests.get(url=next_url)
		json_object =  resp.json()
		self.save_user_info_to_db(json_object)

	def save_user_info_to_db(self,json_object,uname):

		user_info_dict = dict()

		user_info_dict["udomain"] = uname
		user_info_dict["idstr"] = json_object.get("idstr","")
		user_info_dict["name"] = json_object.get("name","")
		user_info_dict["location"] = json_object.get("location","")
		user_info_dict["description"] = json_object.get("description","")
		user_info_dict["gender"] = json_object.get("gender","")
		user_info_dict["followers_count"] = json_object.get("followers_count",0)
		user_info_dict["friends_count"] = json_object.get("friends_count",0)
		user_info_dict["statuses_count"] = json_object.get("statuses_count",0)
		user_info_dict["favourites_count"] = json_object.get("favourites_count",0)
		user_info_dict["created_at"] = json_object.get("created_at",0)
		user_info_dict["verified"] = json_object.get("verified",False)
		user_info_dict["verified_type"] = json_object.get("verified_type",-1)
		user_info_dict["verified_reason"] = json_object.get("verified_reason","")
		user_info_dict["bi_followers_count"] = json_object.get("bi_followers_count",0)

		self.db.insert("user",user_info_dict)



	def crawl_user(self,person_url="http://weibo.com/u/3529773021"):
		user_text = person_url.rsplit("/",1)[-1]
		#if user already exists in database 
		#ignore it

		if self.db.is_key_exist("user","udomain",user_text):
			return
		if self.uid_pattern.match(user_text):
			self.get_user_by_uid(user_text)
		else:
			self.get_user_by_domain(user_text)


	def crawl_service(self,url="http://service.account.weibo.com/?type=0&status=1",report_type=5):

		resp = self.rsession.get(url=url)	
		html_text = self.get_script_component(self.complain_pattern,resp.content)
		if html_text:
			html_xpath = html.fromstring(html_text)
			table_rows = html_xpath.xpath("//tr")
			for row in table_rows[1:]:
				#print row
				task_url = row.xpath("td/div[@class='m_table_tit']/a/@href")[0]
				user_urls = row.xpath("td/a/@href")
				ret_result = self.crawl_detail(self.url_prefix + task_url,user_urls,report_type)
				if not ret_result:
					break
				for user_url in user_urls:
					self.crawl_user(user_url)
				time.sleep(setting.get("download_delay",10))
		else:
			self.deal_with_redirect(resp.content,url,report_type)

	def crawl_weibo_content(self,url):
		content_dict = dict()


		mid_encoded = url.rsplit('/',1)[-1]
		mid = base62.url_to_mid(mid_encoded)
		next_url = self.weibo_url.format(access_token=self.access_token,mid=mid)
		resp = requests.get(url=next_url)
		json_object = resp.json()

		created_at =  json_object.get("created_at","")
		time_struct = time.strptime(created_at,"%a %b %d %H:%M:%S +0800 %Y")
		content_dict["weibo_create_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time_struct)


		content_dict["report_origin_text"] =  json_object.get("text","")
		content_dict["weibo_comment_count"] =  json_object.get("comments_count",0)
		content_dict["weibo_repost_count"] =  json_object.get("reposts_count",0)
		content_dict["weibo_like_count"] =  json_object.get("attitudes_count",0)

		return content_dict

		#print json_object


	def start_crawl(self):

		for url in self.start_urls:
			print url
			self.crawl_service(url[0],url[1])



	def deal_with_redirect(self,content,url,report_type):
		redirect_pattern = re.compile("replace\(\"(.*?)\"\)")
		redirect_match = redirect_pattern.search(content)
		if redirect_match:
			resp = self.rsession.get(url=redirect_match.group(1))			
			self.cookie_jar.save(self.cookie_file,ignore_discard=True, ignore_expires=True)
			self.rsession.cookies = self.cookie_jar
			self.crawl_service(url=url,report_type=report_type)
	#="http://service.account.weibo.com/show?rid=K1CaL7Axj6q0i"
	def crawl_detail(self,url,user_urls,report_type=5):


		rid = url.rsplit("=")[-1]

		#if there is already one in database ignore the rest
		# if self.db.is_key_exist("report_info","rid",rid):
		# 	return False

		report_info_dict = dict()
		report_info_dict["rid"] = rid
		report_info_dict["report_type"] = report_type
		report_info_dict["reporter"] = user_urls[0].rsplit('/',1)[-1]
		report_info_dict["bereporteder"] = user_urls[1].rsplit('/',1)[-1]

		resp = self.rsession.get(url=url)
		html_text = self.get_script_component(self.detail_pattern,resp.content)

		if not html_text:
			self.deal_with_redirect(resp.content,url,user_urls,report_type)
		else:
			html_xpath = html.fromstring(html_text)
			report_count_text =  html_xpath.xpath('//span[@class="W_f12 W_textb"]/text()')[0]
			report_count = 1
			try:
				report_count = int(re.search('\d+',report_count_text).group(0))
			except:
				pass
			report_info_dict["report_count"] = report_count
			# #if it is not multi pages
			# if not html_xpath.xpath('//div[@class="W_main_half_l"]//div[@class="page"]'):
				#get first report time
			report_time_str = html_xpath.xpath('//div[@class="W_main_half_l"]//div[@class="item"][last()]/p/text()')
			report_time = report_time_str[0].lstrip(u"举报人陈述时间：")
			report_info_dict["first_report_time"] = report_time
			
			#get the original weibo url
			origin_text_url = html_xpath.xpath('//div[@class="W_main_half_r"]//div[@class="item top"]/p/a/@href')
			
			#if there is original text
			if origin_text_url:
				content_dict  = self.crawl_weibo_content(origin_text_url[0])
				report_info_dict.update(content_dict)
			else:
				report_type_str = html_xpath.xpath('//div[@class="W_main_half_r"]//div[@class="item top"]/p/text()')[0]
				report_type_str = report_type_str.replace("\t","").replace("\n","").strip()
			
				#被举报的用户
				if report_type_str == u'被举报用户':
					report_info_dict["report_type"] = 101
				#user have deleted the weibo
				else:
					text =  html_xpath.xpath('//div[@class="W_main_half_r"]//div[@class="item top"]//div[@class="con"]/text()')[0]
					report_info_dict["report_origin_text"] = text
			self.db.insert("report_info",report_info_dict)
			return True

if __name__ == "__main__":
	crawler = Crawler()
	#crawler.crawl_service()	
	#crawler.crawl_detail()
	crawler.start_crawl()
	#crawler.crawl_user()
	#crawler.get_user_by_domain()
	#crawler.crawl_last_page()