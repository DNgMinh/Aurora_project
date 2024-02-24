course1A = {"A01": ["12:30 pm-01:20 pm", "MWF"]}
course1B = {"B01": ["09:30 am-10:20 am", "W"], "B02": ["10:30 am-11:20 am", "W"], "B03": ["11:30 am-12:20 pm", "W"], 
            "B04": ["01:30 pm-02:20 pm", "W"], "B05": ["02:30 pm-03:20 pm", "W"]}
course2A = {"A01": ["02:30 pm-03:45 pm", "T"], "A02": ["02:30 pm-03:45 pm", "R"]}
course3A = {"A01": ["10:00 am-11:15 am", "TR"]}
course3B = {"B01": ["08:30 am-09:20 am", "T"], "B02": ["02:30 pm-03:20 pm", "W"], "B03": ["03:30 pm-04:20 pm", "W"], 
            "B04": ["02:30 pm-03:20 pm", "R"]}
course4A = {"A01": ["09:30 am-10:20 am", "MWF"]}
course4B = {"B001": ["02:30 pm-03:45 pm", "W"]} #, "B02": ["05:30 pm-06:45 pm", "F"]}   ###
course5A = {"A01": ["10:30 am-11:20 am", "MWF"]}
course5B = {"B01": ["08:30 am-09:20 am", "F"], "B02": ["12:30 pm-01:20 pm", "F"], "B03": ["02:30 pm-03:20 pm", "F"]}


def courseArangement(course):
    for i in range(7):
        return 0
    

# take in time and convert to numbers
def timeEncoder(time):
    # days = [i for i in time[1]]
    startTime = time[0:5]
    startPeriod = time[6:8]
    endTime = time[9:14]
    endPeriod = time[15:17]
    if startPeriod == "am":
        startTime = int(startTime[0:2]) + int(startTime[3:5])/60        # convert to number
    if startPeriod == "pm":
        startTime = 12 + int(startTime[0:2])%12 + int(startTime[3:5])/60
    if endPeriod == "am":
        endTime = int(endTime[0:2]) + int(endTime[3:5])/60
    if endPeriod == "pm":
        endTime = 12 + int(endTime[0:2])%12 + int(endTime[3:5])/60

    return (startTime, endTime)


def backtracking(k):
    for key, value in courses[k].items():
        if checkEligibility(value, k):
            class_list[k] = {key: value}
            if k == n - 1:
                class_list_ways.append(class_list.copy())           # if no copy() then it is a reference damn python
            else:
                backtracking(k+1)


# check eligibility for backtracking
def checkEligibility(value, k):
    if k == 0:
        return 1
    else:
        for i in range(k):
            temp_value = list(class_list[i].values())
            for day in value[1]:             
                if day in temp_value[0][1]:                         # python is just dumb to make dict.values() an object
                    if checkOverlap(value[0], temp_value[0][0]):
                        return 0             
    return 1

# check whether 2 times are overlap 
def checkOverlap(time1, time2):
    startTime1, endTime1 = timeEncoder(time1)
    startTime2, endTime2 = timeEncoder(time2)
    if (startTime1 <= startTime2 and startTime2 < endTime1) or (startTime2 <= startTime1 and startTime1 < endTime2):
        return 1
    return 0

# calculate time gap of each option
def timeGapCalculation(class_list):
    timeGap = 0
    for day in "MTWRF":
        startTime_list = []
        endTime_list = []
        for i in range(len(class_list)):
            for key, value in class_list[i].items():
                if day in value[1]:
                    startTime, endTime = timeEncoder(value[0])
                    startTime_list.append(startTime)
                    endTime_list.append(endTime)
        startTime_list.sort()
        endTime_list.sort()
        for j in range(1,len(startTime_list)):
            timeGap += startTime_list[j] - endTime_list[j-1]
                    
    return timeGap



# courses = [course1A, course1B, course2A, course3A, course3B, course4A, course4B, course5A, course5B]
# n = len(courses)
# class_list = [0]*n
# class_list_ways  = []

def main():
    global courses, n, class_list, class_list_ways
    courses = [course1A, course1B, course2A, course3A, course3B, course4A, course4B, course5A, course5B]
    n = len(courses)
    class_list = [0]*n
    class_list_ways  = []
    
    backtracking(0)
    print(len(class_list_ways))
    # print(class_list_ways[2])
    smallestTimeGap = 1000
    best_class_list = []
    for _class_list in class_list_ways:
        timeGap = timeGapCalculation(_class_list)
        if timeGap < smallestTimeGap:
            smallestTimeGap = timeGap
            best_class_list = _class_list
        print(timeGap)
    
    return (len(class_list_ways), "{:.2f}".format(smallestTimeGap), best_class_list)

main()

