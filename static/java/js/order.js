var orderAnalyseApp = angular.module('orderAnalyseApp', []);


orderAnalyseApp.config(['$httpProvider', function($httpProvider) {

    if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};
        // $httpProvider.defaults.headers.post = {};    

    }

    $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
}]);



var ChartInit = function(scope, http) {
    this.scope = scope;
    this.http = http;



    function isEmptyObject(obj) {
        for (var n in obj) {
            return false;
        }
        return true;
    }



    function tablink() {
        var menucount = loadtabs.length;
        var a = 0;
        var b = 1;
        do {
            easytabs(b, loadtabs[a]);
            a++;
            b++;
        } while (b <= menucount);
        if (autochangemenu != 0) {
            start_autochange();
        }
    }


    this.realchartInit = function() {

        console.log("图标初始化");
        // 路径配置
        require.config({
            paths: {
                echarts: '/static/java/dist'
            }
        });

        require(
            [
                'echarts',
                'echarts/chart/line',
                'echarts/chart/pie'
            ],
            function(ec) {

                //console.log(ec);

                var myChart = ec.init(document.getElementById(scope.lineId));

                var option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'line',
                            lineStyle: {
                                color: '#999',
                                width: 2,
                                type: 'solid'
                            }
                        }
                    },
                    legend: {
                        data: ['订单量', '间夜量'],
                        orient: 'vertical',
                        x: 'right',
                        selectedMode: false

                    },
                    toolbox: {
                        show: false,
                        feature: {
                            mark: {
                                show: true
                            },
                            dataView: {
                                show: true,
                                readOnly: false
                            },
                            magicType: {
                                show: true,
                                type: ['line', 'bar', 'stack', 'tiled']
                            },
                            restore: {
                                show: true
                            },
                            saveAsImage: {
                                show: true
                            }
                        }
                    },
                    calculable: false,
                    xAxis: [{
                        type: 'category',
                        /* show:false,*/
                        boundaryGap: false,
                        data: scope.xAxisOrder,

                        axisLine: {
                            lineStyle: {
                                color: '#000000',
                                width: 1,
                                type: 'solid'
                            }
                        }

                    }],
                    yAxis: [{
                        axisLine: {
                            lineStyle: {
                                color: '#000000',
                                width: 1,
                                type: 'solid'
                            }
                        },

                        type: 'value'
                    }],

                    series: [{
                        name: '订单量',
                        type: 'line',
                        // stack: '订单量',
                        data: scope.yAxisvalueOrder
                    }, {
                        name: '间夜量',
                        type: 'line',
                        //stack: '间夜量',
                        data: scope.totalnightCounts
                    }]
                };
                myChart.setOption(option);


                if (scope.otavalueOrder.length != 0) {
                    $("#" + scope.pieId).show();
                    myChart = ec.init(document.getElementById(scope.pieId));

                    option = {

                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        legend: {
                            orient: 'vertical',
                            x: 'right',
                            data: scope.otaWays,
                            selectedMode: false
                        },
                        toolbox: {
                            show: false,
                            feature: {
                                mark: {
                                    show: true
                                },
                                dataView: {
                                    show: true,
                                    readOnly: false
                                },
                                magicType: {
                                    show: true,
                                    type: ['pie', 'funnel'],
                                    option: {
                                        funnel: {
                                            x: '25%',
                                            width: '50%',
                                            funnelAlign: 'left',
                                            max: 1548
                                        }
                                    }
                                },
                                restore: {
                                    show: true
                                },
                                saveAsImage: {
                                    show: true
                                }
                            }
                        },
                        calculable: false,
                        series: [{
                            name: '渠道来源',
                            type: 'pie',
                            radius: '55%',
                            center: ['50%', '60%'],
                            data: scope.otavalueOrder
                        }],


                        color: [
                            '#63B8FF', '#ff7f50', '#7FFF00', '#FFFF00', '#6495ed',
                            '#ff69b4', '#cd5c5c', '#ffa500',
                            '#1e90ff', '#ff6347', '#00fa9a', '#ffd700',
                            '#6b8e23', '#ff00ff', '#3cb371', '#b8860b', '#30e0e0'
                        ]


                    };
                    myChart.setOption(option);
                } else {
                    $("#" + scope.pieId).hide();
                }


                if (scope.pieId == "pietwo" && scope.searchFlag == 0) {
                    tablink();
                }



            }

        );
    }



    this.init = function() {
        console.log("数据初始化");

        // var allOtaNames = ["全部", "去哪儿(优品房源)", "淘宝旅行", "美团", "携程(预付)", "艺龙", "去哪儿(酒店联盟)", "去哪儿(快团)", "去哪儿(酒店直销)", "百达屋", "携程(团购)"];

        var allOtaNames = ["全部", "去哪儿", "淘宝旅行", "美团", "携程", "艺龙", "", "", "", "百达屋", ""];

        var initCurrentAllWays;

        if (scope.currentOtaWay == 1) {
            initCurrentAllWays = "1-6-7-8";

        } else if (scope.currentOtaWay == 4) {
            initCurrentAllWays = "4-10";

        } else {
            initCurrentAllWays = scope.currentOtaWay;

        }

        var url = "/ebooking/orderStat/night/" + scope.dateRange + "/" + initCurrentAllWays + "/start" + scope.startTime + "/end" + scope.endTime;

        console.log(url);
        // console.log(params);
        http.get(url)
            .success(function(resp) {
                console.log(resp);
                console.log("数据1初始化完成");


                /* var resp = {
            "errcode": 0,
            "errmsg": "",
            "result": {
                "merchantId": 1,
                "dataRanges": [
                    "2015-01-05",
                    "2015-01-06",
                    "2015-01-07",
                    "2015-01-08",
                    "2015-01-09",
                    "2015-01-10"
                ],
                "dayNights": [
                    0,
                    8,
                    3,
                    0,
                    0,
                    0
                ],
                "nightCounts": 6,
                "dayOrders": [
                    0,
                    5,
                    2,
                    0,
                    0,
                    0
                ],
                "orderCounts": 6,
                "otaDatas": [{
                    "otaId": 0,
                    "otaName": "去哪儿",
                    "roomNights": 11,
                    "orderCounts": 7
                }, {
                    "otaId": 1,
                    "otaName": "携程",
                    "roomNights": 11,
                    "orderCounts": 7
                }]
            }
        }
*/

                if (resp.errcode == 0) {

                    var orderCounts = resp.result.dayOrders.length;

                    var dataRanges = resp.result.dataRanges;

                    var dayOrders = resp.result.dayOrders;

                    //console.log(dayOrders);

                    var startTime = dataRanges[0];
                    var endTime = dataRanges[(dataRanges.length - 1)];
                    //console.log(endTime);

                    scope.startTime = startTime;
                    scope.endTime = endTime;
                    scope.currentCounts = resp.result.orderCounts;

                    /*dayCounts(startTime,endTime);*/

                    var monthCounts = (dataRanges.length - 1) / 30;

                    //var monthCounts=orderCounts/30;
                    var tickCount;
                    var xaxisNumber = [];
                    var yaxisNumber = [];
                    var yaxisValue = [];


                    /*if (monthCounts > 1) {
                        tickCount = Math.ceil(monthCounts);


                        for (var i = 0; i < dataRanges.length;) {
                            xaxisNumber.push(dataRanges[i]);
                            yaxisValue.push(dayOrders[i]);
                            i = i + 2;
                        };

                        //console.log(yaxisValue);

                    } else if (monthCounts < 1) {*/

                    xaxisNumber = dataRanges;
                    yaxisValue = dayOrders;

                    //}



                    for (var i = 0; i < xaxisNumber.length; i++) {
                        var axisDate = xaxisNumber[i].split("-");
                        xaxisNumber[i] = axisDate[1] + "." + axisDate[2];
                    };


                    /* for (var i = 0; i < 10; i++) {
                         if (orderCounts > (Math.pow(10, i)) && orderCounts < (Math.pow(10, (i + 1)))) {

                             var yOrderCount = 0;
                             var ytick = Math.pow(10, i);
                             yaxisNumber.push(yOrderCount);

                             for (var j = 0; j < 10; j++) {

                                 yOrderCount = parseInt(yOrderCount) + parseInt(ytick);

                                 yaxisNumber.push(yOrderCount);


                             };

                             break;


                         }
                     };*/

                    scope.totalnightCounts = resp.result.dayNights;
                    console.log(scope.totalnightCounts);
                    scope.xAxisOrder = xaxisNumber;
                    //scope.yAxisOrder = yaxisNumber;
                    scope.yAxisvalueOrder = yaxisValue;

                    //console.log(xaxisNumber);
                    // console.log(yaxisNumber);
                    //console.log(yaxisValue);


                    /*饼图*/

                    /* var otaOrder = resp.result.otaDatas;
                     var otaNameValue = [];
                     var otaObj;
                     var otaWays = [];

                     for (var i = 0; i < otaOrder.length; i++) {
                         //console.log(otaOrder[i]["otaId"]);
                         otaObj = {
                             value: parseInt(otaOrder[i]["orderCounts"]),
                             name: otaOrder[i]["otaName"]
                         };
                         otaNameValue.push(otaObj);
                         otaWays.push(otaOrder[i]["otaName"]);

                     };

                     scope.otavalueOrder = otaNameValue;
                     scope.otaWays = otaWays;
                     console.log(otaNameValue);*/

                    var currentAllWays;

                    if (scope.currentOtaWay == 1) {
                        currentAllWays = "1-6-7-8";

                    } else if (scope.currentOtaWay == 4) {
                        currentAllWays = "4-10";

                    } else {
                        currentAllWays = scope.currentOtaWay;

                    }


                    var pieurl = "/ebooking/orderStat/source/" + scope.dateRange + "/" + currentAllWays + "/start" + scope.startTime + "/end" + scope.endTime;

                    console.log(pieurl);
                    http.get(pieurl)
                        .success(function(resp) {
                            console.log(resp);
                            console.log("数据2初始化完成");

                            if (resp.errcode == 0) {

                                /*饼图*/
                                /*otaOrder数据*/

                                var zeroTotalOtaOrderObj = {};



                                var otaOrder = resp.result.otaDatas;
                                var otaNameValue = [];
                                var otaObj;
                                var otaWays = [];

                                var orderWaystrue = ["0", "1", "2", "3", "4", "5", "", "", "", "9"];

                                for (var i = 0; i < otaOrder.length; i++) {


                                    if (otaOrder[i].otaId == 6 || otaOrder[i].otaId == 7 || otaOrder[i].otaId == 8) {

                                        otaOrder[i].otaId = 1;

                                    } else if (otaOrder[i].otaId == 10) {

                                        otaOrder[i].otaId = 4;

                                    }



                                    if (otaOrder[i].otaId != 0) {
                                        //console.log(otaOrder[i]["otaId"]);
                                        otaObj = {
                                            value: parseInt(otaOrder[i]["orderCounts"]),
                                            name: allOtaNames[otaOrder[i].otaId]
                                        };
                                        otaNameValue.push(otaObj);
                                        otaWays.push(allOtaNames[otaOrder[i].otaId]);


                                        var totalOtaOrderObj = {
                                            "orderCounts": otaOrder[i].orderCounts,
                                            "nightCounts": otaOrder[i].roomNights,
                                            "orders": otaOrder[i].orders,
                                            "name": allOtaNames[otaOrder[i].otaId]

                                        };

                                        //console.log(totalOtaOrderObj);

                                        //orderWaystrue.splice(otaOrder[i].otaId, 1);

                                         orderWaystrue[otaOrder[i].otaId]="";

                                        zeroTotalOtaOrderObj[otaOrder[i].otaId] = totalOtaOrderObj;

                                    }

                                };

                                orderWaystrue.splice(0, 1);

                                if (scope.currentOtaWay == 0) {
                                    for (var i = 0; i < orderWaystrue.length; i++) {

                                        if ($.trim(orderWaystrue[i]) != "") {

                                            var totalOtaOrderObj = {
                                                "orderCounts": 0,
                                                "nightCounts": 0,
                                                "orders": [],
                                                "name": allOtaNames[orderWaystrue[i]]

                                            };


                                            zeroTotalOtaOrderObj[orderWaystrue[i]] = totalOtaOrderObj;
                                        }


                                    }
                                    scope.allSumShow=true;
                                } else {


                                    if (isEmptyObject(zeroTotalOtaOrderObj)) {

                                        var zeroObj = {

                                            "orderCounts": 0,
                                            "nightCounts": 0,
                                            "orders": [],
                                            "name": allOtaNames[scope.currentOtaWay]

                                        };


                                        zeroTotalOtaOrderObj[scope.currentOtaWay] = zeroObj;

                                    }

                                    scope.allSumShow=false;

                                }



                                scope.totalOtaResult = zeroTotalOtaOrderObj;

                                scope.currrentOtaResult = scope.totalOtaResult;

                                console.log(scope.totalOtaResult);


                                /*if (isEmptyObject(scope.currrentOtaResult)) {

                                    if (scope.currentOtaWay == 0) {

                                        for (var i = 1; i < allOtaNames.length; i++) {

                                            var zeroObj = {

                                                "orderCounts": 0,
                                                "nightCounts": 0,
                                                "orders": [],
                                                "name": allOtaNames[i]

                                            };


                                            scope.currrentOtaResult[i] = zeroObj;


                                        };

                                    } else {

                                        var zeroObj = {

                                            "orderCounts": 0,
                                            "nightCounts": 0,
                                            "orders": [],
                                            "name": allOtaNames[scope.currentOtaWay]

                                        };


                                        scope.currrentOtaResult[scope.currentOtaWay] = zeroObj;

                                    }



                                    console.log("空对象");

                                }*/



                                console.log(scope.currrentOtaResult);


                                scope.otavalueOrder = otaNameValue;
                                scope.otaWays = otaWays;
                                //console.log(otaNameValue);

                                $("#" + scope.contentId).css("display", "block");

                                scope.chartInit.realchartInit();

                            } else {

                                console.log(resp);

                                if (resp.errcode == 401) {

                                    $("#" + scope.timeId).hide();

                                    tablink();

                                }

                            }
                        })
                        .error(function() {
                            console.log('network error');
                        })



                } else {

                    console.log(resp);

                    if (resp.errcode == 401) {

                        $("#" + scope.timeId).hide();

                        tablink();

                    }



                }
            })
            .error(function() {
                console.log('network error');
            })



    }



};



