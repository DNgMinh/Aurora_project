import class_optimization
import schedule_retrieve

def calculate_result(term, courses_list):
    classes_list = schedule_retrieve.schedule_retrieve(term, courses_list)

    ways, smallestTimeGap, best_class_list = class_optimization.main(classes_list)
    result = "There are:" + str(ways) + " ways.\n Smallest time gap is " + str(smallestTimeGap) + " \nwith schedule: \n" + str(best_class_list) 
    return result
