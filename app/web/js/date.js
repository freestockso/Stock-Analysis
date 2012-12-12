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

