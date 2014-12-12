function inner_add_extra_info(extra_data_list){
	for(var i=0;i<extra_data_list.length;i++){
		var extra_data = extra_data_list[i];
		var course_data = extra_data.fields.course;
		var time_data_list = extra_data.fields.course_times;

		var top = null;
		var left = null;
		var width = 0;
		var height = 0;
		for(var j=0;j<time_data_list.length;j++){
			var time_data = time_data_list[j];
			var block = $("#{0}_{1}".format(time_data.fields.day, time_data.fields.period_index));

			if(j==0){
				top  = block.position().top;
				left = block.position().left;
				width= block.outerWidth();
			}
			height += block.outerHeight();
		}
		var extra_info = $("<div>").attr("data-pk", extra_data.pk).attr("data-category",extra_data.fields.category).addClass("extra_info attached_box opaque {0}".format(COLOR_SELECT[extra_data.fields.category])).css({
			top: top,
			left: left,
			width: width,
			height: height,
		});
		
		var ul_element = $("<ul>").attr("id","info_ul");
		ul_element.addClass("clear");
		var li_course_name = $("<li>").text(extra_data.fields.course.fields.name);
		var li_memo = $("<li>").addClass("extra_memo").text(extra_data.fields.memo);

		var edit_button = $("<button>").addClass("glyphicon glyphicon-pencil menu_button edit_button").click(function(){
			var extra_info = $(this).parent().parent();
			console.log(extra_info);
			var modal = $("#modify_modal");
			var pk = extra_info.attr("data-pk");
			var form = modal.find("#modify_extra_form");
			var li_memo = extra_info.find(".extra_memo");
			form.find("input[name=extra_pk]").val(pk);

			var category = extra_info.attr("data-category");
			// form.find("input[name=category]");
			form.find("input[value={0}]:radio".format(category)).attr("checked", true);
			form.find("textarea").text(li_memo.text());
			modal.modal();

			modal.find("#modify_extra_button").off("click");
            modal.find("#modify_extra_button").click(function(){
                if(!form.find("input[name=category]:checked").val()){
                    toast_message("warning", "일정 유형을 선택해주세요");
                    return false;
                }
                $.post(
                    form.attr("action"),
                    form.serialize()
                )
                    .done(function(json){
                        toast_message(json.type, json.message);
                        if(json.result){
                            // add_extra_info(ajax.data.extra_data, ajax.data.attendance_info_no);
                            extra_info.removeClass(COLOR_SELECT[category]);
                            extra_info.addClass(COLOR_SELECT[form.find("input:checked").val()]);
                            console.log(form.find("textarea").val());
                            li_memo.text(form.find("textarea").val());
                        }
                    })
                    .always(function(){
                        modal.modal("hide");
                    });
            });
		}).hide();
		var remove_button = $("<button>").addClass("glyphicon glyphicon-remove menu_button remove_button").click(function(){
			//TODO: remove DB
			var extra_info = $(this).parent().parent();
			var pk = extra_info.attr("data-pk");
			var form = $("#delete_extra_form");
			var confirm_value = confirm("일정을 취소하시겠습니까?");
			if(confirm_value){
				form.find("input[name=extra_pk]").val(pk);
				$.post(
					form.attr("action"),
					form.serialize()
				)
					.done(function(json){
						toast_message(json.type, json.message);
						if(json.result){
							extra_info.remove();
						}
					});
			}

		}).hide();

		var menu_button_wrapper = $("<div>").addClass("menu_button_wrapper");
		menu_button_wrapper.append([edit_button, remove_button]);
		extra_info.append(menu_button_wrapper);


		ul_element.append(li_course_name);
		ul_element.append(li_memo);
		extra_info.append(ul_element);

        extra_info.hover(function() {
            /* Stuff to do when the mouse enters the element */
            $(this).removeClass('opaque');
            $(this).addClass('top_layer');

            $(this).find("button").show();
        }, function() {
            /* Stuff to do when the mouse leaves the element */
            $(this).addClass('opaque');
            $(this).removeClass('top_layer');
            
            $(this).find("button").hide();
        });
		$("#extra_info_wrapper").append(extra_info);
	}
}

function add_extra_info(extra_data_list, attendance_info_no){
	inner_add_extra_info(extra_data_list);
	if(attendance_info_no != undefined){
		$(".attendance_info[data-no={0}]".format(attendance_info_no)).remove();	
	}
}
function remove_extra_info(){

}
function reload_extra_info(extra_data_list){
	// remove Current extra_info;
	$(".extra_info").each(function(index, element){
		$(this).remove();
	});
	// load extra_info;
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
}

function clear_extras(){
	var attendance_info_list = $(".attendance_info");
	attendance_info_list.each(function(index, element){
		$(element).remove();
	});
}