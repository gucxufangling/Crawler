/*******
逻辑说明：使用phantomjs无界面浏览器作为操作平台，
破解对方针对js解析的反爬虫辨别.并且伪造多代理的假象，伪造xforword。可
以多写几个值用，号隔开，模拟多代理连跳
************************************/
var page = require('webpage').create(), //获取操作dom或web网页的对象，通过它可以打开网页、接收网页内容、request、response参数，其为最核心对
    system = require('system'), //获得系统操作对象，包括命令行参数、phantomjs系统设置等信息
    address;

address = system.args[1];
page.setting.resourceTimeout = 30000;
page.setting.XSSAuditingEnabled = true;

page.customHeaders = {
    "connection":"keep-alive",
    "Cache-Control":"max-age=0";
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "X-Forwarded-For": '12.13.223.173',//简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP,只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
};

page.open(address, function(){ //通过page对象打开address链接，并可以回调其声明的回调函数
    console.log(address);
    console.log('begin');
})

//加载页面完毕运行
page.onLoadFinished = function(status) { //当page.open的目标URL被真正打开后，会在调用open的回调函数前调用该函数，在此可以进行内部的翻页等操作
  console.log('Status: ' + status);
  console.log(page.content);
  phantom.exit();
};