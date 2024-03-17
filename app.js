$(document).ready(function() {
    $('#submit').click(function() {

        // Get the input value
        const coursesInput = $('#courses');
        const courses = coursesInput.val();
        const termInput = $('#term');
        const term = termInput.val();

        // Make an AJAX request to the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/schedule',
            type: 'POST',
            // contentType: 'application/json',
            // data: JSON.stringify({ courses }),      // key is courses
            data: { courses: courses, term : term },

            success: function(response) {
                console.log('Backend response:', response.ways);
                console.log('Backend response:', response.smallestTimeGap);

                const best_class_list = response.best_class_list;
                console.log('Backend response:', best_class_list);

                const best_class_list_str = JSON.stringify(best_class_list)

                $("#ways").html("There are: " + response.ways + " ways.");
                $("#smallestTimeGap").html("The smallest time gap is: " + response.smallestTimeGap + " hour per week.");
                $("#best_class_list").html("With this schedule: " + best_class_list_str);

                // return indexes of values of an array by ascending order
                function sortedIndexes(array) {
                    const indexedArray = array.map((value, index) => ({ value, index }));
                    indexedArray.sort((a, b) => a.value - b.value);
                    const sortedIndexes = indexedArray.map(item => item.index);
                    return sortedIndexes;
                }
                
                const startTime_sorted_indexes = sortedIndexes(response.startTime_list);
                const endTime_sorted_indexes = sortedIndexes(response.endTime_list);

                

                // const secondClass = best_class_list[startTime_sorted_indexes[1]];
                // const key2 = Object.keys(secondClass)[0];
                // const time2 = secondClass[key2][0];
                const weekDays = ["M", "T", "W", "R", "F"];

                for (let i = 0; i < startTime_sorted_indexes.length; i++) {
                    const _class = best_class_list[startTime_sorted_indexes[i]];
                    const className = Object.keys(_class)[0];                       // this object only has one key
                    const time = _class[className][0];
                    const days = _class[className][1];
                    const day_list = [];

                    console.log("days" + days);

                    for (let j = 0; j < days.length; j++) {
                        for (let k = 0; k < weekDays.length; k++) {
                            if (days[j] == weekDays[k]) {
                                day_list.push(k);
                                break;
                            }
                        }
                    }
                    console.log("day_list" + day_list);

                    const fillRow = new Array(5).fill("");
                    for (let j = 0; j < day_list.length; j++) {
                        fillRow[day_list[j]] = className;
                    }

                    console.log("fillRow" + fillRow);

                    const rowContent = `
                    <tr>
                        <td>${time}</td>
                        <td>${fillRow[0]}</td>
                        <td>${fillRow[1]}</td>
                        <td>${fillRow[2]}</td>
                        <td>${fillRow[3]}</td>
                        <td>${fillRow[4]}</td>
                    </tr>`;

                    $('tbody').append(rowContent);          // .html if want to replace existing html
                }
                    

                // for (let i = 0; i < best_class_list.length; i++) {
                //     const _class = best_class_list[i];
                //     for (let key in _class) {
                //         if (_class.hasOwnProperty(key)) {
                //             console.log(key + ': ' + _class[key]);
                //         }
                //     
                // }
            },

            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});
