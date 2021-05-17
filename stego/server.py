'''
Program: server.py

Description serve up the demo page for my use
as well as the exploit code within the image 

TODO:
	serve the static html (render template)
	serve the static js files to the html
'''

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)


@app.route('/analysis')
def analysis():
	return render_template('image_layer_analysis.html')
	
# Note: for this route, the server needs to allow cross-
#		origin images and I need to modify:
#			iterative_encoding.html:112
#		in order to set the image origin anonymous
# 		
#		Example:
#			Access-Control-Allow-Origin "*"
@app.route('/encoding')
def encoding():
	resp = make_response(render_template('iterative_encoding.html'))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

@app.route('/stego.jpg')
def stego():
	return app.send_static_file('img/out3.jpg')

@app.route('/poc')
def poc():
	return app.send_static_file('poc.txt')

@app.route('/exploit.jpg')
def exploit():
	return app.send_static_file('img/exploit.jpg')

@app.route('/out3')
def out3():
	return app.send_static_file('out3.html')


@app.route('/')
def index():
	return """
		<!DOCTYPE html>
		<html>
		<body>
			<h1>Stegosploit Demo Server</h1>
			<ul>
				<li><a href='/'>Home</a></li>
				<li><a href='/analysis'>Image Layer Analysis (Working)</a></li>
				<li><a href='/encoding'>Iterative Encoding</a></li>
				<li><a href='/exploit.jpg'>Exploit!</a></li>
			</ul>
		</body>
		</html>
		"""

def main():
	app.run(host='localhost',
			port=5000,
			debug=True)

if __name__ == '__main__':
	main()