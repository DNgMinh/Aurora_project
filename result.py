import class_optimization
import schedule_retrieve

def calculate_result(term, courses_list):
    classes_list = schedule_retrieve.schedule_retrieve(term, courses_list)

    ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = class_optimization.main(classes_list)

    print(startTime_list)
    print(endTime_list)
    printResult = "There are: " + str(ways) + " ways.\n Smallest time gap is " + str(smallestTimeGap) + " \nwith schedule: \n" + str(best_class_list) 
    return ways, smallestTimeGap, best_class_list, printResult, startTime_list, endTime_list

def calculate_customization(weekDay, dayTime, customTime):
    ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = class_optimization.customization(weekDay, dayTime, customTime)
    return ways, smallestTimeGap, best_class_list, startTime_list, endTime_list
    