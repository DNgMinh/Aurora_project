from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_caching import Cache
import result
import class_optimization
import sys
import redis
import json
# from result import calculate_result

sys.stderr.flush()
sys.stdout.flush()

app = Flask(__name__)
# cache = Cache(app, config={
#     'CACHE_TYPE': 'redis',
#     'CACHE_REDIS_HOST': 'localhost', # Replace with your server's IP address
#     'CACHE_REDIS_PORT': 6379,          # The default Redis port
#     'CACHE_REDIS_DB': 0,                # Database number (optional)
#     #'CACHE_REDIS_PASSWORD': 'your-password', # If you've set a password
#     'CACHE_REDIS_URL': 'redis://localhost:6379/0',
#     'CACHE_DEFAULT_TIMEOUT': 300        # Cache expiration in seconds
# })
redis_client = redis.Redis(host='localhost', port=6379, db=0)
CORS(app)

@app.route('/schedule', methods=['POST'])
def schedule():
    try:
        entered_courses = str(request.form.get('courses'))   # courses is key, we are getting its value
        # print(entered_courses)
        # get term
        term = str(request.form.get('term'))
        term = term.lower()
        entered_courses = entered_courses.lower()

        if term[0:4] == "fall":
            term = term[-4:] + "90"
        elif term[0:6] == "winter":
            term = term[-4:] + "10"
        elif term[0:6] == "summer":
            term = term[-4:] + "50"  

        #cache_key = f"schedule_{hash(frozenset(entered_courses))}_{hash(frozenset(term))}"
        sorted_courses = ' '.join(sorted(entered_courses.split()))
        cache_key = f"schedule_{sorted_courses}_{term}"
        
        # Check if the result is already in the cache
        cached_result = redis_client.get(cache_key)
        if cached_result is not None:
            print("-----------------------------")
            print("CACHED", flush=True)
            cached_result = json.loads(cached_result.decode('utf-8'))
            print(cached_result['best_class_list'], flush=True)
            return jsonify(cached_result)

        courses = entered_courses.split()
        courses_list = []
        for course in courses:
            course = course.upper()
            if len(course) == 8:
                key = course[0:4]
                value = course[-4:]
            elif len(course) == 7:
                key = course[0:3]
                value = course[-4:]
            else:
                key = course[0:len(course) - 1]
                value = course[-1:]
            courses_list.append({key : value})      

        # print(courses_list)
        error, ways, smallestTimeGap, best_class_list, printResult, startTime_list, endTime_list, class_list_ways, weirdCourses = result.calculate_result(term, courses_list)
        if error == "none":
            print("--------------------------------------------------------------------------------")
            print(term, flush=True)
            print(printResult, flush=True)
            print("--------------------------------------------------------------------------------")
            myResult = {'ways': ways, 'smallestTimeGap': smallestTimeGap, 'best_class_list': best_class_list, 'startTime_list': startTime_list, 'endTime_list': endTime_list, 'class_list_ways': class_list_ways, 'weirdCourses': weirdCourses}
            # Keys of dict can be of any immutable data type, such as integers, strings, tuples,

            redis_client.set(cache_key, json.dumps(myResult), ex=600)
            return jsonify(myResult)
        else:
            print("--------------------------------------------------------------------------------")
            print(term, flush=True)
            print("Error course:", error, flush=True)
            print("--------------------------------------------------------------------------------")
            return jsonify({'error_course': error}), 404

    except Exception as e:
        print(str(e), flush=True)
        return jsonify({'error': str(e)}), 500

@app.route('/customization', methods=['POST'])
def customization():
    try:
        data = request.get_json()                                # This parses the JSON string into Python data structures (list)
        customizations_list = data['customizations']             # or data.get('customization', []) to get [] if no key found  

        # print("ff", customizations_list)
        # customized_class_list_ways = class_optimization.class_list_ways.copy()      # have to use this list at the first iteration
        customized_class_list_ways = list(data['class_list_ways']).copy()

        # impossible values
        # ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = -1, -1, -1, -1, -1

        for customization in customizations_list:
            weekDay = customization["weekDay"]                   # "M" 
            dayTime = customization["dayTime"]                   # "morning"
            customTime = customization["customTime"]             # '12:30 pm-01:20 pm'
            # print(weekDay)
            # print(dayTime)
            # print(customTime)
            customized_class_list_ways, ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = result.calculate_customization(customized_class_list_ways, weekDay, dayTime, customTime)

        # ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = result.calculate_customization(weekDay, dayTime, customTime)
        # print("fff", ways)
        # print("ffff", best_class_list)
        # print("There are " + customizedWays + " customized ways.")
        myCustomizationResult = {'customizedWays': ways, 'smallestCustomizedTimeGap': smallestTimeGap,'best_customized_class_list': best_class_list, 'startTime_list': startTime_list, 'endTime_list': endTime_list, 'customized_class_list_ways': customized_class_list_ways}
    
        return jsonify(myCustomizationResult)
    
    except Exception as e:
        print(str(e), flush=True)
        return jsonify({'error': str(e)}), 500

# this function is no longer needed
# @app.route('/loadSchedule', methods=['POST'])
# def loadSchedule():
#     try:
#         data = request.get_json()                                
#         # scheduleIndex = int(data['scheduleIndex'])

#         current_class_list = list(data['current_class_list'])

#         # class_list_ways = class_optimization.class_list_ways.copy()

#         # if scheduleIndex == len(class_list_ways):
#         #     scheduleIndex = 0
#         # elif scheduleIndex < 0:
#         #     scheduleIndex = len(class_list_ways) - 1

#         # current_class_list = class_list_ways[scheduleIndex]
#         startTime_list, endTime_list = class_optimization.startEndTimeList(current_class_list)
#         timeGap = class_optimization.timeGapCalculation(current_class_list)[0]
#         timeGap = format(timeGap, ".2f")

#         myScheduleResult = {'timeGap': timeGap, 'startTime_list': startTime_list, 'endTime_list': endTime_list}
#         return jsonify(myScheduleResult)

#     except Exception as e:
#         print(str(e), flush=True)
#         return jsonify({'error': str(e)}), 500

@app.route('/loadCustomizedSchedule', methods=['POST'])
def loadCustomizedSchedule():
    try:
        data = request.get_json()                                

        current_class_list = list(data['current_class_list'])

        startTime_list, endTime_list = class_optimization.startEndTimeList(current_class_list)
        timeGap = class_optimization.timeGapCalculation(current_class_list)[0]
        timeGap = format(timeGap, ".2f")

        myScheduleResult = {'timeGap': timeGap, 'startTime_list': startTime_list, 'endTime_list': endTime_list}
        return jsonify(myScheduleResult)

    except Exception as e:
        print(str(e), flush=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

#  [{'MATH1240A06': ['11:30 am-12:20 pm', 'MWF']}, {'MATH1240B12': ['04:00 pm-04:50 pm', 'T']}, 
# {'COMP1010A01': ['12:30 pm-01:20 pm', 'MWF']}]