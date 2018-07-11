#coding:utf-8
from flask import Flask
from flask import request,flash
from flask import render_template
from s_lib.sutils import sxs_db
from s_lib.sxs_loan import get_loanID
from flask import Blueprint,jsonify

admin = Blueprint('admin', __name__)


#app = Flask(__name__)

@admin.route('/', methods=['GET', 'POST'])
def home():
	datas = [
	{'url':'/admin/create',
	'btn_name':'贷款端建标'}
	]
	return render_template('index.html',datas=datas)
#查询用户信息

	
	
#创建标的
@admin.route('/create', methods=['GET','POST'])
def create():
	return render_template('creatloan.html')

def loan(loan_type,idcard,times,title,money,month,yearRates,dailyRate):
	start_num =1
	times = int(times)
	while (start_num < times):
		data=get_loanID(loan_type,title,idcard,money,month,yearRates,dailyRate)
		start_num+=1
	return data
@admin.route('/create_loan', methods=['POST'])
def create_loan():
	loan_type = request.form['loantype']
	idcard = request.form['idcard']
	num = request.form['num']
	title = request.form['title']
	money = request.form['money']
	yearRates = request.form['yearRates']
	month=request.form['month']
	dailyRate=request.form['dailyRate']
	if dailyRate=='':
		print('日利率%s' % dailyRate)
	else:
		yearRates = float('%.2f' % (float(dailyRate)*360))
	print(yearRates,dailyRate)
	msg_code=loan(loan_type,idcard,num,title,money,month,yearRates,dailyRate)

	#flash(msg_code)
	print(msg_code)
	return jsonify(msg_code)
	



	

# if __name__ == '__main__':
	
	# app.run(host='0.0.0.0',port=5001,debug=True)
	