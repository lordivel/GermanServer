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

users = [
	{
	'login' : 'admin',
	'passwd': 'testewarhammer40k',
	'name' : 'Rafael',
	'email' : 'xd@gmail.com'
	},
	{'login' : 'admin2',
	'passwd' : 'teste123',
	'name' : 'Rafael',
	'email' : 'xd2@outlook.com'
	}
	]

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
    user = [user for user in users if user['login'] == request.json.get('login','')]
    if len(user) == 0:
        abort(401)
    if request.json.get('passwd','') != user[0]['passwd']:
		abort(401)
    con = engine.connect()
    con.execute(mark.insert(), title= request.json.get('title','') , link = request.json['link'] , description= request.json.get('desc','') , user=request.json.get('login','') , latitude = request.json.get('lat',""), longitude = request.json.get('lng',""))
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
def auth_failure(error):
	return make_response(jsonify({'error':'One of The Required Fields is Missing'}),400)
    
# END OF WORKING PART

# ALPHA PART    
    
@app.route('/clipcultexperiences/api/alpha/login', methods=['GET'])
def alpha_login():
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})


@app.route('/clipcultexperiences/api/alpha/experiences/', methods=['POST'])
def alpha_new_experience():
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})

#END OF ALPHA PART
    
#HTML PART    
    
#@app.route('/clipcultexperiences/api/v1.0/map')
#def render_map():
	#return render_template('map.html')
    
#@app.route('/clipcultexperiences/api/v1.0/form')
#def render_form():
	#return render_template('form.html')
	
@app.route('/clipcultexperiences/api/v1.0/index')
def render_index():
	return render_template('index.html')
	
#END OF HTML PART
    
#INITIALIZE
if __name__ == '__main__':
    app.run(debug=True, port = 80)
    
