# dct = {"a":[1, 3], "b": [2, 4], "c": [3, 5]}
# for i in dct.values():
#     print(i)

# s = "300"
# print(int(s)/600)

# lst = [0]*3

# for i in range(3):
#     lst[i] = {i: [i+1, i+2]}

# print(lst)
# t = list(lst[1].values())
# print(t)
# print(t[0][1])

course1A = {"A01": ["12:30 pm-01:20 pm", "MWF"]}
course1B = {"B01": ["09:30 am-10:20 am", "W"], "B02": ["10:30 am-11:20 am", "W"], "B03": ["11:30 am-12:20 pm", "W"], 
            "B04": ["01:30 pm-02:20 pm", "W"], "B05": ["02:30 pm-03:20 pm", "W"]}
course2A = {"A01": ["02:30 pm-03:45 pm", "T"], "A02": ["02:30 pm-03:45 pm", "R"]}
course3A = {"A01": ["10:00 am-11:15 am", "TR"]}
course3B = {"B01": ["08:30 am-09:20 am", "T"], "B02": ["02:30 pm-03:20 pm", "W"], "B03": ["03:30 pm-04:20 pm", "W"], 
            "B04": ["02:30 pm-03:20 pm", "R"]}
course4A = {"A01": ["09:30 am-10:20 am", "MWF"]}
course4B = {"B01": ["02:30 pm-03:45 pm", "W"]}
course5A = {"A01": ["10:30 am-11:20 am", "MWF"]}
course5B = {"B01": ["08:30 am-09:20 am", "F"], "B02": ["12:30 pm-01:20 pm", "F"], "B03": ["02:30 pm-03:20 pm", "F"]}


# courses = [course1A, course1B, course2A, course3A, course3B, course4A, course4B, course5A, course5B]
# for key, value in courses[1].items():
#     print(key, value)

class_list = [{'A01': ['12:30 pm-01:20 pm', 'MWF']}, {'B03': ['11:30 am-12:20 pm', 'W']}, {'A01': ['02:30 pm-03:45 pm', 'T']}, 
              {'A01': ['10:00 am-11:15 am', 'TR']}, {'B04': ['02:30 pm-03:20 pm', 'R']}, {'A01': ['09:30 am-10:20 am', 'MWF']}, 
              {'B001': ['02:30 pm-03:45 pm', 'W']}, {'A01': ['10:30 am-11:20 am', 'MWF']}, {'B01': ['08:30 am-09:20 am', 'F']}]

# for i in range(len(class_list)):
#     for key, value in class_list[i].items():
#         print(key)
def doSmth():
    numbers = [[1, 2], 3, 4, 5]
    modifyList(numbers)
    print(numbers)
# numbers[0] = numbers[0].copy()
# print(numbers)

def modifyList(lst):
    lst[0] = 1

doSmth()

lst = [1, 2, 3]
lst = list(lst)
print(lst)

# doubled_numbers = map(lambda x: x * 2, numbers)
# print(doubled_numbers)
# print(list(doubled_numbers))

# def incrementor(x):
#         return x + 5
# a = incrementor
# print(a(5))

# test_lst = []
# test_lst.append(None)
# print(test_lst)

# import class_optimization

# print("T" in "MWF")
# print(class_optimization.checkOverlap("01:00 pm-17:00 pm", '01:30 pm-02:20 pm'))