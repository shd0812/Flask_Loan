from flask import Flask,render_template
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
app.secret_key = '123'






from view.shd_view import admin
app.register_blueprint(admin,url_prefix='/admin')



@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    #app.run(host='192.168.110.53',port=1314,debug=True)  python manager.py runserver --host 0.0.0.0 --port 1314
#    app.run(debug=True)
	manager.run()
