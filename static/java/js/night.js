var ratePlanApp = angular.module('ratePlanApp', []);

ratePlanApp.controller('ratePlanCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.xAxisNights = [];
    $scope.yAxisNights = [];
    $scope.yAxisvalueNights = [];
    $scope.otavalueNights = [];
    $scope.otaWays = [];



    function chartInit() {
        // 路径配置
        require.config({
            paths: {
                echarts: './dist'
            }
        });


        require(
            [
                'echarts',
                'echarts/chart/line',
                'echarts/chart/pie'
            ],
            function(ec) {

                testline(ec);
                testpie(ec);
            }

        );
    }


    function testline(ec) {

        var myChart = ec.init(document.getElementById('line'));

        var option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['间夜量'],
                orient: 'vertical',
                x: 'left',
                
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
            calculable: true,
            xAxis: [{
                type: 'category',
                /* show:false,*/
                boundaryGap: false,
                data: $scope.xAxisNights,
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
                name: '间夜量',
                type: 'line',
                stack: '总量',
                data: $scope.yAxisvalueNights
            }]
        };
        myChart.setOption(option);



    }

    function testpie(ec) {

        var myChart = ec.init(document.getElementById('main'));

        var option = {
            
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                data: $scope.otaWays
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
            calculable: true,
            series: [{
                name: '访问来源',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: $scope.otavalueNights
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


    function init() {

        /*var url = ;
        var params;

        params = {

        };

        console.log(params);
        http.put(url, params)
            .success(function(resp) {*/


        var resp = {
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
                    "roomNights": 19,
                    "orderCounts": 7
                }, {
                    "otaId": 1,
                    "otaName": "携程",
                    "roomNights": 12,
                    "orderCounts": 7
                }]
            }
        }


        if (resp.errcode == 0) {

            var nightCounts = resp.result.dayNights.length;

            var dataRanges = resp.result.dataRanges;

            var dayNights = resp.result.dayNights;

            //console.log(dayOrders);

            var startTime = dataRanges[1];
            var endTime = dataRanges[(dataRanges.length - 1)];

            /*dayCounts(startTime,endTime);*/

            var monthCounts = (dataRanges.length - 1) / 30;

            //var monthCounts=orderCounts/30;
            var tickCount;
            var xaxisNumber = [];
            var yaxisNumber = [];
            var yaxisValue = [];


            if (monthCounts > 1) {
                tickCount = Math.ceil(monthCounts);


                for (var i = 0; i < dataRanges.length;) {
                    xaxisNumber.push(dataRanges[i]);
                    yaxisValue.push(dayNights[i]);
                    i = i + 2;
                };

                //console.log(yaxisValue);

            } else if (monthCounts < 1) {

                xaxisNumber = dataRanges;
                yaxisValue = dayNights;

            }



            for (var i = 0; i < xaxisNumber.length; i++) {
                var axisDate = xaxisNumber[i].split("-");
                xaxisNumber[i] = axisDate[1] + "." + axisDate[2];
            };


            for (var i = 0; i < 10; i++) {
                if (nightCounts > (Math.pow(10, i)) && nightCounts < (Math.pow(10, (i + 1)))) {

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


            $scope.xAxisNights = xaxisNumber;
            $scope.yAxisNights = yaxisNumber;
            $scope.yAxisvalueNights = yaxisValue;

            console.log(xaxisNumber);
            console.log(yaxisNumber);
            console.log(yaxisValue);


            /*饼图*/

            var otaOrder = resp.result.otaDatas;
            var otaNameValue = [];
            var otaObj;
            var otaWays = [];

            for (var i = 0; i < otaOrder.length; i++) {
                //console.log(otaOrder[i]["otaId"]);
                otaObj = {
                    value: parseInt(otaOrder[i]["roomNights"]),
                    name: otaOrder[i]["otaName"]
                };
                otaNameValue.push(otaObj);
                otaWays.push(otaOrder[i]["otaName"]);

            };

            $scope.otavalueNights = otaNameValue;
            $scope.otaWays = otaWays;
            console.log(otaNameValue);



        } else {

            console.log(resp);

        }
        /* })
         .error(function() {
             console.log('network error');
         })*/



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

    init();
    chartInit();



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