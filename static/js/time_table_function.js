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
		var extra_info = $("<div>").attr("data-pk", extra_data.fields.pk).addClass("extra_info attached_box opaque").css({
			top: top,
			left: left,
			width: width,
			height: height,
			"background-color": "#ccc"
		});
		extra_info.append($("<button>").addClass("glyphicon glyphicon-pencil menu_button edit_button").click(function() {
			// console.log("edit button pressed");

		}).hide());
		extra_info.append($("<button>").addClass("glyphicon glyphicon-remove menu_button remove_button").click(function(){
			// $(this).parent().remove();
			//TODO: remove DB
		}).hide());
        extra_info.hover(function() {
            /* Stuff to do when the mouse enters the element */
            $(this).removeClass('opaque');
            $(this).addClass('top_layer');

            $(this).children().show();
        }, function() {
            /* Stuff to do when the mouse leaves the element */
            $(this).addClass('opaque');
            $(this).removeClass('top_layer');
            
            $(this).children().hide();
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