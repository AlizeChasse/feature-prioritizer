from flask import Flask, jsonify, request, render_template_string
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Anthropic()

features = []
next_id = 1

@app.route('/')
def index():
    with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r') as f:
        html = f.read()
    response = render_template_string(html)
    return response, 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }

@app.route('/features', methods=['GET'])
def get_features():
    sorted_features = sorted(features, key=lambda f: f['impact'] / f['effort'], reverse=True)
    return jsonify(sorted_features)

@app.route('/features', methods=['POST'])
def add_feature():
    global next_id
    data = request.json
    feature = {
        'id': next_id,
        'name': data['name'],
        'impact': data['impact'],
        'effort': data['effort'],
        'score': round(data['impact'] / data['effort'], 1)
    }
    features.append(feature)
    next_id += 1
    return jsonify(feature), 201

@app.route('/features/<int:feature_id>', methods=['DELETE'])
def delete_feature(feature_id):
    global features
    features = [f for f in features if f['id'] != feature_id]
    return jsonify({'message': 'deleted'}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    if not features:
        return jsonify({'error': 'No features to analyze'}), 400
    
    list_str = '\n'.join([f"- {f['name']} (impact {f['impact']}/5, effort {f['effort']}/5, score {f['score']})" for f in features])
    
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Tu es un product manager expert. Voici un backlog de features :\n{list_str}\n\nEn 2-3 phrases max, donne une recommandation de priorisation claire et actionnable."
        }]
    )
    
    return jsonify({'recommendation': message.content[0].text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))