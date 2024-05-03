from flask import Flask, request, jsonify
from flask_cors import CORS
import result
import class_optimization
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

@app.route('/customization', methods=['POST'])
def customization():
    try:
        data = request.get_json()                                # This parses the JSON string into Python data structures (list)
        customizations_list = data['customizations']             # or data.get('customization', []) to get [] if no key found  

        # print("ff", customizations_list)
        customized_class_list_ways = class_optimization.class_list_ways.copy()      # have to use this list at the first iteration

        for customization in customizations_list:
            weekDay = customization["weekDay"]                   # "M" 
            dayTime = customization["dayTime"]                   # "morning"
            customTime = customization["customTime"]             # '12:30 pm-01:20 pm'
            customized_class_list_ways, ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = result.calculate_customization(customized_class_list_ways, weekDay, dayTime, customTime)

        # ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = result.calculate_customization(weekDay, dayTime, customTime)
        # print("fff", ways)
        # print("ffff", best_class_list)
        # print("There are " + customizedWays + " customized ways.")
        myCustomizationResult = {'customizedWays': ways, 'smallestCustomizedTimeGap': smallestTimeGap,'best_customized_class_list': best_class_list, 'startTime_list': startTime_list, 'endTime_list': endTime_list}
    
        return jsonify(myCustomizationResult)
    
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/loadSchedule', methods=['POST'])
def loadSchedule():
    try:
        data = request.get_json()                                
        scheduleIndex = int(data['scheduleIndex'])

        class_list_ways = class_optimization.class_list_ways.copy()

        if scheduleIndex == len(class_list_ways):
            scheduleIndex = 0
        elif scheduleIndex < 0:
            scheduleIndex = len(class_list_ways) - 1

        current_class_list = class_list_ways[scheduleIndex]
        startTime_list, endTime_list = class_optimization.startEndTimeList(current_class_list)
        timeGap = class_optimization.timeGapCalculation(current_class_list)[0]
        timeGap = format(timeGap, ".2f")

        myScheduleResult = {'scheduleIndex': scheduleIndex, 'timeGap': timeGap, 'currentSchedule': current_class_list, 'startTime_list': startTime_list, 'endTime_list': endTime_list}
        return jsonify(myScheduleResult)

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/loadCustomizedSchedule', methods=['POST'])
def loadCustomizedSchedule():
    try:
        data = request.get_json()                                
        scheduleIndex = int(data['scheduleIndex'])

        class_list_ways = class_optimization.new_customized_class_list_ways.copy()

        if scheduleIndex == len(class_list_ways):
            scheduleIndex = 0
        elif scheduleIndex < 0:
            scheduleIndex = len(class_list_ways) - 1

        current_class_list = class_list_ways[scheduleIndex]
        startTime_list, endTime_list = class_optimization.startEndTimeList(current_class_list)
        timeGap = class_optimization.timeGapCalculation(current_class_list)[0]
        timeGap = format(timeGap, ".2f")

        myScheduleResult = {'scheduleIndex': scheduleIndex, 'timeGap': timeGap, 'currentSchedule': current_class_list, 'startTime_list': startTime_list, 'endTime_list': endTime_list}
        return jsonify(myScheduleResult)

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

#  [{'MATH1240A06': ['11:30 am-12:20 pm', 'MWF']}, {'MATH1240B12': ['04:00 pm-04:50 pm', 'T']}, 
# {'COMP1010A01': ['12:30 pm-01:20 pm', 'MWF']}]