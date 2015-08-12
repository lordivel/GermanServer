from flask import Flask, jsonify, abort, make_response, request, render_template
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String

engine = create_engine('sqlite:///test.db', convert_unicode=True)
metadata = MetaData()
metadata.reflect(bind=engine)
user = metadata.tables['USER']
mark = metadata.tables['MARK']

app = Flask(__name__)

#con = engine.connect()
#con.execute(user.insert(), nome='admin', login = 'admin', email='admin@localhost', senha='teste123')
#con.execute(user.insert(), nome='admin2', login = 'admin Rafael teste2', email='admin35k28@localhost', senha='teste1')
#con.execute(mark.insert(), title='My Trip to Germany', link = '9peAsDZwiiQ', description='Just testing', user='admin', latitude='5', longitude='5')
#con.execute(mark.insert(), title='First Impressions', link = '49gVihPIX3Q', description='Just chillin', user='admin2', latitude='10', longitude='10')

# WORKING PART

@app.route('/clipcultexperiences/api/v1.0/experiences/<int:experience_id>', methods=['GET'])
def get_experience(experience_id):
	con = engine.connect()
	result = con.execute("select * from mark where id =" + str(experience_id))
	returnData = []
	for row in result:
		experience = {
		'id': row["id"],
        'title': row["title"],
        'link': row["link"], 
        'desc': row["description"],
		'lat': row["latitude"],
		'lng': row["longitude"],
		'user': row["user"]
		}
		returnData.append(experience)
	con.close()
	return jsonify({'experiences': returnData})

@app.route('/clipcultexperiences/api/v1.0/experiences', methods=['GET'])
def get_experiences():
	con = engine.connect()
	result = con.execute("select * from mark")
	returnData = []
	for row in result:
		experience = {
		'id': row["id"],
        'title': row["title"],
        'link': row["link"], 
        'desc': row["description"],
		'lat': row["latitude"],
		'lng': row["longitude"],
		'user': row["user"]
		}
		returnData.append(experience)
	con.close()
	return jsonify({'experiences': returnData})

@app.route('/clipcultexperiences/api/v1.0/experiences/', methods=['POST'])
def new_experience():
    if not request.json or not 'link' in request.json or not 'title' in request.json or not 'desc' in request.json or not 'lat' in request.json or not 'lng' in request.json:
        abort(400)
    if request.json['link'] == '' or request.json['title'] == '' or request.json['desc'] == '' or request.json['lat'] == '' or request.json['lng'] == '':
        abort(400)
    userlogin = request.json.get('login','')
    passwd = request.json.get('passwd','')
    if len(userlogin) == 0:
        abort(401)
    con = engine.connect()
    userresult = con.execute("select * from user where login = \"" + userlogin + "\"").first()
    if userresult is None:
		con.close()
		abort(401)
    if userresult["passwd"] != passwd:
		con.close()
		abort(401)
    con.execute(mark.insert(), title= request.json.get('title','') , link = request.json['link'] , description= request.json.get('desc','') , user=userlogin , latitude = request.json.get('lat',""), longitude = request.json.get('lng',""))
    con.close()
    return jsonify({'Resultado': "Inserido com Sucesso"}), 201
    
@app.route('/clipcult/api/v1.0/user', methods=['POST'])
def new_user():	
	if not request.json or not 'name' in request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json or not 'passwordconfirm' in request.json:
		abort(400)
	if request.json['name'] == '' or request.json['username'] == '' or request.json['email'] == '' or request.json['password'] == '' or request.json['passwordconfirm'] == '':
		abort(400)
	if request.json['password'] != request.json['passwordconfirm']:
		abort(400)
	con = engine.connect()
	userresult = con.execute("select * from user where login = \"" + request.json['username'] + "\"").first()
	if userresult is not None:
		con.close()
		abort(400)
	con.execute(user.insert(), name= request.json.get('name','') , login = request.json.get('username','') , email= request.json.get('email','') , passwd= request.json.get('password',''))
	con.close()
	return jsonify({'Resultado': "Inserido com Sucesso"}), 201
	
	

# ERROR HANDLING

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)
	
@app.errorhandler(401)
def auth_failure(error):
	return make_response(jsonify({'error':'Authentication Failure'}),401)
	
@app.errorhandler(400)
def field_error(error):
	return make_response(jsonify({'error':'One of The Required Fields is Missing'}),400)
	
@app.errorhandler(500)
def internal_server_error(error):
	return make_response(jsonify({'error':'Ja existe um'}),500)
    
# END OF WORKING PART

# ALPHA PART    
    
#HTML PART    
    
@app.route('/clipcultexperiences/api/v1.0/map')
def render_map():
	return render_template('map.html')
	
@app.route('/clipcultexperiences/api/v1.0/index')
def render_index():
	return render_template('index.html')
	
@app.route('/clipcult/api/v1.0/index', methods=['GET','POST'])
def render_clipcult_index():
	return render_template('clipcultindex.html')
	
@app.route('/clipcult/api/v1.0/signup')
def render_clipcult_signup():
	return render_template('signup.html')
	
@app.route('/clipcult/api/v1.0/login')
def render_login():
	return render_template('signin.html')
	
@app.route('/clipcult/api/v1.0/emporio')
def render_emporio():
	return render_template('emporio.html')
	
@app.route('/clipcult/api/v1.0/emporio/4')
def render_video4():
	return render_template('4.html')
	
@app.route('/clipcult/api/v1.0/emporio/recursos')
def render_recursos():
	return render_template('recursos.html')
	
	
#END OF HTML PART
    
#INITIALIZE
if __name__ == '__main__':
    app.run(debug=True, port = 80)
    
