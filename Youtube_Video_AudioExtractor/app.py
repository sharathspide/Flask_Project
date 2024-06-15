from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_input = data.get('user_input')
    processed_data = user_input.upper()  # Example processing
    return jsonify({'processed_data': processed_data})

if __name__ == '__main__':
    app.run(debug=True)
