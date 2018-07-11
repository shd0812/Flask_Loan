#coding:utf-8
import requests
import json
import os
from yaml import load
from s_lib.sutils import sxs_db,shd_time,operate_file
from time import sleep
from configparser import ConfigParser
from s_conf.setting import *

def get_url(name):

	dd_config = ConfigParser()
	dd_config.read(Config_PATH)

	return dd_config['login_url'][name]

#从配置文件获取标的所有内容
def get_data(loantype):
	if loantype =='fang':
		config_path=FANG_PATH
	else:
		config_path=QI_PATH
	with open(config_path,'rb') as f:
		cont=f.read()
		s=load(cont)
		#print (s)
	return s

#更新标的未待招标，省去上传图片流程	
def updata(loanId):
	my_db =sxs_db('sxs_loan')
	sql = "UPDATE vault_loan SET state =4 WHERE  state=1  AND id=%s " % loanId
	#print (sql)
	print (my_db.get_data(sql))
	
#获取贷款端的cookies
def base_request():
	login_url = get_url('login')
	
	#session = requests.Session()
	#获取用户名和密码
	operate_files = operate_file(Config_PATH)
	data=operate_files.open()['user_info']
	login_data = {'account':data['mobile'],'passWord':data['passwd'],'pass':data['passcode']}
	r=requests.post(login_url,login_data)
	_cookies=r.cookies
	#print(_cookies)
	return _cookies

	
	#return session
def get_person(idCard):
	my_db =sxs_db('sxs_borrower')
	sql = "SELECT realName,mobile,userNumber FROM bor_user_personal WHERE idCard = '%s'" % idCard
	
	data = my_db.get_data(sql)
	
	return data[0]
# 1 统一社会信用代码 仅支持社会统一信用代码 2 营业执照
def get_qiye(code):
		my_db =sxs_db('sxs_borrower')
		sql = "SELECT userNumber,companyName,contact,contactIDCard,contactPersonName,contactPersonPhone,unifiedCode,creditCode,bankLicense FROM bor_user_company WHERE unifiedCode = '%s'" % code
		data = my_db.get_data(sql)
		return data[0]
	
		
	
#提交标的  file_name:yaml文件名字  type：1 个人贷 2 企业贷  title：借款标题 
def get_loanID(file_name,title,idCard,money,month,yearRates,dailyRate):
	test_url,qi_url = get_url('person'),get_url('bus')
	data = get_data(file_name)
	form_data =(data['data'])
	sxs_time = shd_time()
	str1 = str(sxs_time.getTimestamp())
	lenth = len(str1)
	title1=str1[lenth-4:lenth]
	title = title+title1
	form_data['title'] = title
	if file_name == 'qi':
		type=2
	else:
		type=1
		
	if type == 1:
		dic = get_person(idCard)
		form_data['username'] = dic['realName']
		form_data['mobile']= dic['mobile']
		form_data['xwUserNo']= dic['userNumber']
		form_data['money']=money
		form_data['loanTerm']=month
		form_data['idcard']=idCard
		form_data['yearRates']=yearRates
	else:
		dic = get_qiye(idCard)
		form_data['xwUserNo']=dic['userNumber']
		form_data['enterprise']=dic['companyName']
		
		form_data['legalName']=dic['contact']
		form_data['legalMobile']=dic['contactPersonPhone']
		form_data['legalIdcard']=dic['contactIDCard']
		form_data['socialCreditCode']=idCard
		form_data['bankLicense']=dic['bankLicense']
		form_data['creditCode']=dic['creditCode']
		form_data['money']=money
		form_data['loanTerm']=month
		form_data['yearRates'] = yearRates
		if dailyRate !='':
			form_data['dailyRate'] = dailyRate
			form_data['repayMethod']='2'
			form_data['loanTermType']='1'
			form_data['isCarMerchant']='6'
		#print (dic)
	#print (form_data) 112164362286
	cookies = base_request()
	if type == 1:
		url =test_url
	else:
		url = qi_url
	#print (form_data)
	r=requests.post(url,form_data,cookies=cookies)
	res_vault=r.json()
	print(res_vault)
	code = res_vault['code']
	if code =='-1':
		return res_vault['error']
	else:
		loanId=res_vault['data']['loanId']
		updata(loanId)
		sleep(1)
		ZB_URL= get_url('tender')
		ZB_data={'loanid':loanId,'status':'zbz'}
		reponse=requests.post(ZB_URL,ZB_data,cookies=cookies)
		msg_code=reponse.json()
		print(msg_code['msg'])
		return msg_code['msg']


# def vault_baseRequest():
# 	print(1111)
# 	login_url='https://ts.shaxiaoseng.com:4433/Vault/vault.php/Login/inLogin.html'
# 	login_data='mobile=13521137793&password=96e79218965eb72c92a549dd5a330112&verify_code=111111'
# 	r=requests.post(login_url,login_data)
# 	return r.cookies
#
# def get_loanInfo(loanId):
# 	my_db =sxs_db('sxs_loan')
# 	sql = "SELECT realName,mobile,userNumber FROM bor_user_personal WHERE idCard = '%s'" % idCard
#
# 	data = my_db.get_data(sql)
#
# 	return data[0]
	
	

if __name__=='__main__':
	# vault_baseRequest()
	print(11111)
	# start_num =1
	# times=2
	# while (start_num < times):
		# title='111批量交易款'
		# get_loanID('fang',title,'110101198101010544',100,3)
		# start_num+=1
	

