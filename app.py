from flask import Flask, request, jsonify
from flask_cors import CORS
import result
# from result import calculate_result

app = Flask(__name__)
CORS(app)

@app.route('/schedule', methods=['POST'])
def schedule():
    try:
        entered_courses = str(request.form.get('courses'))   # number is key, we are getting its value


        myResult = result.calculate_result(entered_courses)

        return jsonify({'result': myResult})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
