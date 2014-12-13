/**
 * Created by sungjinyoo on 12/2/14.
 */

function toast_message(type, message){
    if(message == ""){
        return;
    }
    if(type == "success")
        toastr.success(message);
    else if(type == "warning")
        toastr.warning(message);
    else if(type == "info")
        toastr.info(message);
    else if(type == "error")
        toastr.error(message);
    else
        toastr.info(message);
}