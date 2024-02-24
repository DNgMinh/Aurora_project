# Aurora scheduler

This application will take in user input which are courses that they want to take in a semester. Then, by using data of course schedules scrapped from Aurora, it will recommend options for your registration (no overlapping class). It will also show the best option which has the smallest time gap between classes in a week. 

The algorithm used for solving overlapping is backtracking.

### Fronend

Include `index.html` and `app.js`

### Backend

1. `class_optimization.py`: options including the best option for class scheduling. The backtracking algorithm is `backtracking` method.
2. `schedule_retrieve.py`: scrapping Aurora webpage.
3. `result.py`: return result to send to frontend.
4. `app.py`: server.
5. `test.py`: ignore. Just a test file.
