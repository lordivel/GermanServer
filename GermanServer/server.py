from flask import Flask, jsonify, abort, make_response, request, render_template
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String

engine = create_engine('sqlite:///test.db', convert_unicode=True)
metadata = MetaData(bind=engine)

app = Flask(__name__)

user = Table('USER', metadata, autoload=True)
mark = Table('MARK', metadata, autoload=True)

con = engine.connect()
con.execute(user.insert(), nome='admin', login = 'admin', email='admin@localhost', senha='teste123')
con.execute(user.insert(), nome='admin2', login = 'admin Rafael teste2', email='admin35k28@localhost', senha='teste1')
con.execute(mark.insert(), title='My Trip to Germany', link = '9peAsDZwiiQ', description='Just testing', userlogin='admin', latitude='5', longitude='5')
con.execute(mark.insert(), title='First Impressions', link = '49gVihPIX3Q', description='Just chillin', userlogin='admin2', latitude='10', longitude='10')

users = [
	{
	'login' : 'admin',
	'passwd': 'teste123'
	},
	{'login' : 'admin2',
	'passwd' : 'teste123'
	}
	]

experiences = [
    {
        'id': 1,
        'title': u'My Trip to Germany',
        'link': u'9peAsDZwiiQ', 
        'desc': "Just testing",
		'lat': '5',
		'lng': '5'
    },
    {
        'id': 2,
        'title': u'First Impressions',
        'link': u'49gVihPIX3Q', 
        'desc': "Just testing 2",
		'lat': '10',
		'lng': '10'
    }
]
# WORKING PART
@app.route('/')
def index():
    return "Hello, World!"
    
@app.route('/clipcultexperiences/api/v1.0/login', methods=['GET'])
def get_login():
    user = [user for user in users if user['login'] == request.json.get('login','')]
    if len(user) == 0:
        abort(404)
    if request.json.get('passwd','') != user[0]['passwd']:
		abort(401)
    return jsonify({'auth_result': 'success'})

@app.route('/clipcultexperiences/api/v1.0/experiences/<int:experience_id>', methods=['GET'])
def get_experience(experience_id):
    experience = [experience for experience in experiences if experience['id'] == experience_id]
    if len(experience) == 0:
        abort(404)
    return jsonify({'experience': experience[0]})

@app.route('/clipcultexperiences/api/v1.0/experiences', methods=['GET'])
def get_experiences():
    return jsonify({'experiences': experiences})
    
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not found'}),404)
	
@app.errorhandler(401)
def auth_failure(error):
	return make_response(jsonify({'auth_result':'failure'}),401)

@app.route('/clipcultexperiences/api/v1.0/experiences/', methods=['POST'])
def new_experience():
    if not request.json or not 'link' in request.json or not 'title' in request.json:
        abort(400)
    experience = {
        'id': experiences[-1]['id'] + 1,
        'link': request.json['link'],
        'title': request.json.get('title',''),
        'desc': request.json.get('desc',''),
        'lat' : request.json.get('lat',""),
        'lng' : request.json.get('lng',"")
    }
    experiences.append(experience)
    return jsonify({'experience': experience}), 201
    
@app.route('/clipcultexperiences/api/v1.0/experiences/<int:experience_id>', methods=['DELETE'])
def delete_experience(experience_id):
    experience = [experience for experience in experiences if experience['id'] == experience_id]
    if len(experience) == 0:
        abort(404)
    experiences.remove(experience[0])
    return jsonify({'result': True})
    
# END OF WORKING PART

# ALPHA PART    
    
@app.route('/clipcultexperiences/api/alpha/login', methods=['GET'])
def alpha_login():
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})

@app.route('/clipcultexperiences/api/alpha/experiences/<int:experience_id>', methods=['GET'])
def alpha_experience(experience_id):
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})


@app.route('/clipcultexperiences/api/alpha/experiences', methods=['GET'])
def alpha_experiences():
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})


@app.route('/clipcultexperiences/api/alpha/experiences/', methods=['POST'])
def alpha_new_experience():
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})

    
@app.route('/clipcultexperiences/api/alpha/experiences/<int:experience_id>', methods=['DELETE'])
def alpha_delete_experience(experience_id):
    return "Hello, World!"
    #return jsonify({'auth_result': 'success'})

    
#END OF ALPHA PART
    
#HTML PART    
    
@app.route('/clipcultexperiences/api/v1.0/map')
def render_map():
	return render_template('map.html')
    
@app.route('/clipcultexperiences/api/v1.0/form')
def render_form():
	return render_template('form.html')
	
#END OF HTML PART
    
#INITIALIZE
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    
