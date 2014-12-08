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
        if(0 <= current_month && current_month < 2) // 겨울학기 (1~2월)
            semester = WINTER_SEMESTER;
        else if(2 <= current_month && current_month < 6) // 1학기 (3~6월)
            semester = FIRST_SEMESTER;
        else if(6 <= current_month && current_month < 8) // 여름학기 (7~8월)
            semester = SUMMER_SEMESTER;
        else if(8 <= current_month && current_month < 12)
            semester = SECOND_SEMESTER;

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
        })
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
        $("#week").text(week).attr("data-value", week);
        var week_class = $(".week");
        week_class.each(function(index, element){
            $(element).val(week).attr("data-value", week);
        });
    }

    function initialize_event_handlers(){
        function fetch_attendance_data(block_no, blocks){
            var form = $("#fetch_attendance_data_form");
            form.find("#block_no").val(block_no);

            var block_list = [];
            blocks.each(function(index, block){
                block_list.push({row: $(block).attr("data-row"), col: $(block).attr("data-col")});
            });

            form.find("#blocks").val(JSON.stringify({block_data: block_list}));
            $.post(form.attr("action"),
                form.serialize()
            );
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
        })

        // CONTROLLER
        $("#prev_week").click(function(){
            var week_id = $("#week");
            var week_class = $(".week");
            var current_week = parseInt(week_class.val())-1;
            if( !(1<=current_week && current_week <=16) ){
                return  toast_message("error","invalid week");
            }
            $("#week").text(current_week);
            week_class.each(function(index, element){
                $(element).val(current_week);
            })
        });

        $("#next_week").click(function(){
            var week_id = $("#week");
            var week_class = $(".week");
            var current_week = parseInt(week_class.val())+1;
            if( !(1<=current_week && current_week <=16)){
                return  toast_message("error","invalid week");
            }
            $("#week").text(current_week);
            week_class.each(function(index, element){
                $(element).val(current_week);
            })
        });
    }

    $(".arrows").each(function(index, element){
        $(element).affix({
            offset: {
                top: 0,
                // left: 300,
                bottom: function () {
                  return (this.bottom = $('.footer').outerHeight(true))
                }
            }
        })
    })
    initialize();
}