orderAnalyseApp.controller('orderTab1AnalyseCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.searchFlag = 0;


    $scope.contentId = "tabcontent1";

    $scope.xAxisOrder = [];
    //$scope.yAxisOrder = [];
    $scope.yAxisvalueOrder = [];
    $scope.otavalueOrder = [];
    $scope.otaWays = [];

    $scope.currentCounts = "";

    $scope.chartInit = new ChartInit($scope, $http);


    $scope.lineId = "lineone";
    $scope.pieId = "pieone";

    $scope.startTime = "";
    $scope.endTime = "";

    $scope.dateRange = "0";

    $scope.timeId = "tab1time";


    $scope.currentOtaWay = 0;


    $scope.totalOtaResult = {};



    $scope.totalnightCounts = [];



    $scope.qorderDetail = false;
    $scope.currentOtaOrders;

    $scope.currrentOtaResult;

    $scope.currentOrder;
    $scope.currentOrderDetails = false;

    $scope.detailInfo;



    $scope.allSumShow=false;

    $scope.getAllOrderCounts=function(order){

        var sumCounts=0;
        for(var i in order){

            sumCounts=sumCounts+order[i]['orderCounts'];
            
        }

        return sumCounts;

    }

    $scope.getAllNightCounts=function(order){

        var sumCounts=0;
        for(var i in order){

            sumCounts=sumCounts+order[i]['nightCounts'];
            
        }

        return sumCounts;

    }

 


    $scope.resonStatusCheck = function(a, b) {

        if (a == "拒绝") {
            return b;
        } else {
            return "无";
        }


    }


    $scope.getCancelStatus = function(m) {

        if (m == "0") {
            return "不可取消";
        } else if (m == "1") {
            return "自由取消";
        } else if (m == "2") {
            return "提前取消";
        }

    }


    $scope.getCurrentOrder = function(order) {
        console.log(order);
        $scope.currentOrder = order;
        $scope.detailInfo = $scope.infoconvent($scope.currentOrder['customerInfo']);

        $scope.currentOrderDetails = true;
    }


    $scope.$watch('currentOtaWay', function(newValue, oldValue) {

        if (newValue == oldValue) {
            return;

        }

       

        $scope.searchCurrentOta();

    });



    $scope.conchecktime = function conchecktime(time) {
        time = parseInt(time);

        var datevalue = new Date(time);
        var realmonth = datevalue.getMonth() + 1;
        var realdate = datevalue.getDate();
        var realyear = datevalue.getFullYear();

        var realhours = datevalue.getHours();
        var realmin = datevalue.getMinutes();
        var realsec = datevalue.getSeconds();


        if (realmonth < 10) {
            realmonth = "0" + realmonth;
        }
        if (realdate < 10) {
            realdate = "0" + realdate;
        }
        if (realhours < 10) {
            realhours = "0" + realhours;
        }

        if (realmin < 10) {
            realmin = "0" + realmin;
        }

        if (realsec < 10) {
            realsec = "0" + realsec;
        }



        var finaldate = realyear + "-" + realmonth + "-" + realdate + " " + realhours + ":" + realmin + ":" + realsec;

        return finaldate;
    }



    $scope.orderDetail = function(k) {
        $scope.currentOtaOrders = $scope.totalOtaResult[k];
        $scope.qorderDetail = true;


    }

    $scope.DateDiff = function DateDiff(startDate, endDate) {

        var splitDate, startTime, endTime, iDays;
        splitDate = startDate.split("-");
        startTime = dateTimeChecker(splitDate[0], splitDate[1], splitDate[2]);
        splitDate = endDate.split("-");
        endTime = dateTimeChecker(splitDate[0], splitDate[1], splitDate[2]);
        iDays = parseInt(Math.abs(startTime - endTime) / 1000 / 60 / 60 / 24);

        var daysResult = "( " + iDays + "晚 )";
        return daysResult;
    }

    function dateTimeChecker(a, b, c) {
        var day = new Date();

        day.setFullYear(a);
        day.setMonth(b);
        day.setDate(c);

        var dayTime = day.getTime();
        return dayTime;

    }

    $scope.timeConvert = function(time) {

        var timeFormat = $scope.conchecktime(time);

        //console.log(timeFormat);        


        var creatTime = timeFormat.split(" ");
        return creatTime;

    }

    $scope.infoconvent = function(info) {
        console.log(info);

        var infoobj = {};

        try {

            infoobj = eval(info);

        } catch (e) {

            infoobj = [{
                "name": " "
            }];

        }

        return infoobj;

    }


    $scope.getConfirmType = function getConfirmType(v) {
        if (v == "2") {
            return "手动确认";
        } else if (v == "1") {
            return "自动确认";
        } else {
            return " ";
        }

    }


    $scope.checkStatus = function(status) {

        if (status == "100") {

            return "待确定";

        } else if (status == "300") {

            return "接受";

        } else if (status == "400") {

            return "拒绝";

        } else if (status == "500" || status == "600") {

            return "服务器取消";

        } else {
            return "";
        }

    }

    $scope.searchCurrentOta = function() {

        /* if ($scope.currentOtaWay == 0) {
             $scope.currrentOtaResult = $scope.totalOtaResult;
             return;
         }


         $scope.currrentOtaResult = $scope.totalOtaResult[$scope.currentOtaWay];*/


        if ($.trim($scope.currentOtaWay) == "") {
            console.log("返回");
            return;
        }



        $scope.chartInit.init();

    }



    function jurisdictioninit() {


        var jurisdictionurl = "/ebooking/orderStat/isAdminAuth";
        $http.get(jurisdictionurl)
            .success(function(resp) {
                console.log(resp);

                if (resp.errcode == 0) {

                    if (resp.result.isAdmin == "false") {
                        $("#manageMenu").hide();

                    }
                    if (resp.result.hasWillCoop == "false") {
                        $("#willcoophotel").hide();

                    }


                    var nameCheckValue = $.trim(resp.result.username);
                    var nameLength = nameCheckValue.replace(/[\u4e00-\u9fa5]/g, "aa").length;
                    if (nameLength > 6) {

                        var cordCount = 0;
                        var realName = "";
                        for (var i = 0; i < 6; i++) {
                            var singleCode = nameCheckValue.substring(i, i + 1);

                            if (/[\u4e00-\u9fa5]/.test(singleCode)) {

                                cordCount = cordCount + 2;
                                realName = realName + singleCode;
                                if (cordCount > 4) {
                                    break;
                                }

                            } else {
                                cordCount = cordCount + 1;
                                realName = realName + singleCode;
                                if (cordCount > 6) {
                                    break;
                                }

                            }

                        };
                        realName = realName + "...";

                        //console.log(realName);
                        $("#usenameId").html(realName);

                    } else {

                        $("#usenameId").html(resp.result.username);

                    }


                    $scope.chartInit.init();


                } else {
                    console.log(resp);

                    if (resp.errcode == 301) {
                        console.log("跳转登陆");

                        window.location.href = "/login/";

                    }

                }
            })
            .error(function() {
                console.log('network error');
            })


    }



    function checkTime(time) {

        var date = time.split("-");


        var day = new Date();
        day.setMonth((date[1] + 1));
        day.setFullYear(date[0]);
        day.setDate(date[2]);
        var totaltime = day.getTime();

        return totaltime;
    }


    function dayCounts(start, end) {

        var startTotal = checkTime(start);
        var endTotal = checkTime(end);

        var realDayCounts = (endTotal - startTotal) / (1000 * 24 * 60 * 60);
        /* console.log(realDayCounts);*/
        return parseInt(realDayCounts);

    }

    // $scope.chartInit.init();
    jurisdictioninit();



}]);



