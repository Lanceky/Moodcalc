from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from scipy import stats

app = Flask(__name__)
CORS(app)

def perform_calculation(operation, numbers, mood):
    result = None
    if operation == 'sum':
        result = np.sum(numbers)
    elif operation == 'mean':
        result = np.mean(numbers)
    elif operation == 'median':
        result = np.median(numbers)
    elif operation == 'mode':
        result = stats.mode(numbers).mode[0]
    
    # Adjust precision based on mood
    if mood in ['Excited', 'Confident']:
        return round(result, 5)  # More precise for positive moods
    else:
        return round(result, 2)  # Less overwhelming for other moods

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    operation = data['operation']
    numbers = data['numbers']
    mood = data['mood']
    
    result = perform_calculation(operation, numbers, mood)
    return jsonify({'result': result})

def suggest_resources(mood, topic):
    # Simplified resource suggestion
    resources = {
        'algebra': [
            {'title': 'Basic Algebra', 'difficulty': 1},
            {'title': 'Intermediate Algebra', 'difficulty': 2},
            {'title': 'Advanced Algebra', 'difficulty': 3}
        ],
        'calculus': [
            {'title': 'Limits and Continuity', 'difficulty': 2},
            {'title': 'Derivatives', 'difficulty': 3},
            {'title': 'Integrals', 'difficulty': 3}
        ]
    }
    
    topic_resources = resources.get(topic, [])
    
    if mood in ['Excited', 'Confident']:
        return [r for r in topic_resources if r['difficulty'] >= 2]
    elif mood == 'Neutral':
        return topic_resources
    else:  # 'Anxious' or 'Frustrated'
        return [r for r in topic_resources if r['difficulty'] <= 2]

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    mood = data['mood']
    topic = data['topic']
    
    suggested_resources = suggest_resources(mood, topic)
    return jsonify({'resources': suggested_resources})

if __name__ == '__main__':
    app.run(debug=True)

