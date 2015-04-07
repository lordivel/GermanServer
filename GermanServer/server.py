from flask import Flask, jsonify, abort, make_response, request, render_template

app = Flask(__name__)

experiences = [
    {
        'id': 1,
        'title': u'My Trip to Germany',
        'link': u'https://www.youtube.com/watch?v=9peAsDZwiiQ', 
        'desc': "Just testing",
		'lat': '10',
		'lng': '10'
    },
    {
        'id': 2,
        'title': u'First Impressions',
        'link': u'https://www.youtube.com/watch?v=49gVihPIX3Q', 
        'desc': "Just testing 2",
		'lat': '10',
		'lng': '10'
    }
]
@app.route('/')
def index():
    return "Hello, World!"
    
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
    
@app.route('/clipcultexperiences/api/v1.0/map')
def render_map():
	return render_template('map.html')
    
@app.route('/clipcultexperiences/api/v1.0/form')
def render_form():
	return render_template('form.html')
    

if __name__ == '__main__':
    app.run(debug=True)
    
