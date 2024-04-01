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
                    const indexedArray = array.map((value, index) => ({ value:value, index:index }));
                    indexedArray.sort((a, b) => a.value - b.value);
                    const sortedIndexes = indexedArray.map(item => item.index);
                    return sortedIndexes;
                }
                
                const startTime_sorted_indexes = sortedIndexes(response.startTime_list);
                const endTime_sorted_indexes = sortedIndexes(response.endTime_list);
                    
                $('.newTable').empty(); 
                let soonest_time = response.startTime_list[startTime_sorted_indexes[0]] | 0;
                let latest_time = response.endTime_list[endTime_sorted_indexes[endTime_sorted_indexes.length-1]] | 0;
                for (let j = soonest_time; j <= latest_time; j++) {
                    let first_column = `
                    <tr value = "${j}" class="noBorder">
                        <td style = "background-color: #f2f2f2;"></td>                
                        <td class = "M"></td>
                        <td class = "T"></td>
                        <td class = "W"></td>
                        <td class = "R"></td>
                        <td class = "F"></td>
                    </tr>
                    <tr value = "${j+0.25}" class="noBorder">
                        <td class="cell" style = "background-color: #f2f2f2;"><div class="hour"><strong>${j}:00</strong></div></td>
                        <td class = "M"></td>
                        <td class = "T"></td>
                        <td class = "W"></td>
                        <td class = "R"></td>
                        <td class = "F"></td>
                    </tr>
                    <tr value = "${j+0.5}" class="noBorder">
                        <td style = "background-color: #f2f2f2;"></td>
                        <td class = "M"></td>
                        <td class = "T"></td>
                        <td class = "W"></td>
                        <td class = "R"></td>
                        <td class = "F"></td>
                    </tr>
                    <tr value = "${j+0.75}" class="noBorder">
                        <td style="background-color: #f2f2f2; border-bottom: 1px solid #ddd;"></td>
                        <td class = "M" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "T" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "W" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "R" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "F" style="border-bottom: 1px solid #ddd;"></td>
                    </tr>`;

                    $('.newTable').append(first_column);
                }
                for (let j = 0; j < response.startTime_list.length; j++) {
                    let color_list = ["goldenrod","slateblue","firebrick","limegreen","mediumorchid","darkgoldenrod"];
                    let round_start_time = response.startTime_list[j] % 0.25 !== 0 ? response.startTime_list[j] - (response.startTime_list[j] % 0.25) : response.startTime_list[j];
                    let round_end_time = response.endTime_list[j] % 0.25 !==0 ? response.endTime_list[j] - (response.endTime_list[j] % 0.25) + 0.25 : response.endTime_list[j];
                    const _class = best_class_list[j];    
                    const className = Object.keys(_class)[0].slice(0, -3);                       // this object only has one key
                    const classSection = Object.keys(_class)[0].slice(-3);
                    const classTime = _class[Object.keys(_class)[0]][0];                    
                    const days = _class[Object.keys(_class)[0]][1];
                    let table = document.getElementsByClassName("newTable")[0];
                    let time = round_start_time;
                    while (time < round_end_time) {
                        time_string = time.toString();
                        let row = table.querySelector(`[value="${time_string}"]`);
                        console.log(row);
                        for (let i = 0; i < days.length; i++) {
                            let cell = row.querySelector(`.${days[i]}`);
                            if ((round_end_time + round_start_time - 0.25)/2 - time < 0.25 && (round_end_time + round_start_time - 0.25)/2 - time >= 0) {
                                cell.innerHTML = classSection; 
                                let above_row = table.querySelector(`[value="${(time-0.25).toString()}"]`);
                                let above_cell = above_row.querySelector(`.${days[i]}`);
                                above_cell.innerHTML = className;
                                let below_row = table.querySelector(`[value="${(time+0.25).toString()}"]`);
                                let below_cell = below_row.querySelector(`.${days[i]}`);
                                below_cell.innerHTML = classTime;
                            }                            
                            cell.classList.add(color_list[j]); 
                            if (time < round_end_time - 0.25) {cell.style.borderBottom= "none";}
                            if (time == round_end_time - 0.25 && round_end_time !== response.endTime_list[j]) {
                                let divHTML = `<div style="position: absolute; top: 0; left: 0; width: 100%; height: 33.33%; background-color: ${color_list[j]};"></div>`;
                                cell.style.position = "relative";
                                cell.innerHTML += divHTML;
                                cell.style.backgroundColor = "transparent";
                            }
                        }
                        time += 0.25;
                    }
                }
            },

            error: function(error) {
                console.error('Error:', error);
            }
        })
    })


    $('#done').click(function() {
        // Get the input value
        const weekDaySelect = $('#weekDay');
        const weekDay = weekDaySelect.val();
        const dayTimeSelect = $('#dayTime');
        const dayTime = dayTimeSelect.val();
        const customTimeInput = $('#customTime');
        const customTime = customTimeInput.val();

        // Make an AJAX request to the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/customization',
            type: 'POST',
            data: { weekDay: weekDay, dayTime : dayTime , customTime : customTime},

            success: function(response) {
                // {'customizedWays': ways, 'smallestCustomizedTimeGap': smallestTimeGap,'best_customized_class_list': best_class_list}
                console.log("There are ", response.customizedWays)
                const best_customized_class_list = response.best_customized_class_list;
                console.log('Backend customized response:', best_customized_class_list);
                const best_customized_class_list_str = JSON.stringify(best_customized_class_list);

                $("#customizedWays").html("There are: " + response.customizedWays + " customized ways.");
                $("#smallestCustomizedTimeGap").html("The smallest time gap is: " + response.smallestCustomizedTimeGap + " hour per week.");
                $("#best_customized_class_list").html("With this schedule: " + best_customized_class_list_str);

                // return indexes of values of an array by ascending order
                function sortedIndexes(array) {
                    const indexedArray = array.map((value, index) => ({ value:value, index:index }));
                    indexedArray.sort((a, b) => a.value - b.value);
                    const sortedIndexes = indexedArray.map(item => item.index);
                    return sortedIndexes;
                }
                
                const startTime_sorted_indexes = sortedIndexes(response.startTime_list);
                const endTime_sorted_indexes = sortedIndexes(response.endTime_list);

                $('.myCustomizedTable').empty(); 
                let soonest_time = response.startTime_list[startTime_sorted_indexes[0]] | 0;
                let latest_time = response.endTime_list[endTime_sorted_indexes[endTime_sorted_indexes.length-1]] | 0;
                for (let j = soonest_time; j <= latest_time; j++) {
                    let first_column = `
                    <tr value = "${j}" class="noBorder">
                        <td style = "background-color: #f2f2f2;"></td>                
                        <td class = "M"></td>
                        <td class = "T"></td>
                        <td class = "W"></td>
                        <td class = "R"></td>
                        <td class = "F"></td>
                    </tr>
                    <tr value = "${j+0.25}" class="noBorder">
                        <td class="cell" style = "background-color: #f2f2f2;"><div class="hour"><strong>${j}:00</strong></div></td>
                        <td class = "M"></td>
                        <td class = "T"></td>
                        <td class = "W"></td>
                        <td class = "R"></td>
                        <td class = "F"></td>
                    </tr>
                    <tr value = "${j+0.5}" class="noBorder">
                        <td style = "background-color: #f2f2f2;"></td>
                        <td class = "M"></td>
                        <td class = "T"></td>
                        <td class = "W"></td>
                        <td class = "R"></td>
                        <td class = "F"></td>
                    </tr>
                    <tr value = "${j+0.75}" class="noBorder">
                        <td style="background-color: #f2f2f2; border-bottom: 1px solid #ddd;"></td>
                        <td class = "M" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "T" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "W" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "R" style="border-bottom: 1px solid #ddd;"></td>
                        <td class = "F" style="border-bottom: 1px solid #ddd;"></td>
                    </tr>`;

                    $('.myCustomizedTable').append(first_column);
                }
                for (let j = 0; j < response.startTime_list.length; j++) {
                    let color_list = ["goldenrod","slateblue","firebrick","limegreen","mediumorchid","darkgoldenrod"];
                    let round_start_time = response.startTime_list[j] % 0.25 !== 0 ? response.startTime_list[j] - (response.startTime_list[j] % 0.25) : response.startTime_list[j];
                    let round_end_time = response.endTime_list[j] % 0.25 !==0 ? response.endTime_list[j] - (response.endTime_list[j] % 0.25) + 0.25 : response.endTime_list[j];
                    const _class = best_customized_class_list[j];
                    const className = Object.keys(_class)[0].slice(0, -3);                       // this object only has one key
                    const classSection = Object.keys(_class)[0].slice(-3);
                    const classTime = _class[Object.keys(_class)[0]][0];                    
                    const days = _class[Object.keys(_class)[0]][1];
                    let table = document.getElementsByClassName("myCustomizedTable")[0];
                    let time = round_start_time;
                    while (time < round_end_time) {
                        let time_string = time.toString();
                        let row = table.querySelector(`[value="${time_string}"]`);
                        console.log(row);
                        for (let i = 0; i < days.length; i++) {
                            let cell = row.querySelector(`.${days[i]}`);
                            if ((round_end_time + round_start_time - 0.25)/2 - time < 0.25 && (round_end_time + round_start_time - 0.25)/2 - time >= 0) {
                                cell.innerHTML = classSection; 
                                let above_row = table.querySelector(`[value="${(time-0.25).toString()}"]`);
                                let above_cell = above_row.querySelector(`.${days[i]}`);
                                above_cell.innerHTML = className;
                                let below_row = table.querySelector(`[value="${(time+0.25).toString()}"]`);
                                let below_cell = below_row.querySelector(`.${days[i]}`);
                                below_cell.innerHTML = classTime;
                            }
                            cell.classList.add(color_list[j]); 
                            if (time < round_end_time - 0.25) {cell.style.borderBottom= "none";}
                            if (time == round_end_time - 0.25 && round_end_time !== response.endTime_list[j]) {
                                let divHTML = `<div style="position: absolute; top: 0; left: 0; width: 100%; height: 33.33%; background-color: ${color_list[j]};"></div>`;
                                cell.style.position = "relative";
                                cell.innerHTML += divHTML;
                                cell.style.backgroundColor = "transparent";
                            }
                        }
                        time += 0.25;
                    }
                }
            },

            error: function(error) {
                console.error('Error:', error);   
            }
        })
    })

    $('#dayTime').change(function() {
        if ($(this).val() === 'customize') {
            $('.customTime').show();
        } else {
            $('.customTime').hide();
        }
    });
})
