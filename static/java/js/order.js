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

                console.log(ec);

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
                        data: ['订单量'],
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
                        stack: '总量',
                        data: scope.yAxisvalueOrder
                    }]
                };
                myChart.setOption(option);


                if (scope.otavalueOrder.length != 0) {
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
                            name: '访问来源',
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
                }


                if (scope.pieId == "pietwo") {
                    tablink();
                }



            }

        );
    }


    this.testline = function(ec) {

        var myChart = ec.init(document.getElementById('line'));

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
                data: ['订单量'],
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
                axisLabel: {
                    /* formatter: function(value) {
                         console.log(value);
                         return "星期" + value;
                     }*/
                }

            }],
            yAxis: [{
                type: 'value'
            }],

            series: [{
                name: '订单量',
                type: 'line',
                stack: '总量',
                data: scope.yAxisvalueOrder
            }]
        };
        myChart.setOption(option);



    }

    this.testpie = function(ec) {

        var myChart = ec.init(document.getElementById('main'));

        var option = {

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
                name: '访问来源',
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

    }



    this.init = function() {
        console.log("数据初始化");



        var url = "/ebooking/orderStat/night/" + scope.dateRange + "/start" + scope.startTime + "/end" + scope.endTime;


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
                    console.log(endTime);

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


                    for (var i = 0; i < 10; i++) {
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
                    };


                    scope.xAxisOrder = xaxisNumber;
                    scope.yAxisOrder = yaxisNumber;
                    scope.yAxisvalueOrder = yaxisValue;

                    console.log(xaxisNumber);
                    console.log(yaxisNumber);
                    console.log(yaxisValue);


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


                    var pieurl = "/ebooking/orderStat/source/" + scope.dateRange + "/start" + scope.startTime + "/end" + scope.endTime;


                    http.get(pieurl)
                        .success(function(resp) {
                            console.log(resp);
                            console.log("数据2初始化完成");

                            if (resp.errcode == 0) {

                                /*饼图*/

                                var otaOrder = resp.result.otaDatas;
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
                                console.log(otaNameValue);

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

    $scope.xAxisOrder = [];
    $scope.yAxisOrder = [];
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

                    $("#usenameId").html(resp.result.username);
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

    $scope.xAxisOrder = [];
    $scope.yAxisOrder = [];
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

    $scope.xAxisOrder = [];
    $scope.yAxisOrder = [];
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



    $scope.searchorder = function() {

        $scope.startTime = $.trim($("#time1").val());
        $scope.endTime = $.trim($("#time2").val());



        if ($scope.startTime == null || $scope.endTime == null || $scope.startTime == "" || $scope.endTime == "" || ($scope.startTime > $scope.endTime)) {
            $("#tab3cometitle").hide();
            $("#tab3ordertitle").hide();
            $("#linethree").hide();
            $("#piethree").hide();


            return;
        }



        console.log($scope.startTime);
        console.log($scope.endTime);

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