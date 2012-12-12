//时间
var StockDate=function(options){
    this.invalidDate = ["20100614","20100615","20100616","20100922","20100923","20100924","20101001","20101004","20101005","20101006","20101007","20110103",'20110912'];
}

//初始化本函数的各项参数
StockDate.prototype.getDate=function(offset,date){
    if (!date){
        date=new Date();
    }else if(typeof date == "string"){ //处理含有offset和date参数的日期
        date = this.toDate(date);
    }
    if (offset){
        date.setTime(date.getTime() + offset*60*60*24*1000);
    }else if(date.getHours()<15){//如果没到下午3点，取昨天数据
        date.setTime(date.getTime() - 1*60*60*24*1000);
    }
    if(date.getDay() == 6){//如果是周六，取周五或下周一数据
        offset = offset >0 ? 2:-1;
    }else if(date.getDay()==0){//如果是周日，取周五或下周一数据
        offset = offset >0 ? 1:-2;
    }else{
        offset = 0;
    }
    if (offset && typeof offset == "number") date.setTime(date.getTime()+offset*60*60*24*1000);//has bug.not may 31
    var newDay=this.toString(date);//如果节假日放假，则取放假前数据
    for(var i=0 ;i<this.invalidDate.length;i++){
        if (newDay == this.invalidDate[i]) return this.getDate(-1,newDay);
    }
    return newDay;
}

//格式化日期成字符串
StockDate.prototype.toString=function(date){
    var year=date.getUTCFullYear().toString().substr(0,4);
    var month=(date.getMonth()+1).toString();
    if (month.length<2) month="0"+month;
    date=date.getDate().toString();
    if (date.length<2) date="0"+date;
    return year+month+date;
}

//格式化字符串成日期
StockDate.prototype.toDate=function(str){
    var date=new Date();
    var year = parseInt(str.substr(0,4),10);
    var month = parseInt(str.substr(4,2),10)-1;
    var day = parseInt(str.substr(6,2),10);
    date.setUTCFullYear(year);
    date.setMonth(month);
    date.setDate(day);
    return date;
}

/**
 * 显示数据的组件
 * 传入json地址，返回拼凑好的表格
 * @params options 组件的配置项
 * {
 *   "datadir":   数据的文件夹地址 
 * }
 *
 */
var viewport=function(options){
    //整个组件从服务器端获取的原始数据
    this.data=null;

    //初始化组件的各项参数
    this.datadir="./data/report/";
    this.target="#content";

    if (typeof options == "undefined")   options={};
    for (var i in options){
        this[i]=options[i];
    }   

    stockDate = new StockDate(options)
    for (var i in stockDate){
        this[i]=stockDate[i];
    }

    if(!this.date){
        this.date=this.getDate();
    }
    if(typeof options.autoShow=="undefined" || options.autoShow==true){
        this.show(options);
    }
    
    if(!this.dateInputElement){
        this.dateInputElement="#date";
    }
    this.bindEvents();
}

viewport.prototype.load = function(path,callback,options){
    var me=this;
    if (!options) options = {};
    var params = options.params || {};
    $.get(path,params,function(response){
        callback.call(me,response,options);
    },"json");
}

viewport.prototype.afterLoad = function(response,options){
    this.data=response;
    var ofmtData = this.formatData(response);
    var sHtml = this.buildHtml(ofmtData);
    if(!this.type){
        $(this.target).html(sHtml);
    }else if(this.type=="add"){
        var sRawContent=$(this.target).html();
        $(this.target).html(sRawContent+sHtml);
    }
}

viewport.prototype.show=function(options){
    if (typeof options == "undefined")   options={};
    this.date = options.date || this.date;
    var dataFileName=this.dataFileName || this.date+".json";
    this.API = this.datadir+dataFileName;
    this.changeDateText();
    this.load(this.API,this.afterLoad,options);
}

viewport.prototype.showPre=function(){
    if(typeof this.date!="undefined"){
        this.date=this.getDate(-1,this.date);
        this.show();
    }
}
viewport.prototype.showNext=function(){
    if(typeof this.date!="undefined"){
        this.date=this.getDate(1,this.date);
        this.show();
    }
}

/**
 *  按日期增加显示的内容 
 */

viewport.prototype.add=function(options){
    if(typeof options=="string"){
        var targetExp=options;
    }else if (typeof options=="object"){
        var targetExp=options.target;

    }else{
        return;
    }

    var target=$(targetExp);
    var sValue=target.val();
    this.show({"type":"add","date":sValue});

}

/**
 * 把股票排序
 */

viewport.prototype.sort=function(options){
    if(typeof options=="undefined") return null;
    if(!options.data){
        var data=options;
    }else{
        var data=options.data;
    }
    data.sort();
    return data;
}

viewport.prototype.formatData=function(options){
    /*
    var fmtData=[{
        "title":"sfafsa",
        "total":23,
        "content":"sadasfsfd"
    }];
    return fmtData;
     */
}

viewport.prototype.buildHtml=function(data){
    var html="";
    for (var i=0;i<data.length;i++){
        var row=data[i];
        console.log(row.title);
        if (typeof(row.title) !== "undefined"){
            var title=row.title;
            html+="<h3>"+title+"</h3>";
        }
        if(typeof(row.total) !== "undefined"){
            var total=row.total;
            if(total){
                html+="total:"+total;
            }
        }
        if(typeof(row.content) !== "undefined"){
            var content=row.content;
            html+="<div class='code_block'>"+content+"</div>";
        }
        for (var sub in row){
            if (sub !=="title" && sub !== "total" && sub!= "content"){
                html += row[sub];
            }
        }
    }
    return html;
}


/**
 * 改变日期文字
 */
viewport.prototype.changeDateText=function(options){
    var oDate=$("#date");
    if(oDate.length>0){
        oDate.val(this.date);
    }

}

/**
 * 手动输入日期，则显示输入日期的数据
 */
viewport.prototype.handleInputDate=function(e){
    var event=e||window.event;
    var target=event.target||event.srcElement;
    if(event.keyCode!=13){
        event.preventDefault();
        return;
    }
    this.show({"date":target.value});
}

/**
 * 绑定各种事件
 */

viewport.prototype.bindEvents=function(){
    var me=this;
    //输入日期改变显示数据的控件
    var dateEl=$(this.dateInputElement);
    if(dateEl.length>0){
        dateEl.keyup(function(e){
                me.handleInputDate(e);
                });
    }
    //绑定键盘快捷键
    $(document).keyup(function(event) {
        if (event.target.tagName=="HTML"){
            var keyCode=event.keyCode||event.which||event.charCode;
            switch (keyCode){
                case 37: //<- in mac
                    me.showPre.call(me);
                    break;
                case 38: // up in mac
                    break;
                case 39: //-> in mac
                    me.showNext.call(me);
                    break;
                case 40: // down in mac
                    break;
            }
        }
    });
}

viewport.prototype.getCodeUrl=function(code){
    var html="<a href='http://stockhtm.finance.qq.com/sstock/ggcx/";
        html+=code;
        html+=".shtml' target='_blank'>"+code+"</a>";
    return html;
}



