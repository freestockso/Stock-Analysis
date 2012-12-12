//显示边栏

var toggleSidebar=function(e){
    var event=e||window.event;
    var target=event.target||event.srcElement;
    if($("#sidebar").css("display")=="none"){
        $("#sidebar").show();
    }else{
        $("#sidebar").hide();
    }

    $(target).toggleClass('selected');
}
//显示菜单块
var toggleBlock=function(e){


}

//array object enhance
Array.prototype.remove = function(from, to) {
    var rest = this.slice((to || from) + 1 || this.length);
    this.length = from < 0 ? this.length + from : from;
    return this.push.apply(this, rest);
};
