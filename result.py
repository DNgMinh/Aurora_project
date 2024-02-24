import class_optimization

def calculate_result(entered_courses):
    ways, smallestTimeGap, best_class_list = class_optimization.main()
    return (ways, smallestTimeGap, best_class_list)