orderAnalyseApp.controller('orderTab2AnalyseCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.searchFlag = 0;

    $scope.contentId = "tabcontent2";

    $scope.xAxisOrder = [];
    //$scope.yAxisOrder = [];
    $scope.yAxisvalueOrder = [];
    $scope.otavalueOrder = [];
    $scope.otaWays = [];

    $scope.currentCounts = "";

    $scope.chartInit = new ChartInit($scope, $http);

    $scope.lineId = "linetwo";
    $scope.pieId = "pietwo";

    $scope.startTime = "";
    $scope.endTime = "";
    $scope.dateRange = "1";

    $scope.timeId = "tab2time";

    $scope.currentOtaWay = 0;



    $scope.totalOtaResult = {};

    $scope.qorderDetail = false;
    $scope.currentOtaOrders;

    $scope.currrentOtaResult;



    $scope.currentOrder;
    $scope.currentOrderDetails = false;

    $scope.detailInfo;


    $scope.allSumShow=false;

    $scope.getAllOrderCounts=function(order){

        var sumCounts=0;
        for(var i in order){

            sumCounts=sumCounts+order[i]['orderCounts'];
            
        }

        return sumCounts;

    }

    $scope.getAllNightCounts=function(order){

        var sumCounts=0;
        for(var i in order){

            sumCounts=sumCounts+order[i]['nightCounts'];
            
        }

        return sumCounts;

    }







    $scope.resonStatusCheck = function(a, b) {

        if (a == "拒绝") {
            return b;
        } else {
            return "无";
        }


    }


    $scope.getCancelStatus = function(m) {

        if (m == "0") {
            return "不可取消";
        } else if (m == "1") {
            return "自由取消";
        } else if (m == "2") {
            return "提前取消";
        }

    }


    $scope.getCurrentOrder = function(order) {
        console.log(order);
        $scope.currentOrder = order;
        $scope.detailInfo = $scope.infoconvent($scope.currentOrder['customerInfo']);

        $scope.currentOrderDetails = true;
    }



    $scope.$watch('currentOtaWay', function(newValue, oldValue) {

        if (newValue == oldValue) {
            return;

        }

        $scope.searchCurrentOta();

    });


    $scope.conchecktime = function conchecktime(time) {
        time = parseInt(time);

        var datevalue = new Date(time);
        var realmonth = datevalue.getMonth() + 1;
        var realdate = datevalue.getDate();
        var realyear = datevalue.getFullYear();

        var realhours = datevalue.getHours();
        var realmin = datevalue.getMinutes();
        var realsec = datevalue.getSeconds();


        if (realmonth < 10) {
            realmonth = "0" + realmonth;
        }
        if (realdate < 10) {
            realdate = "0" + realdate;
        }
        if (realhours < 10) {
            realhours = "0" + realhours;
        }

        if (realmin < 10) {
            realmin = "0" + realmin;
        }

        if (realsec < 10) {
            realsec = "0" + realsec;
        }



        var finaldate = realyear + "-" + realmonth + "-" + realdate + " " + realhours + ":" + realmin + ":" + realsec;

        return finaldate;
    }



    $scope.orderDetail = function(k) {
        $scope.currentOtaOrders = $scope.totalOtaResult[k];
        $scope.qorderDetail = true;


    }

    $scope.DateDiff = function DateDiff(startDate, endDate) {

        var splitDate, startTime, endTime, iDays;
        splitDate = startDate.split("-");
        startTime = dateTimeChecker(splitDate[0], splitDate[1], splitDate[2]);
        splitDate = endDate.split("-");
        endTime = dateTimeChecker(splitDate[0], splitDate[1], splitDate[2]);
        iDays = parseInt(Math.abs(startTime - endTime) / 1000 / 60 / 60 / 24);

        var daysResult = "( " + iDays + "晚 )";
        return daysResult;
    }

    function dateTimeChecker(a, b, c) {
        var day = new Date();

        day.setFullYear(a);
        day.setMonth(b);
        day.setDate(c);

        var dayTime = day.getTime();
        return dayTime;

    }

    $scope.timeConvert = function(time) {

        var timeFormat = $scope.conchecktime(time);

        //console.log(timeFormat);        


        var creatTime = timeFormat.split(" ");
        return creatTime;

    }

    $scope.infoconvent = function(info) {

        var infoobj = {};

        try {

            infoobj = eval(info);

        } catch (e) {

            infoobj = [{
                "name": " "
            }];

        }

        return infoobj;

    }


    $scope.getConfirmType = function getConfirmType(v) {
        if (v == "2") {
            return "手动确认";
        } else if (v == "1") {
            return "自动确认";
        } else {
            return " ";
        }

    }


    $scope.checkStatus = function(status) {

        if (status == "100") {

            return "待确定";

        } else if (status == "300") {

            return "接受";

        } else if (status == "400") {

            return "拒绝";

        } else if (status == "500" || status == "600") {

            return "服务器取消";

        } else {
            return "";
        }

    }

    $scope.searchCurrentOta = function() {

        /* if ($scope.currentOtaWay == 0) {
             $scope.currrentOtaResult = $scope.totalOtaResult;
             return;
         }


         $scope.currrentOtaResult = $scope.totalOtaResult[$scope.currentOtaWay];*/
        $scope.searchFlag = 1;

        if ($.trim($scope.currentOtaWay) == "") {
            console.log("返回");
            return;
        }

        $scope.chartInit.init();

    }



    function checkTime(time) {

        var date = time.split("-");


        var day = new Date();
        day.setMonth((date[1] + 1));
        day.setFullYear(date[0]);
        day.setDate(date[2]);
        var totaltime = day.getTime();

        return totaltime;
    }


    function dayCounts(start, end) {

        var startTotal = checkTime(start);
        var endTotal = checkTime(end);

        var realDayCounts = (endTotal - startTotal) / (1000 * 24 * 60 * 60);
        /* console.log(realDayCounts);*/
        return parseInt(realDayCounts);

    }

    $scope.chartInit.init();
    // $scope.chartInit.chartInit();



}]);



