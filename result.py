import class_optimization

def calculate_result(entered_courses):
    ways, smallestTimeGap, best_class_list = class_optimization.main()
    result = "There are:" + str(ways) + " ways.\n Smallest time gap is " + str(smallestTimeGap) + " \nwith schedule: \n" + str(best_class_list) 
    return result
