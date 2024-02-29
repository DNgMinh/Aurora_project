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
        print(entered_courses)
        # get term
        term = str(request.form.get('term'))
        courses = entered_courses.split()
        courses_list = []
        for course in courses:
            key = course[0:4]
            value = course[4:8]
            courses_list.append({key : value})

        print(courses_list)
        myResult = result.calculate_result(term, courses_list)

        return jsonify({'result': myResult})

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
