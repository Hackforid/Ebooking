var orderAnalyseApp = angular.module('orderAnalyseApp', ['myApp.service']);


orderAnalyseApp.config(['$httpProvider', function($httpProvider) {

    if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};
        // $httpProvider.defaults.headers.post = {};    

    }

    $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
}]);



var ChartInit = function(scope, http, log) {
    this.scope = scope;
    this.http = http;
    var log = log;

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
                    $("#tablink1").click(function() {
                        easytabs('1', '1');
                    });
                    $("#tablink2").click(function() {
                        easytabs('1', '2');
                    });
                    $("#tablink3").click(function() {
                        easytabs('1', '3');
                    });
                }
            }
        );
    }

    this.init = function() {
        var allOtaNames = ["全部", "去哪儿", "淘宝旅行", "美团", "携程", "艺龙", "", "", "", "百达屋", ""];
        var initCurrentAllWays;
        if (scope.currentOtaWay == 1) {
            initCurrentAllWays = "1-6-7-8-11-12";
        } else if (scope.currentOtaWay == 4) {
            initCurrentAllWays = "4-10";
        } else {
            initCurrentAllWays = scope.currentOtaWay;
        }
        var url = "/ebooking/orderStat/night/" + scope.dateRange + "/" + initCurrentAllWays + "/start" + scope.startTime + "/end" + scope.endTime;
        log.log(url);
        http.get(url)
            .success(function(resp) {
                log.log(resp);
                if (resp.errcode == 0) {
                    var orderCounts = resp.result.dayOrders.length;
                    var dataRanges = resp.result.dataRanges;
                    var dayOrders = resp.result.dayOrders;
                    var startTime = dataRanges[0];
                    var endTime = dataRanges[(dataRanges.length - 1)];
                    scope.startTime = startTime;
                    scope.endTime = endTime;
                    scope.currentCounts = resp.result.orderCounts;
                    var monthCounts = (dataRanges.length - 1) / 30;
                    var tickCount;
                    var xaxisNumber = [];
                    var yaxisNumber = [];
                    var yaxisValue = [];
                    xaxisNumber = dataRanges;
                    yaxisValue = dayOrders;
                    for (var i = 0; i < xaxisNumber.length; i++) {
                        var axisDate = xaxisNumber[i].split("-");
                        xaxisNumber[i] = axisDate[1] + "." + axisDate[2];
                    };
                    scope.totalnightCounts = resp.result.dayNights;
                    scope.xAxisOrder = xaxisNumber;
                    scope.yAxisvalueOrder = yaxisValue;
                    /*饼图*/
                    var currentAllWays;
                    if (scope.currentOtaWay == 1) {
                        currentAllWays = "1-6-7-8-11-12";
                    } else if (scope.currentOtaWay == 4) {
                        currentAllWays = "4-10";
                    } else {
                        currentAllWays = scope.currentOtaWay;
                    }
                    var pieurl = "/ebooking/orderStat/source/" + scope.dateRange + "/" + currentAllWays + "/start" + scope.startTime + "/end" + scope.endTime;
                    log.log(pieurl);
                    http.get(pieurl)
                        .success(function(resp) {
                            log.log(resp);
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
                                    if (otaOrder[i].otaId == 6 || otaOrder[i].otaId == 7 || otaOrder[i].otaId == 8 || otaOrder[i].otaId == 11 || otaOrder[i].otaId == 12) {
                                        otaOrder[i].otaId = 1;
                                    } else if (otaOrder[i].otaId == 10) {
                                        otaOrder[i].otaId = 4;
                                    }
                                    if ((otaOrder[i].otaId != 0) && (orderWaystrue[otaOrder[i].otaId] != undefined)) {
                                        if (zeroTotalOtaOrderObj[otaOrder[i].otaId] != null && zeroTotalOtaOrderObj[otaOrder[i].otaId] != undefined) {
                                            for (var u = 0; u < otaNameValue.length; u++) {
                                                if (otaNameValue[u]['name'] == allOtaNames[otaOrder[i].otaId]) {
                                                    otaNameValue[u]['value'] = parseInt(otaNameValue[u]['value']) + parseInt(otaOrder[i]["orderCounts"]);
                                                }
                                            };
                                            zeroTotalOtaOrderObj[otaOrder[i].otaId]["orderCounts"] = parseInt(zeroTotalOtaOrderObj[otaOrder[i].otaId]["orderCounts"]) + parseInt(otaOrder[i].orderCounts);
                                            zeroTotalOtaOrderObj[otaOrder[i].otaId]["nightCounts"] = parseInt(zeroTotalOtaOrderObj[otaOrder[i].otaId]["nightCounts"]) + parseInt(otaOrder[i].roomNights);
                                            for (var o = 0; o < otaOrder[i].orders.length; o++) {
                                                zeroTotalOtaOrderObj[otaOrder[i].otaId]["orders"].push(otaOrder[i].orders[o]);
                                            };
                                        } else {
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
                                            orderWaystrue[otaOrder[i].otaId] = "";
                                            zeroTotalOtaOrderObj[otaOrder[i].otaId] = totalOtaOrderObj;
                                        }
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
                                    scope.allSumShow = true;
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
                                    scope.allSumShow = false;
                                }
                                scope.totalOtaResult = zeroTotalOtaOrderObj;
                                scope.currrentOtaResult = scope.totalOtaResult;
                                log.log(scope.totalOtaResult);
                                log.log(scope.currrentOtaResult);
                                scope.otavalueOrder = otaNameValue;
                                scope.otaWays = otaWays;
                                $("#" + scope.contentId).css("display", "block");
                                scope.chartInit.realchartInit();
                            } else {
                                log.log(resp);
                                if (resp.errcode == 401) {
                                    $("#" + scope.timeId).hide();
                                    tablink();
                                }
                            }
                        })
                        .error(function() {
                            log.log('network error');
                        })
                } else {
                    log.log(resp);
                    if (resp.errcode == 401) {
                        $("#" + scope.timeId).hide();
                        tablink();
                    }
                }
            })
            .error(function() {
                log.log('network error');
            })
    }
};


