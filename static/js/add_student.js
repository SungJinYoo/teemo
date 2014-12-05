/**
 * Created by sungjinyoo on 12/3/14.
 */

$(document).ready(function(){
    // event handler for form.submit
    $("#add_student_form").submit(function(event){
        event.preventDefault();

        $.post($(this).attr("action"),
            $(this).serialize()
        )
            .done(function(data) {
                toast_message(data.type, data.message);
            })
        ;
    });
});