orderAnalyseApp.controller('orderTab3AnalyseCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.searchFlag = 0;

    $scope.contentId = "tabcontent3";

    $scope.xAxisOrder = [];
    //$scope.yAxisOrder = [];
    $scope.yAxisvalueOrder = [];
    $scope.otavalueOrder = [];
    $scope.otaWays = [];
    $scope.currentCounts = "";

    $scope.chartInit = new ChartInit($scope, $http);

    $scope.lineId = "linethree";
    $scope.pieId = "piethree";
    $scope.startTime = "";
    $scope.endTime = "";
    $scope.dateRange = "2";

    $scope.timeId = "tab3time";



    $scope.currentOtaWay = "";


    $scope.totalOtaResult = {};

    $scope.qorderDetail = false;
    $scope.currentOtaOrders;

    $scope.currrentOtaResult;



    $scope.currentOrder;
    $scope.currentOrderDetails = false;

    $scope.detailInfo;


    $scope.allSumShow=false;

    $scope.getAllOrderCounts=function(order){

        var sumCounts=0;
        for(var i in order){

            sumCounts=sumCounts+order[i]['orderCounts'];
            
        }

        return sumCounts;

    }

    $scope.getAllNightCounts=function(order){

        var sumCounts=0;
        for(var i in order){

            sumCounts=sumCounts+order[i]['nightCounts'];
            
        }

        return sumCounts;

    }



    $scope.resonStatusCheck = function(a, b) {

        if (a == "拒绝") {
            return b;
        } else {
            return "无";
        }


    }


    $scope.getCancelStatus = function(m) {

        if (m == "0") {
            return "不可取消";
        } else if (m == "1") {
            return "自由取消";
        } else if (m == "2") {
            return "提前取消";
        }

    }


    $scope.getCurrentOrder = function(order) {
        console.log(order);
        $scope.currentOrder = order;
        $scope.detailInfo = $scope.infoconvent($scope.currentOrder['customerInfo']);

        $scope.currentOrderDetails = true;
    }



    $scope.conchecktime = function conchecktime(time) {
        time = parseInt(time);

        var datevalue = new Date(time);
        var realmonth = datevalue.getMonth() + 1;
        var realdate = datevalue.getDate();
        var realyear = datevalue.getFullYear();

        var realhours = datevalue.getHours();
        var realmin = datevalue.getMinutes();
        var realsec = datevalue.getSeconds();


        if (realmonth < 10) {
            realmonth = "0" + realmonth;
        }
        if (realdate < 10) {
            realdate = "0" + realdate;
        }
        if (realhours < 10) {
            realhours = "0" + realhours;
        }

        if (realmin < 10) {
            realmin = "0" + realmin;
        }

        if (realsec < 10) {
            realsec = "0" + realsec;
        }



        var finaldate = realyear + "-" + realmonth + "-" + realdate + " " + realhours + ":" + realmin + ":" + realsec;

        return finaldate;
    }



    $scope.orderDetail = function(k) {
        $scope.currentOtaOrders = $scope.totalOtaResult[k];
        $scope.qorderDetail = true;


    }

    $scope.DateDiff = function DateDiff(startDate, endDate) {

        var splitDate, startTime, endTime, iDays;
        splitDate = startDate.split("-");
        startTime = dateTimeChecker(splitDate[0], splitDate[1], splitDate[2]);
        splitDate = endDate.split("-");
        endTime = dateTimeChecker(splitDate[0], splitDate[1], splitDate[2]);
        iDays = parseInt(Math.abs(startTime - endTime) / 1000 / 60 / 60 / 24);

        var daysResult = "( " + iDays + "晚 )";
        return daysResult;
    }

    function dateTimeChecker(a, b, c) {
        var day = new Date();

        day.setFullYear(a);
        day.setMonth(b);
        day.setDate(c);

        var dayTime = day.getTime();
        return dayTime;

    }

    $scope.timeConvert = function(time) {

        var timeFormat = $scope.conchecktime(time);

        //console.log(timeFormat);        


        var creatTime = timeFormat.split(" ");
        return creatTime;

    }

    $scope.infoconvent = function(info) {

        var infoobj = {};

        try {

            infoobj = eval(info);

        } catch (e) {

            infoobj = [{
                "name": " "
            }];

        }

        return infoobj;

    }


    $scope.getConfirmType = function getConfirmType(v) {
        if (v == "2") {
            return "手动确认";
        } else if (v == "1") {
            return "自动确认";
        } else {
            return " ";
        }

    }


    $scope.checkStatus = function(status) {

        if (status == "100") {

            return "待确定";

        } else if (status == "300") {

            return "接受";

        } else if (status == "400") {

            return "拒绝";

        } else if (status == "500" || status == "600") {

            return "服务器取消";

        } else {
            return "";
        }

    }

    $scope.searchCurrentOta = function() {

        if ($scope.currentOtaWay == 0) {
            $scope.currrentOtaResult = $scope.totalOtaResult;
            return;
        }


        $scope.currrentOtaResult = $scope.totalOtaResult[$scope.currentOtaWay];

    }



    $scope.searchorder = function() {

        $scope.startTime = $.trim($("#time1").val());
        $scope.endTime = $.trim($("#time2").val());



        if ($.trim($scope.currentOtaWay) == "" || $scope.startTime == null || $scope.endTime == null || $scope.startTime == "" || $scope.endTime == "" || ($scope.startTime > $scope.endTime)) {
            $("#tab3cometitle").hide();
            $("#tab3ordertitle").hide();
            $("#linethree").hide();
            $("#piethree").hide();
            $scope.currrentOtaResult = {};

            return;
        }



        //console.log($scope.startTime);
        //console.log($scope.endTime);

        $("#tab3cometitle").show();
        $("#tab3ordertitle").show();

        $("#linethree").show();
        $("#piethree").show();


        $scope.chartInit.init();
        //$scope.chartInit.chartInit();

    }

    $scope.resetorder = function() {
        $("#time1").val("");
        $("#time2").val("");
        $scope.currentOtaWay = "";

    }



}]);



/*{
  "errcode": 0,
  "errmsg": "",
  "result": {
    "merchantId": 1,
    "dataRanges": [
      "2015-01-26",
      "2015-01-27",
      "2015-01-28",
      "2015-01-29"
    ],
    "dayNights": [
      0,
      0,
      0,
      0
    ],
    "nightCounts": 0,
    "dayOrders": [
      0,
      0,
      0,
      0
    ],
    "orderCounts": 0
  }
}
15:56:43
*/