orderAnalyseApp.controller('orderTab1AnalyseCtrl', ['$scope', '$http', 'log', function($scope, $http, log) {
    $scope.searchFlag = 0;
    $scope.contentId = "tabcontent1";
    $scope.xAxisOrder = [];
    //$scope.yAxisOrder = [];
    $scope.yAxisvalueOrder = [];
    $scope.otavalueOrder = [];
    $scope.otaWays = [];
    $scope.currentCounts = "";
    $scope.chartInit = new ChartInit($scope, $http, log);
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
    $scope.allSumShow = false;
    $scope.roomBedType = ['单床', '大床', '双床', '三床', '三床-1大2单', '榻榻米', '拼床', '水床', '榻榻米双床', '榻榻米单床', '圆床', '上下铺', '大床或双床'];

    $scope.checkPayType = function(payType) {
        if (payType == "0") {
            return "现付";
        } else if (payType == "1") {
            return "预付";
        }
    }

    $scope.checkBedType = function(bedType) {
        var currentBedType = $scope.roomBedType[parseInt(bedType)];
        if ($.trim(currentBedType) != "" && currentBedType != undefined && currentBedType != null) {
            return currentBedType;
        } else {
            return "";
        }
    }

    $scope.checkBreakFast = function(breakfast) {
        if ($.trim(breakfast) == "" || breakfast == undefined || breakfast == null) {
            return "";
        } else {
            var everyBreakFast = breakfast.split(",");
            var currentBreakFast = everyBreakFast[0];
            if (currentBreakFast == "0") {
                return "无早餐";
            } else if (currentBreakFast == "1") {
                return "一份早餐";
            } else if (currentBreakFast == "2") {
                return "两份早餐";
            } else if (currentBreakFast == "100") {
                return "按人头早餐";
            } else {
                return "";
            }
        }
    }

    $scope.checkEveryPrice = function(price) {
        if ($.trim(price) != "" && price != undefined) {
            var hotelEverydayPrice = price.split(",");
            for (var k = 0; k < hotelEverydayPrice.length; k++) {
                hotelEverydayPrice[k] = hotelEverydayPrice[k] / 100;
            };
            var everyPrice = hotelEverydayPrice.join(",");
            return everyPrice;
        }
    }

    $scope.getAllOrderCounts = function(order) {
        var sumCounts = 0;
        for (var i in order) {
            sumCounts = sumCounts + order[i]['orderCounts'];
        }
        return sumCounts;
    }

    $scope.getAllNightCounts = function(order) {
        var sumCounts = 0;
        for (var i in order) {
            sumCounts = sumCounts + order[i]['nightCounts'];
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

    $scope.getCancelStatus = function(m, n) {
        var cancel;
        if (m == "0") {
            cancel = "不可取消";
        } else if (m == "1") {
            cancel = "自由取消";
        } else if (m == "2") {
            cancel = "提前取消";
        }
        var punish;
        if (n == "0") {
            punish = "不扣任何费用";
        } else if (n == "1") {
            punish = "扣首晚房费";
        } else if (n == "2") {
            punish = "扣全额房费";
        } else if (n == "3") {
            punish = "扣定额";
        } else if (n == "4") {
            punish = "扣全额房费百分比";
        }
        var cancelResult = cancel + ",取消时" + punish;
        return cancelResult;
    }

    $scope.getCurrentOrder = function(order) {
        log.log(order);
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
        day.setMonth((b - 1), 1);
        day.setDate(c);
        var dayTime = day.getTime();
        return dayTime;

    }

    $scope.timeConvert = function(time) {

        var timeFormat = $scope.conchecktime(time);
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
        if ($.trim($scope.currentOtaWay) == "") {
            return;
        }
        $scope.chartInit.init();
    }



    function jurisdictioninit() {
        var jurisdictionurl = "/ebooking/orderStat/isAdminAuth";
        $http.get(jurisdictionurl)
            .success(function(resp) {
                log.log(resp);
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
                        $("#usenameId").html(realName);
                    } else {
                        $("#usenameId").html(resp.result.username);
                    }
                    $scope.chartInit.init();
                } else {
                    log.log(resp);
                    if (resp.errcode == 301) {
                        log.log("跳转登陆");
                        window.location.href = "/login/";
                    }
                }
            })
            .error(function() {
                log.log('network error');
            })
    }


    function checkTime(time) {
        var date = time.split("-");
        var day = new Date();
        day.setMonth((date[1] - 1), 1);
        day.setFullYear(date[0]);
        day.setDate(date[2]);
        var totaltime = day.getTime();
        return totaltime;
    }


    function dayCounts(start, end) {
        var startTotal = checkTime(start);
        var endTotal = checkTime(end);
        var realDayCounts = (endTotal - startTotal) / (1000 * 24 * 60 * 60);
        return parseInt(realDayCounts);
    }
    jurisdictioninit();
}]);



