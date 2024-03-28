from flask import Flask, request, jsonify
from flask_cors import CORS
import result
# from result import calculate_result

app = Flask(__name__)
CORS(app)

@app.route('/schedule', methods=['POST'])
def schedule():
    try:
        entered_courses = str(request.form.get('courses'))   # courses is key, we are getting its value
        # print(entered_courses)
        # get term
        term = str(request.form.get('term'))
        courses = entered_courses.split()
        courses_list = []
        for course in courses:
            key = course[0:4]
            value = course[4:8]
            courses_list.append({key : value})

        # print(courses_list)
        ways, smallestTimeGap, best_class_list, printResult, startTime_list, endTime_list = result.calculate_result(term, courses_list)
        print(printResult)
        myResult = {'ways': ways, 'smallestTimeGap': smallestTimeGap, 'best_class_list': best_class_list, 'startTime_list': startTime_list, 'endTime_list': endTime_list}
        # Keys of dict can be of any immutable data type, such as integers, strings, tuples,
        return jsonify(myResult)

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

#  [{'MATH1240A06': ['11:30 am-12:20 pm', 'MWF']}, {'MATH1240B12': ['04:00 pm-04:50 pm', 'T']}, 
# {'COMP1010A01': ['12:30 pm-01:20 pm', 'MWF']}]