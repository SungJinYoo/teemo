/**
 * Created by sungjinyoo on 12/2/14.
 */

"use strict";

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
        var year_id = $("#year");
        var year_class = $(".year");
        var current_year = new Date().getFullYear();

        year_id.text(current_year);
        year_class.each(function(index, element){
            $(element).val(current_year);
        });
    }

    function initialize_current_semester(){
        var semester_id = $("#semester");
        var semester_class = $(".semester");
        var current_month = new Date().getMonth();

        var semester = FIRST_SEMESTER; // default to 1학기

        if(0 <= current_month && current_month < 2) { // 겨울학기 (1~2월)
            semester = WINTER_SEMESTER;
        }
        else if(2 <= current_month && current_month < 6) { // 1학기 (3~6월)
            semester = FIRST_SEMESTER;
        }
        else if(6 <= current_month && current_month < 8) { // 여름학기 (7~8월)
            semester = SUMMER_SEMESTER;
        }
        else if(8 <= current_month && current_month < 12) {
            semester = SECOND_SEMESTER;
        }

        if(semester===WINTER_SEMESTER){
            semester_id.text("겨울 계절");
        }
        else if(semester===FIRST_SEMESTER){
            semester_id.text("1");
        }
        else if(semester===SUMMER_SEMESTER){
            semester_id.text("여름 계절");
        }
        else if(semester===SECOND_SEMESTER){
            semester_id.text("2");
        }

        semester_class.each(function(index, element){
            $(element).val(semester);
        });

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

        if(start_date.getDay() == 6) { // saturday + 2 == monday
            start_date.setDate(start_date.getDate() + 2);
        }
        if(start_date.getDay() == 0) { // sunday + 1 == monday
            start_date.setDate(start_date.getDate() + 1);
        }

        week = find_current_week(today, start_date);
        $("#week").text(week).attr("data-value", week);
        var week_class = $(".week");
        week_class.each(function(index, element){
            $(element).val(week).attr("data-value", week);
        });
    }

    function initialize_event_handlers(){
        var attendance_info_no = 0;

        function append_attendance_info(blocks, attendance_data){
            var dismiss = attendance_data.dismiss_students;
            var total = attendance_data.total_students;
            var attend = total - dismiss;
            var attendance_rate = total == 0? 0 : attend / total;
            var left = 0;
            var top = 0;
            var width = 0;
            var height = 0;

            blocks.each(function(index, element){
                if(index == 0) {
                    var position = $(element).position();
                    left = position.left;
                    top = position.top;
                    width = $(element).outerWidth();
                }
                height += $(element).outerHeight();
            });

            var attendance_info = $("<div>").attr("data-no", attendance_info_no++).addClass("attendance_info attatched_box").css({
                top: top,
                left: left,
                width: width,
                height: height,
                "background-color": get_random_color_code()
            });

            // TODO: show some buttons when mouse overlaied
            attendance_info.append($("<button>").addClass("glyphicon glyphicon-plus menu_button add_button").click(function(){
                var modal = $("#add_extra_confirm_modal");
                modal.modal();

                var form = modal.find("#add_extra_form");
                form.find(".year").val(attendance_data.year);
                form.find(".semester").val(attendance_data.semester);
                form.find(".course_no").val(attendance_data.course_no);
                form.find(".week").val(attendance_data.week);
                form.find(".day").val($(blocks[0]).attr("data-day"));
                form.find(".start_time").val(TIME_TABLE_PERIODS[$(blocks[0]).attr("data-row")][0]);
                form.find(".end_time").val(TIME_TABLE_PERIODS[$(blocks[blocks.length - 1]).attr("data-row")][1]);
                form.find(".attendance_info_no").val(attendance_info.attr("data-no"));

                modal.find("#add_extra_button").off("click");
                modal.find("#add_extra_button").click(function(){
                    if(!form.find("input[name=category]:checked").val()){
                        toast_message("warning", "일정 유형을 선택해주세요");
                        return false;
                    }

                    $.post(
                        form.attr("action"),
                        form.serialize()
                    )
                        .done(function(ajax){
                            toast_message(ajax.type, ajax.message);
                            if(ajax.result){

                                // TODO: SPLIT INTO ANOTHER FUNCTION -- add_extra_info(extra_data_list, attendance_no=null)
                                var extra_data = ajax.data.extra_data[0];
                                // Call function with arg[1];
                                add_extra_info(extra_data_list,ajax.data.attendance_info_no);
                            }
                        })
                        .always(function(){
                            modal.modal("hide");
                        });
                });
            }));
            attendance_info.append($("<button>").addClass("glyphicon glyphicon-remove menu_button remove_button").click(function(){
                $(this).parent().remove();
            }));
            attendance_info.append($("<div>").addClass("clear-both"));
            attendance_info.append($("<pre>").append($("<p>").text("총 수강인원: {0}\n예상 참석인원: {1}\n참석예상률: {2}%".format(total, attend, attendance_rate * 100))));

            $("#attendance_info_wrapper").append(attendance_info);
        }

        function fetch_attendance_data(block_no, blocks){
            var form = $("#fetch_attendance_data_form");
            var period_index_list = [];

            form.find("#block_no").val(block_no);

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
                        append_attendance_info(blocks, json.data);
                    }
                })
                .always(function(){
                    blocks.each(function(index, element){
                        $(this).removeClass("selected").removeAttr("data-block-no").css("background-color", $(this).attr("data-background-color"));
                        $(this).attr("data-background-color", "");
                    });
                });
        }

        // event for time table cells
        var is_mouse_down = false;
        var column = null;
        var block_no = 0;
        var random_color_code = null;
        $("#time_table").find("td")
            .mousedown(function(){
                is_mouse_down = true;
                random_color_code = get_random_color_code();

                column = $(this).attr("data-col");

                $(this).addClass("selected").attr("data-background-color", $(this).css("background-color"))
                    .attr("data-block-no", block_no).css("background-color", random_color_code);
                return false; // prevent text selection
            })
            .mouseover(function(){
                if(is_mouse_down && column == $(this).attr("data-col")){
                    $(this).addClass("selected").attr("data-background-color", $(this).css("background-color"))
                        .attr("data-block-no", block_no).css("background-color", random_color_code);
                }
            })
            .mouseup(function(){
                is_mouse_down = false;
                column = null;

                var blocks = $("#time_table").find("td.selected[data-block-no={0}]".format(block_no));
                if(blocks.size() > 0){
                    fetch_attendance_data(block_no, blocks);
                }
                block_no++;
            });

        // event for util buttons
        $("#reset_button").click(function(){
            var blocks = $("#time_table").find("td.selected");
            blocks.each(function(index, block){
                $(block).removeAttr("data-block-no").removeClass("selected").css("background-color", "");
            });
        });

        $("#course_no_form").submit(function(e){
            e.preventDefault();
            return false;
        });

        $("#course_no").change(function(){
            var course_no_re = new RegExp("^\\d{5}$");
            var course_no_input = $(this);

            if(!course_no_re.test(course_no_input.val())){
                toast_message("warning", "수업번호 형식에 맞지 않습니다");
                return;
            }

            $(".course_no").each(function(index, element){
                $(this).val(course_no_input.val());
            });

            var fetch_time_table_form = $("#fetch_time_table_form");

            $.post(
                fetch_time_table_form.attr('action'),
                fetch_time_table_form.serialize()
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
                                var current_color = $("#empty").css("background-color", color_code).css("background-color");
                                var upper_block_background_color = upper_block.css("background-color");
                                if(j == 0 || upper_block_background_color == "rgba(0, 0, 0, 0)" || current_color != upper_block_background_color){
                                    block.text("{0}, {1}".format(course_no, course_name));
                                }
                                block.css("background-color", color_code);
                            }
                        }
                    }
                });

            var fetch_extras_form = $("#fetch_extras_form");

            $.post(
                fetch_extras_form.attr("action"),
                fetch_extras_form.serialize()
            )
                .done(function(json){
                    toast_message(json.type, json.message);

                    if(json.result){
                        var extra_data_list = json.data;
                        add_extra_info(extra_data_list);
                    }
                });
        });

        function clear_time_table(){

        }

        function clear_extras(){
            var attendance_info_list = $(".attendance_info");
            attendance_info_list.each(function(index, element){
                $(element).remove();
            });
        }

        function fetch_extras(){
            var form = $("#fetch_extras_form");

            $.post(
                form.attr("action"),
                form.serialize()
            )
                .done(function(ajax){
                    clear_extras();
                    toast_message(ajax.type, ajax.message);
                    if(ajax.result){
                        var extras_data = ajax.data;


                    }
                });
        }

        // CONTROLLER
        $("#prev_week").click(function() {
            var week_id = $("#week");
            var week_class = $(".week");
            var current_week = parseInt(week_class.val()) - 1;
            if (!(1 <= current_week && current_week <= 16)) {
                return  toast_message("error", "이전주는 없습니다");
            }

            $("#week").text(current_week);
            week_class.each(function (index, element) {
                $(element).val(current_week);
            });
        });

        $("#next_week").click(function(){
            var week_id = $("#week");
            var week_class = $(".week");
            var current_week = parseInt(week_class.val()) + 1;
            if( !(1<=current_week && current_week <=16)){
                return  toast_message("error","다음주는 없습니다");
            }
            $("#week").text(current_week);
            week_class.each(function(index, element){
                $(element).val(current_week);
            });
        });

        // About arrows
        $(".arrows").each(function(index, element){
            $(element).affix({
                offset: {
                    top: 0
                }
            });

            $(element).hover(function() {
                /* Stuff to do when the mouse enters the element */
                $(this).find("span").css("color","#969090");
            }, function() {
                /* Stuff to do when the mouse leaves the element */
                $(this).find("span").css("color","#333333");
            });
            $(element).mousedown(function(event) {
                /* Act on the event */
                $(this).find("span").css("color","#CA5E58");
            });
            $(element).mouseup(function(event) {
                /* Act on the event */
                $(this).find("span").css("color","#333333");
            });
        });
    }

    initialize();
}