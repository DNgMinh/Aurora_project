$(document).ready(function() {
    $('#submit').click(function() {
        $('#loading').show();
        $('#error').text('');
        $('#error2').text('');
        $("#scheduleInfo1").html('');
        $("#scheduleInfo2").html('');
        $("#ways").html("");
        $("#smallestTimeGap").html("");
        $("#best_class_list").html("");
        $("#customizedWays").html("");
        $("#smallestCustomizedTimeGap").html("");
        $("#best_customized_class_list").html("");
        $(".newTable").empty();
        $(".myCustomizedTable").empty();
        window.class_list_ways = [];
        window.customized_class_list_ways = [];
        currentScheduleIndex1 = 0;
        // Get the input value
        const coursesInput = $('#courses');
        const courses = coursesInput.val();
        const termInput = $('#term');
        const term = termInput.val();

        $.ajax({
            url: 'https://aurorascheduler.online/schedule',
            type: 'POST',
            data: { courses: courses, term : term },

            success: function(response) {
                class_list_ways = response.class_list_ways;

                console.log('Backend response:', response.ways);
                console.log('Backend response:', response.smallestTimeGap);

                const best_class_list = response.best_class_list;
                console.log('Backend response:', best_class_list);

                const best_class_list_str = JSON.stringify(best_class_list)

                $('#loading').hide();
                $("#scheduleInfo1").html('');

                $("#ways").html("There are: " + response.ways + " ways.");
                $("#smallestTimeGap").html("The best option (fewest class days and minimal time gaps between classes) has the time gap of: " + response.smallestTimeGap + " hours per week.");
                $("#best_class_list").html("With this schedule: " + best_class_list_str);

                drawScheduleTable("newTable", best_class_list, response.startTime_list, response.endTime_list)
            },

            error: function(error) {
                if (error.status == 404) {
                    let error_course = error.responseJSON.error_course
                    console.error('Error 404: Course not found: ', error_course);
                    $('#loading').hide();
                    $('#error').text(`No course ${error_course} can be found! Please check again!`);
                } else {
                    console.error('Error:', error);  
                    $('#loading').hide();                  
                    $('#error').text('Error! PLease check again!');
                }
            }
        })
    })

    function drawScheduleTable(tableClassName, class_list, startTime_list, endTime_list) {

        // return indexes of values of an array by ascending order
        function sortedIndexes(array) {
            const indexedArray = array.map((value, index) => ({ value:value, index:index }));
            indexedArray.sort((a, b) => a.value - b.value);
            const sortedIndexes = indexedArray.map(item => item.index);
            return sortedIndexes;
        }

        const startTime_sorted_indexes = sortedIndexes(startTime_list);
        const endTime_sorted_indexes = sortedIndexes(endTime_list);

        $(`.${tableClassName}`).empty(); 
        let soonest_time = startTime_list[startTime_sorted_indexes[0]] | 0;
        let latest_time = endTime_list[endTime_sorted_indexes[endTime_sorted_indexes.length-1]] | 0;
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

            $(`.${tableClassName}`).append(first_column);
        }
        for (let j = 0; j < startTime_list.length; j++) {
            let color_list = ["goldenrod","slateblue","firebrick","limegreen","mediumorchid","darksalmon","cornflowerblue","darkkhaki","darkslategray","darkgoldenrod"];
            let round_start_time = startTime_list[j] % 0.25 !== 0 ? startTime_list[j] - (startTime_list[j] % 0.25) : startTime_list[j];
            let round_end_time = endTime_list[j] % 0.25 !==0 ? endTime_list[j] - (endTime_list[j] % 0.25) + 0.25 : endTime_list[j];
            const _class = class_list[j];
            const className = Object.keys(_class)[0].slice(0, -3);                       // this object only has one key
            const classSection = Object.keys(_class)[0].slice(-3);
            const classTime = _class[Object.keys(_class)[0]][0];                    
            const days = _class[Object.keys(_class)[0]][1];
            let table = document.getElementsByClassName(`${tableClassName}`)[0];
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
                    if (time == round_end_time - 0.25 && round_end_time !== endTime_list[j]) {
                        let divHTML = `<div style="position: absolute; top: 0; left: 0; width: 100%; height: 33.33%; background-color: ${color_list[j]};"></div>`;
                        cell.style.position = "relative";
                        cell.innerHTML += divHTML;
                        cell.style.backgroundColor = "transparent";
                    }
                }
                time += 0.25;
            }
        }
    }
    
    var currentScheduleIndex1 = 0;

    function loadSchedule(index) {

        if (index == class_list_ways.length) {
            index = 0;
        }
        else if (index < 0) {
            index = class_list_ways.length - 1;
        }        

        currentScheduleIndex1 = index;
        const current_class_list = class_list_ways[index];

        $.ajax({
            url: 'https://aurorascheduler.online/loadSchedule',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ current_class_list: current_class_list }),

            success: function(response) {
                $("#scheduleInfo1").html("Schedule number " + (currentScheduleIndex1+1) + " with the time gap = " + response.timeGap + " hrs/week");
                drawScheduleTable("newTable", current_class_list, response.startTime_list, response.endTime_list);
            },

            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    $('#nextSchedule1').click(function() {
        currentScheduleIndex1++;
        loadSchedule(currentScheduleIndex1);
    })

    $('#prevSchedule1').click(function() {
        currentScheduleIndex1--;
        loadSchedule(currentScheduleIndex1);
    })

    $('#return1').click(function() {
        currentScheduleIndex1 = 0;
        loadSchedule(currentScheduleIndex1);
    })


    $('#done').click(function() {
        $('#loading2').show();
        $("#error2").html("");
        var customizations_list = [];
        currentScheduleIndex2 = 0;
        customized_class_list_ways = [];

        $("#scheduleInfo2").html('');

        $('.customization').each(function() {
            
            const weekDaySelect = $(this).find('.weekDay');
            const weekDay = weekDaySelect.val();
            const dayTimeSelect = $(this).find('.dayTime');
            const dayTime = dayTimeSelect.val();
            const customTimeInput = $(this).find('.customTime');
            const customTime = customTimeInput.val();

            customizations_list.push({
                weekDay: weekDay,
                dayTime: dayTime,
                customTime: customTime
            });
        });

        console.log(customizations_list[0]);
        
        $.ajax({
	    url: 'https://aurorascheduler.online/customization',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ customizations: customizations_list, class_list_ways: class_list_ways}),              
            // data: { weekDay: weekDay, dayTime : dayTime , customTime : customTime},

            success: function(response) {
                $('#loading2').hide();
                customized_class_list_ways = response.customized_class_list_ways;
                // {'customizedWays': ways, 'smallestCustomizedTimeGap': smallestTimeGap,'best_customized_class_list': best_class_list}
                console.log("There are ", response.customizedWays)
                const best_customized_class_list = response.best_customized_class_list;
                console.log('Backend customized response:', best_customized_class_list);
                const best_customized_class_list_str = JSON.stringify(best_customized_class_list);

                $("#customizedWays").html("There are: " + response.customizedWays + " customized ways.");
                $("#smallestCustomizedTimeGap").html("The best option (fewest class days and minimal time gaps between classes) has the time gap of: " + response.smallestCustomizedTimeGap + " hours per week.");
                $("#best_customized_class_list").html("With this schedule: " + best_customized_class_list_str);

                drawScheduleTable("myCustomizedTable", best_customized_class_list, response.startTime_list, response.endTime_list)
            },

            error: function(error) {
                $('#loading2').hide();                  
                $('#error2').text('Error! PLease check again!');
                $("#customizedWays").html("");
                $("#smallestCustomizedTimeGap").html("");
                $("#best_customized_class_list").html("");
                $(".myCustomizedTable").empty();
                console.error('Error:', error);   
            }
        })
    })

    var currentScheduleIndex2 = 0;

    function loadCustomizedSchedule(index) {

        if (index == customized_class_list_ways.length) {
            index = 0;
        }
        else if (index < 0) {
            index = customized_class_list_ways.length - 1;
        }        

        currentScheduleIndex2 = index;
        const current_class_list = customized_class_list_ways[index];

        $.ajax({
            url: 'https://aurorascheduler.online/loadCustomizedSchedule',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ current_class_list: current_class_list }),

            success: function(response) {       
                $("#scheduleInfo2").html("Schedule number " + (currentScheduleIndex2+1) + " with the time gap = " + response.timeGap + " hrs/week");
                drawScheduleTable("myCustomizedTable", current_class_list, response.startTime_list, response.endTime_list);
            },

            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    $('#nextSchedule2').click(function() {
        currentScheduleIndex2++;
        loadCustomizedSchedule(currentScheduleIndex2);
    })

    $('#prevSchedule2').click(function() {
        currentScheduleIndex2--;
        loadCustomizedSchedule(currentScheduleIndex2);
    })

    $('#return2').click(function() {
        currentScheduleIndex2 = 0;
        loadCustomizedSchedule(currentScheduleIndex2);
    })


    $('#addCustomization').click(function () {
        // let newCustomization = $('.customization').first().clone();
        let newCustomization = 
        `
        <div class="customization">
                <div>
                    <label for="weekDay">Select day that you want to customize time:</label>
                    <select name="weekDay" class="weekDay">
                        <option value="M">Monday</option>
                        <option value="T">Tuesday</option>
                        <option value="W">Wednesday</option>
                        <option value="R">Thursday</option>
                        <option value="F">Friday</option>
                    </select>
                </div>
                <div>
                    <label for="dayTime">Select time that you do not want to have class:</label>
                    <select name="dayTime" class="dayTime">
                        <option value="customize">Customize</option>
                        <option value="allday">All day</option>
                        <option value="morning">Morning (08:00 am-11:00 am)</option>
                        <option value="midday">Midday (11:00 am-01:00 pm)</option>
                        <option value="afternoon">Afternoon (01:00 pm-17:00 pm)</option>
                        <option value="evening">Evening (17:00 pm-22:00 pm)</option>           
                    </select>
                </div>
                <div class="customTime_div">
                    <label for="customTime">Enter time that you do not want to have class (format: '08:00 am-11:00 am'):</label>
                    <input type="text" name="customTime" class="customTime">
                </div>
                <br>
            </div>
        `
        $('#customizationForm').append(newCustomization);

    });

    $('#removeCustomization').click(function() {
        const numCustomizations = $('.customization').length;
        if (numCustomizations > 1) {
            $('.customization:last-child').remove();               
        }
    });

    // $('.dayTime').change(function() {
    //     if ($(this).val() === 'customize') {
    //         $('.customTime').show();
    //     } else {
    //         $('.customTime').hide();
    //     }
    // });
    $(document).on('change', '.dayTime', function() {
        if ($(this).val() === 'customize') {
            $(this).closest('.customization').find('.customTime_div').show();
        } else {
            $(this).closest('.customization').find('.customTime_div').hide();
        }
    });
    
})