orderAnalyseApp.controller('orderTab2AnalyseCtrl', ['$scope', '$http', 'log', function($scope, $http, log) {
    $scope.searchFlag = 0;
    $scope.contentId = "tabcontent2";
    $scope.xAxisOrder = [];
    //$scope.yAxisOrder = [];
    $scope.yAxisvalueOrder = [];
    $scope.otavalueOrder = [];
    $scope.otaWays = [];
    $scope.currentCounts = "";
    $scope.chartInit = new ChartInit($scope, $http, log);
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
    $scope.allSumShow = false;
    $scope.roomBedType = ['单床', '大床', '双床', '三床', '三床-1大2单', '榻榻米', '拼床', '水床', '榻榻米双床', '榻榻米单床', '圆床', '上下铺', '大床或双床'];


    $scope.checkPayType = function(payType) {
        if (payType == "0") {
            return "现付";
        } else if (payType == "1") {
            return "预付";
        }
    }


    $scope.checkBedType = function(bedType) {
        var currentBedType = $scope.roomBedType[parseInt(bedType)];
        if ($.trim(currentBedType) != "" && currentBedType != undefined && currentBedType != null) {
            return currentBedType;
        } else {
            return "";
        }
    }

    $scope.checkBreakFast = function(breakfast) {
        if ($.trim(breakfast) == "" || breakfast == undefined || breakfast == null) {
            return "";
        } else {
            var everyBreakFast = breakfast.split(",");
            var currentBreakFast = everyBreakFast[0];
            if (currentBreakFast == "0") {
                return "无早餐";
            } else if (currentBreakFast == "1") {
                return "一份早餐";
            } else if (currentBreakFast == "2") {
                return "两份早餐";
            } else if (currentBreakFast == "100") {
                return "按人头早餐";
            } else {
                return "";
            }
        }
    }


    $scope.checkEveryPrice = function(price) {
        if ($.trim(price) != "" && price != undefined) {
            var hotelEverydayPrice = price.split(",");
            for (var k = 0; k < hotelEverydayPrice.length; k++) {
                hotelEverydayPrice[k] = hotelEverydayPrice[k] / 100;
            };
            var everyPrice = hotelEverydayPrice.join(",");
            return everyPrice;
        }
    }


    $scope.getAllOrderCounts = function(order) {
        var sumCounts = 0;
        for (var i in order) {
            sumCounts = sumCounts + order[i]['orderCounts'];
        }
        return sumCounts;
    }

    $scope.getAllNightCounts = function(order) {
        var sumCounts = 0;
        for (var i in order) {
            sumCounts = sumCounts + order[i]['nightCounts'];
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

    $scope.getCancelStatus = function(m, n) {
        var cancel;
        if (m == "0") {
            cancel = "不可取消";
        } else if (m == "1") {
            cancel = "自由取消";
        } else if (m == "2") {
            cancel = "提前取消";
        }
        var punish;
        if (n == "0") {
            punish = "不扣任何费用";
        } else if (n == "1") {
            punish = "扣首晚房费";
        } else if (n == "2") {
            punish = "扣全额房费";
        } else if (n == "3") {
            punish = "扣定额";
        } else if (n == "4") {
            punish = "扣全额房费百分比";
        }
        var cancelResult = cancel + ",取消时" + punish;
        return cancelResult;
    }


    $scope.getCurrentOrder = function(order) {
        log.log(order);
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
        day.setMonth((b - 1), 1);
        day.setDate(c);
        var dayTime = day.getTime();
        return dayTime;

    }

    $scope.timeConvert = function(time) {
        var timeFormat = $scope.conchecktime(time);
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
        $scope.searchFlag = 1;
        if ($.trim($scope.currentOtaWay) == "") {
            return;
        }
        $scope.chartInit.init();
    }



    function checkTime(time) {
        var date = time.split("-");
        var day = new Date();
        day.setMonth((date[1] - 1), 1);
        day.setFullYear(date[0]);
        day.setDate(date[2]);
        var totaltime = day.getTime();
        return totaltime;
    }


    function dayCounts(start, end) {
        var startTotal = checkTime(start);
        var endTotal = checkTime(end);
        var realDayCounts = (endTotal - startTotal) / (1000 * 24 * 60 * 60);
        return parseInt(realDayCounts);
    }
    $scope.chartInit.init();
}]);

orderAnalyseApp.controller('orderTab3AnalyseCtrl', ['$scope', '$http', 'log', function($scope, $http, log) {
    $scope.searchFlag = 0;
    $scope.contentId = "tabcontent3";
    $scope.xAxisOrder = [];
    //$scope.yAxisOrder = [];
    $scope.yAxisvalueOrder = [];
    $scope.otavalueOrder = [];
    $scope.otaWays = [];
    $scope.currentCounts = "";
    $scope.chartInit = new ChartInit($scope, $http, log);
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
    $scope.allSumShow = false;
    $('#time1').datepicker({
        format: "yyyy-mm-dd",
        language: "zh-CN",
        orientation: "top auto",
        autoclose: true,
        enableOnReadonly: true,
        showOnFocus: true
    });

    $('#time2').datepicker({
        format: "yyyy-mm-dd",
        language: "zh-CN",
        orientation: "top auto",
        autoclose: true,
        enableOnReadonly: true,
        showOnFocus: true
    });
    $scope.roomBedType = ['单床', '大床', '双床', '三床', '三床-1大2单', '榻榻米', '拼床', '水床', '榻榻米双床', '榻榻米单床', '圆床', '上下铺', '大床或双床'];
    $scope.checkPayType = function(payType) {
        if (payType == "0") {
            return "现付";
        } else if (payType == "1") {
            return "预付";
        }
    }
    $scope.checkBedType = function(bedType) {
        var currentBedType = $scope.roomBedType[parseInt(bedType)];
        if ($.trim(currentBedType) != "" && currentBedType != undefined && currentBedType != null) {
            return currentBedType;
        } else {
            return "";
        }
    }

    $scope.checkBreakFast = function(breakfast) {
        if ($.trim(breakfast) == "" || breakfast == undefined || breakfast == null) {
            return "";
        } else {
            var everyBreakFast = breakfast.split(",");
            var currentBreakFast = everyBreakFast[0];
            if (currentBreakFast == "0") {
                return "无早餐";
            } else if (currentBreakFast == "1") {
                return "一份早餐";
            } else if (currentBreakFast == "2") {
                return "两份早餐";
            } else if (currentBreakFast == "100") {
                return "按人头早餐";
            } else {
                return "";
            }
        }
    }


    $scope.checkEveryPrice = function(price) {
        if ($.trim(price) != "" && price != undefined) {
            var hotelEverydayPrice = price.split(",");
            for (var k = 0; k < hotelEverydayPrice.length; k++) {
                hotelEverydayPrice[k] = hotelEverydayPrice[k] / 100;
            };
            var everyPrice = hotelEverydayPrice.join(",");
            return everyPrice;
        }
    }


    $scope.getAllOrderCounts = function(order) {
        var sumCounts = 0;
        for (var i in order) {
            sumCounts = sumCounts + order[i]['orderCounts'];
        }
        return sumCounts;
    }

    $scope.getAllNightCounts = function(order) {
        var sumCounts = 0;
        for (var i in order) {
            sumCounts = sumCounts + order[i]['nightCounts'];
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


    $scope.getCancelStatus = function(m, n) {
        var cancel;
        if (m == "0") {
            cancel = "不可取消";
        } else if (m == "1") {
            cancel = "自由取消";
        } else if (m == "2") {
            cancel = "提前取消";
        }

        var punish;
        if (n == "0") {
            punish = "不扣任何费用";
        } else if (n == "1") {
            punish = "扣首晚房费";
        } else if (n == "2") {
            punish = "扣全额房费";
        } else if (n == "3") {
            punish = "扣定额";
        } else if (n == "4") {
            punish = "扣全额房费百分比";
        }
        var cancelResult = cancel + ",取消时" + punish;
        return cancelResult;
    }


    $scope.getCurrentOrder = function(order) {
        log.log(order);
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
        day.setMonth((b - 1), 1);
        day.setDate(c);
        var dayTime = day.getTime();
        return dayTime;
    }

    $scope.timeConvert = function(time) {
        var timeFormat = $scope.conchecktime(time);
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
        $("#tab3cometitle").show();
        $("#tab3ordertitle").show();
        $("#linethree").show();
        $("#piethree").show();
        $scope.chartInit.init();
    }

    $scope.resetorder = function() {
        $("#time1").val("").datepicker('update');
        $("#time2").val("").datepicker('update');
        $scope.currentOtaWay = "";
    }

}]);