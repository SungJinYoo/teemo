/**
 * Created by sungjinyoo on 12/2/14.
 */

$(document).ready(function(){
    time_table();
});

function time_table(){
    var current_semester = 1;

    function initialize(){
        initialize_current_year();
        initialize_current_semester();
        initialize_current_week();
        initialize_event_handlers();
    }

    function initialize_current_year(){
        var year_span = $("span#year");
        var fetch_form_year_input = $("#fetch_time_table_form").find("#year_input");
        var attendance_form_year_input = $("#fetch_attendance_data_form").find("#year_input");

        var current_year = new Date().getFullYear();

        year_span.text(current_year);
        fetch_form_year_input.val(current_year);
        attendance_form_year_input.val(current_year);
    }

    function initialize_current_semester(){
        var fetch_form_semester_input = $("#semester");
        var attendance_form_semester_input = $("#semester_input");
        var current_month = new Date().getMonth();
        var semester = FIRST_SEMESTER; // default to 1학기
        if(0 <= current_month && current_month < 2) // 겨울학기 (1~2월)
            semester = 40;
        else if(2 <= current_month && current_month < 6) // 1학기 (3~6월)
            semester = FIRST_SEMESTER;
        else if(6 <= current_month && current_month < 8) // 여름학기 (7~8월)
            semester = 30;
        else if(8 <= current_month && current_month < 12)
            semester = SECOND_SEMESTER;

        fetch_form_semester_input.val(semester);
        attendance_form_semester_input.val(semester);
        current_semester = semester;
    }

    function initialize_current_week(){
        // finding week number, from 3/1, 9/1
        function find_current_week(today, start_date){
            var delta_time = today.getTime() - start_date.getTime();
            var delta_date = delta_time / 1000 / 60 / 60 / 24;
            return Math.floor(delta_date / 7) + 1; // calculate in weeks
        }

        var today = new Date();
        var week = 0;
        var start_date = new Date();
        if(current_semester == FIRST_SEMESTER){
            start_date = new Date(today.getFullYear(), 2, 1, 0, 0, 0, 0); // mar 1st
        }
        else if(current_semester == SECOND_SEMESTER){
            start_date = new Date(today.getFullYear(), 8, 1, 0, 0, 0, 0); // sep 1st
        }

        if(start_date.getDay() == 6) start_date.setDate(start_date.getDate() + 2); // saturday + 2 == monday
        if(start_date.getDay() == 0) start_date.setDate(start_date.getDate() + 1); // sunday + 1 == monday

        week = find_current_week(today, start_date);

        $("#fetch_time_table_form").find("#week_input").val(week).attr("data-value", week);
        $("#fetch_attendance_data_form").find("#week_input").val(week).attr("data-value", week);
    }

    function initialize_event_handlers(){
        function fetch_attendance_data(block_no, blocks){
            var form = $("#fetch_attendance_data_form");
            form.find("#block_no").val(block_no);

            var period_index_list = [];
            blocks.each(function(index, block){
                period_index_list.push($(block).attr("data-row"));
            });

            form.find("#block_data").val(JSON.stringify(
                {
                    day: $(blocks[0]).attr("data-day"),
                    period_index_list: period_index_list
                }
            ));
            $.post(form.attr("action"),
                form.serialize()
            )
                .done(function(json){
                    toast_message(json.type, json.message);
                    if(json.result){
                        attendance_data = json.data;
                        console.log(attendance_data);
                    }
                });
        }

        // event for time table cells
        var is_select_mode = false;
        var is_mouse_down = false;
        var column = null;
        var block_no = 0;
        var selected_block_no = null;
        var random_color_code = null;
        $("#time_table").find("td")
            .mousedown(function(){
                is_mouse_down = true;
                random_color_code = get_random_color_code();

                column = $(this).attr("data-col");
                is_select_mode = !$(this).hasClass("selected");

                if(is_select_mode){
                    $(this).addClass("selected").attr("data-block-no", block_no).css("background-color", random_color_code);
                }
                else{
                    $(this).removeClass("selected");
                    selected_block_no = $(this).attr("data-block-no");
                    $(this).removeAttr("data-block-no").css("background-color", "");
                }

                return false; // prevent text selection
            })
            .mouseover(function(){
                if(is_mouse_down && column == $(this).attr("data-col")){
                    if(is_select_mode){
                        $(this).addClass("selected").attr("data-block-no", block_no).css("background-color", random_color_code);
                    }
                    else{
                        $(this).removeClass("selected").removeAttr("data-block-no").css("background-color", "");
                    }
                }
            })
            .mouseup(function(){
                is_select_mode = false;
                is_mouse_down = false;
                column = null;

                if(selected_block_no){
                    var blocks = $("#time_table").find("td.selected[data-block-no={0}]".format(selected_block_no));
                    if(blocks.size() > 0){
                        fetch_attendance_data(selected_block_no, blocks);
                        selected_block_no = null;
                    }
                }
                else{
                    var blocks = $("#time_table").find("td.selected[data-block-no={0}]".format(block_no));
                    if(blocks.size() > 0){
                        fetch_attendance_data(block_no++, blocks);
                    }
                }
            });

        // event for week input
        $("#fetch_time_table_form").find("#week_input").change(function(){
            var week = $(this).val();
            if(!(0 < week && week < 17)){
                alert("1~16주차만이 입력가능합니다");
                $(this).val($(this).attr("data-value"));
                return;
            }
            $(this).attr("data-value", $(this).val());
            $("#fetch_attendance_data_form").find("#week_input").val($(this).val()).attr("data-value", $(this).val());
        });

        // event for util buttons
        $("#reset_button").click(function(){
            var blocks = $("#time_table").find("td.selected");
            blocks.each(function(index, block){
                $(block).removeAttr("data-block-no").removeClass("selected").css("background-color", "");
            });
        });

        $("#course_no").change(function(){
            var form = $("#fetch_time_table_form");

            var course_no_re = new RegExp("^\\d{5}$");
            var course_no_input = form.find("#course_no");

            if(!course_no_re.test(course_no_input.val())){
                toast_message("warning", "수업번호 형식에 맞지 않습니다");
                return;
            }

            $(".course_no").each(function(index, element){
                $(this).val(course_no_input.val());
            });

            $.post(
                form.attr('action'),
                form.serialize()
            )
                .done(function(json){
                    toast_message(json.type, json.message);

                    if(json.result){
                        var time_table_data = json.data;
                        for(var i = 0; i < time_table_data.length; i++){
                            var course_data = time_table_data[i];
                            var course_no = course_data.fields.course_no;
                            var course_name = course_data.fields.name;
                            var course_time_data = course_data.fields.course_times;
                            var color_code = get_random_color_code();

                            for(var j = 0; j < course_time_data.length; j++){
                                var course_time = course_time_data[j];
                                var block = $("#{0}_{1}".format(course_time.fields.day, course_time.fields.period_index));
                                var upper_block = $("#{0}_{1}".format(course_time.fields.day, parseInt(course_time.fields.period_index) - 1));

                                var upper_block_background_color = upper_block.css("background-color");
                                if(j == 0 || upper_block_background_color == "rgba(0, 0, 0, 0)"){
                                    block.text("{0}, {1}".format(course_no, course_name));
                                }
                                block.css("background-color", color_code);
                            }
                        }
                    }
                });
        });
    }

    initialize();
}