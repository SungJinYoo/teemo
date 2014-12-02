/**
 * Created by sungjinyoo on 12/2/14.
 */

String.prototype.format = function(){
    var s = this;
    for (var i = 0; i < arguments.length; i++){
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        s = s.replace(reg, arguments[i]);
    }

    return s;
};

function get_random_color_code(){
    var red = (Math.random() * 1000) % 256;
    var green = (Math.random() * 1000) % 256;
    var blue = (Math.random() * 1000) % 256;

    red = parseInt((red + 255 * 6) / 7).toString(16);
    green = parseInt((green + 255 * 6) / 7).toString(16);
    blue = parseInt((blue + 255 * 6) / 7).toString(16);

    return "#{0}{1}{2}".format(red, green, blue);
}