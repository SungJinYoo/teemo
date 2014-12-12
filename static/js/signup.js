/**
 * Created by sungjinyoo on 12/12/14.
 */

$(document).ready(function(){
    signup();
});

function signup(){
    function validate_userid(){
        var userid_success_message = "사용 가능한 학번입니다";
        var userid_error_message = "사용 불가능한 학번입니다";
        var userid_input = $("#userid");
        var validation_form = $("#userid_validation_form");

        $("input[name=userid]").each(function(index, element){
            $(element).val(userid_input.val());
        });

        $.post(
            validation_form.attr("action"),
            validation_form.serialize()
        )
            .done(function(json){
                toast_message(json.type, json.message);
                if(json.result){
                    userid_input.siblings("p").removeClass("bg-danger text-danger").addClass("bg-success text-success").text(userid_success_message);
                }
                else{
                    userid_input.siblings("p").removeClass("bg-success text-success").addClass("bg-danger text-danger").text(userid_error_message);
                }
            });
    }

    function validate_email(){
        var email_success_message = "사용 가능한 이메일입니다";
        var email_error_message = "사용 불가능한 이메일입니다";
        var email_input = $("#email");

        var validation_form = $("#email_validation_form");

        $("input[name=email]").each(function(index, element){
            $(element).val(email_input.val());
        });

        $.post(
            validation_form.attr("action"),
            validation_form.serialize()
        )
            .done(function(json){
                toast_message(json.type, json.message);
                if(json.result){
                    email_input.siblings("p").removeClass("bg-danger text-danger").addClass("bg-success text-success").text(email_success_message);
                }
                else{
                    email_input.siblings("p").removeClass("bg-success text-success").addClass("bg-danger text-danger").text(email_error_message);
                }
            });
    }

    function validate_password(){
        var password_success_message = "비밀번호가 일치합니다";
        var password_error_message = "비밀번호가 일치하지 않습니다";
        var password_input = $("#password");

        if(password_input.val() == $("#password_repeat").val()){
            password_input.siblings("p").removeClass("bg-danger text-danger").addClass("bg-success text-success").text(password_success_message);
        }
        else{
            password_input.siblings("p").removeClass("bg-success text-success").addClass("bg-danger text-danger").text(password_error_message);
        }
    }

    // add event handlers
    $("#userid").change(validate_userid);
    $("#email").change(validate_email);
    $(".password").each(function(index, element){
        $(element).change(validate_password);
    });

    $("button[type=submit]").submit(function(e){
        e.preventDefault();
    })
        .click(function(){
            // TODO: do validation of sign up data
            var form = $("#signup_form");
            form.submit();
        });


}