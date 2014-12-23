(function() {

	var hotelInventoryApp = angular.module('hotelInventoryApp', []);

	hotelInventoryApp.filter('orderObjectBy', function() {
		return function(input) {

			var kv = [];
			for (var k in input) {
				kv.push({
					k: k,
					v: input[k],
				});
			}
			kv.sort(function(a, b) {
				a = parseInt(a.k);
				b = parseInt(b.k);
				return a - b;
			});
			var array = [];
			for (var k in kv) {
				array.push(kv[k].v);
			}
			return array;
		}
	});



	$("#roomtype-list .action input").click(function() {
		$("#roomtype-list").fadeOut(500);
	});


	var HotelHeadDialog = function(scope, http) {
		this.scope = scope;
		this.http = http;
		this.name = '';
		this.mealType = 0;
		this.punishType = 0;
		this.errmsg = '';

		this.prefixName = "";
		this.remarkName = "";


		this.exampleDivIn=function(index){

			$("#exampleDiv-"+index).after("<span class='example' style='position:relative;'>示例：<b>170元</b></span>").show(0, function() {});

		}
		this.exampleDivLeave=function(index){

			$("#exampleDiv-"+index).next("span.example").hide(0, function() {
				$("#exampleDiv-"+index).next("span.example").remove();
			});

		}


		this.eachhide = function(index) {

			$("div.eachroom").eq(index).css("display", "none");

		}
		this.eachshow = function(index) {

			$("div.eachroom").eq(index).css("display", "block");
			//var tempmealsum = scope.roomrates[index].meal1.split("|", 1);
			//$("#roomheadmeal" + index).val(tempmealsum[0]);

		}

		this.save = function(index) {
			console.log(scope.cooped);

			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.cooped[index]["id"] + '/cooped/';


			var params = {
				"prefix_name": $("#prefixId-" + index).val(),
				"remark_name": $("#remarkId-" + index).val()
			}

			console.log(url);
			console.log(params);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("div.eachroom").eq(index).css("display", "none");

					} else {
						this.errmsg = resp.errmsg;
						console.log(errmsg);
					}
				})
				.error(function() {
					this.errmsg = '网络错误';
				})



		}


	}


	var ChangeNumDialog = function(scope, http) {
		this.scope = scope;
		this.http = http;
		this.name = '';
		this.mealType = 0;
		this.punishType = 0;
		this.errmsg = '';

		this.close = function() {

			$("#openDiv1").fadeOut(500);
		}

		this.addSave = function() {
			var time1 = $("#time1").val();
			var time2 = $("#time2").val();
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomId + '/inventory/';

			var params = {
				"start_date": time1,
				"end_date": time2,
				"change_num": parseInt($("#roomNumCount").val()),
				"price_type": parseInt(scope.currentPriceType)

			}

			console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$("#openDiv1").fadeOut(500);
						scope.roomNum = [];

						scope.cooped[scope.currentIndex].inventory = resp.result.inventories[0];

						scope.dateCheck(scope.monthvalue);

					} else {
						this.errmsg = resp.errmsg;
						console.log(errmsg);
					}
				})
				.error(function() {
					this.errmsg = '网络错误';
				})



		}
		this.minusSave = function() {
			var time1 = $("#time1").val();
			var time2 = $("#time2").val();
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomId + '/inventory/';

			/*var params = {
			"start_date":time1,
			"end_date":time2,
			"change_num":-5,
			"price_type":1

			}*/

			var params = {
				"start_date": time1,
				"end_date": time2,
				"change_num": -parseInt($("#roomNumCount").val()),
				"price_type": parseInt(scope.currentPriceType)

			}
			console.log(params);

			console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("#openDiv1").fadeOut(500);
						scope.roomNum = [];

						scope.cooped[scope.currentIndex].inventory = resp.result.inventories[0];

						scope.dateCheck(scope.monthvalue);

					} else {
						this.errmsg = resp.errmsg;
						console.log(errmsg);
					}
				})
				.error(function() {
					this.errmsg = '网络错误';
				})

		}


		this.zeroSave = function() {

			var tempNum = $("#" + scope.currentId).html();

			var time1 = $("#time1").val();
			var time2 = $("#time2").val();
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomId + '/inventory/';

			var params = {
				"start_date": time1,
				"end_date": time2,
				"change_num": -parseInt(tempNum),
				"price_type": parseInt(scope.currentPriceType)

			}
			console.log(params);

			console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("#openDiv1").fadeOut(500);
						scope.roomNum = [];

						scope.cooped[scope.currentIndex].inventory = resp.result.inventories[0];

						scope.dateCheck(scope.monthvalue);

					} else {
						this.errmsg = resp.errmsg;
						console.log(errmsg);
					}
				})
				.error(function() {
					this.errmsg = '网络错误';
				})



		}


	}



	hotelInventoryApp.controller('hotelInventoryCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.hotel = {};
		$scope.willCoop = [];
		$scope.cooped = [];
		$scope.selecableMonths = [1, 2, 3];
		$scope.monthvalue = 1;

		$scope.testone;
		$scope.months = {};
		$scope.roomNum = [];
		$scope.roomNumAuto = [];
		$scope.roomNumHand = [];
		$scope.dayWeekSum = [];
		$scope.changeNumDialog = new ChangeNumDialog($scope, $http);
		$scope.hotelHeadDialog = new HotelHeadDialog($scope, $http);
		$scope.currentRoomId;
		$scope.currentIndex;
		$scope.currentPriceType;
		$scope.currentId;
		$scope.desResult=false;
		/*$scope.prefixName;
		$scope.remarkName;
		

		$scope.test=function test (){
			console.log("111");
			console.log($scope.prefixName);
			console.log($scope.remarkName);
			console.log($scope.testone);

		}*/

		$scope.roomDescribe =function roomDescribe(index){


			$scope.desResult=true;



/*var roomDes="<div class='messageDiv' id='cool-roomtype' style=' '><div class='messageBlack'></div><div class='detail detail-roomtype'><div class='head'><h1>房型概述</h1></div>"+
 "<p id='closeDiv' class='close' ng-click='roomDescribeClose()'>X</p><div class='con'><div class='cm'> <table width='100%' border='0' cellspacing='0' cellpadding='0'>"+
  "<tr><td width='90'><strong>房型名称：</strong></td><td>豪华房</td> </tr><tr><td><strong>房间大小：</strong></td> <td>15-20平方米</td></tr><tr><td><strong>床型：</strong></td><td>大床、双床、三床、四床</td></tr>"+
  "<tr><td><strong>床尺寸：</strong></td><td>200cm*180cm</td></tr><tr><td><strong>楼层：</strong></td><td>1层</td></tr><tr><td><strong>入住人数：</strong></td><td>2人</td></tr><tr><td><strong>设施：</strong></td>"+
   "<td>wi-fi、宽带、有线电视、洗漱用品、24小时热水、空调</td></tr><tr><td><strong>描述：</strong></td><td>标准间……</td></tr></table></div></div>"+
   "</div> </div>";  

$("body").append(roomDes);  */

		}

		$scope.roomDescribeClose=function roomDescribeClose(){
			$scope.desResult=false;

		}


		$scope.changeNum = function changeNum(d, c, i, p, m) {

			console.log(p);

			if (c != "stop") {
				$scope.currentRoomId = i;
				$scope.currentIndex = p;
				$scope.currentPriceType = m;
				$scope.currentId = d;
				console.log($("#" + d).html());

				$("#" + d).after("<div class='div1'><input name='' type='button' value='修改房价' class='btn-number' /></div>").show(0, function() {
					$(".btn-number").click(function() {
						$("#openDiv1").show();
					});
				});
			}

			$("#" + d).mouseout(function() {

				$("#" + d).next("div").delay(1000).hide(0, function() {
					$("#" + d).next("div").remove();
				});

			});

		}



		// ------- 新增房型 ------------
		$scope.newRoomType = function() {
			for (var i = 0; i < $scope.willCoop.length; i++) {
				$scope.willCoop[i].isChecked = false;
			}
			$("#roomtype-list").fadeIn(500);

			console.log($scope.willCoop);
		}

		$scope.saveNewRoomType = function() {
			var shouldCooped = [];
			for (var i = 0; i < $scope.willCoop.length; i++) {
				if ($scope.willCoop[i].isChecked) {
					shouldCooped.push($scope.willCoop[i].id);
				}
			}

			var url = "/api/hotel/" + hotelId + "/roomtype/";
			console.log(url);
			$http.post(url, {
				'year':$scope.months[$scope.monthvalue-1].year,
				'month':$scope.months[$scope.monthvalue-1].month,
				'roomtype_ids': shouldCooped
				})
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						// Todo loading anime

						for (var i = 0; i < shouldCooped.length; i++) {

							//$scope.cooped.push(resp.result.cooped_roomtypes[i]);
							$scope.cooped.push($scope.cooped[0]);
						};

						console.log($scope.cooped);

						$scope.cooped[1].inventory = $scope.cooped[0].inventory;
						//$scope.cooped[5]=$scope.cooped[0];

						console.log($scope.cooped);


						$scope.dayWeekSum = [];
						$scope.dateCheck($scope.monthvalue);


					} else {
						console.log(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})
		}

		// -----------------------------



		function initMonthWatch() {

			console.log("watch");

			$scope.$watch('monthvalue', function() {
				if ($scope.monthvalue == undefined) {
					return;
				}
				$scope.roomNum = [];

				loadHotelMsg(hotelId);
			});
		}


		function loadHotelMsg(hotel_id) {
			var url = "/api/hotel/" + hotel_id + "/roomtype/?year=" + $scope.months[$scope.monthvalue-1].year+"&month="+$scope.months[$scope.monthvalue-1].month;   
			console.log(url);
			$http.get(url)
				.success(function(resp) {
					console.log(resp)
					if (resp.errcode == 0) {
						$scope.hotel = resp.result.hotel;
						$scope.willCoop = resp.result.will_coop_roomtypes;
						$scope.cooped = resp.result.cooped_roomtypes;


						$scope.cooped[1].inventory = $scope.cooped[0].inventory;


						$scope.dayWeekSum = [];
						$scope.dateCheck($scope.monthvalue);


					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})
		}

		function computeSelecableDate() {
			var date = new Date();
			var month0 = date.getMonth() + 1;
			var month1 = month0 + 1 > 12 ? 1 : month0 + 1;
			var month2 = month1 + 1 > 12 ? 1 : month1 + 1;

			$scope.selecableMonths = [{
				'm': 0,
				'name': month0 + '月'
			}, {
				'm': 1,
				'name': month1 + '月'
			}, {
				'm': 2,
				'name': month2 + '月'
			}];
			$scope.monthvalue = $scope.selecableMonths[0];
		}

		function init() {
			//computeSelecableDate();
			monthCheck();
			console.log("months");

			console.log($scope.months);

			initMonthWatch();
		}

		init();


		function monthCheck() {
			var day = new Date();
			var month = day.getMonth() + 1;
			var year = day.getFullYear();

			var ninetytime = day.getTime() + 1000 * 60 * 60 * 24 * 90;
			var ninetyday = new Date(ninetytime);
			var ninetymonth = ninetyday.getMonth() + 1;
			var monthcount = (ninetyday.getFullYear() - year) * 12 + (ninetyday.getMonth() + 1 - month) + 1;

			var temp = {};

			$scope.months[0] = {
				"month": month,
				"year": year
			};
			for (var i = 1; i < monthcount; i++) {
				month++;
				if (month > 12) {
					month = 1;
					year++;
				}
				temp = {
					"month": month,
					"year": year
				};
				$scope.months[i] = temp;
			}

		}



		$scope.dateCheck = function dateCheck(monthvalue) {

			if (typeof($scope.roomrates) === "object" && !($scope.roomrates instanceof Array)) {
				return;
			}

			var day = new Date();
			var year = $scope.months[monthvalue - 1].year;
			var month = $scope.months[monthvalue - 1].month;
			day.setFullYear(year);
			day.setMonth(month - 1);

			var ninetytime = new Date().getTime() + 1000 * 60 * 60 * 24 * 90;
			var ninetyday = new Date(ninetytime);
			var ninetyyear = ninetyday.getFullYear();
			var ninetymonth = ninetyday.getMonth() + 1;

			var ninetysum = new Date(ninetyyear, ninetymonth, 0).getDate();
			var daynum;var currentDay=day.getDate();


			if (monthvalue == 1) {
				daynum = day.getDate();
			} else if (monthvalue == 4) {
				daynum = ninetyday.getDate();

			} else {
				daynum = new Date(year, month, 0).getDate();
			}


			var weekDay = new Array("日", "一", "二", "三", "四", "五", "六");



			/*赋值部分*/
			$scope.roomNum = [];
			for (var i = 0; i < $scope.cooped.length; i++) {
				$scope.roomNum.push($scope.cooped[i].inventory);
			};
			//$scope.roomNum[1] = $scope.cooped[0].inventory;
			console.log($scope.roomNum);
			/*赋值部分*/


			var tempDayNum = new Date(year, month, 0).getDate();

			if (monthvalue == 1) {

				for (var i = 0; i < $scope.roomNum.length; i++) {
					var tempAuto = {};
					var tempHead = {};
					var id = $scope.cooped[i]["id"];



					for (var a = 0; a < daynum - 1; a++) {
						tempAuto[a] = {
							"autoNum": "--",
							"classStyle": "stop"
						};
						tempHead[a] = {
							"headNum": "--",
							"classStyle": "stop"
						};
					};


					for (var j = daynum - 1; j < tempDayNum; j++) {
						var temp = [];
						var classStyle;
						temp = $scope.roomNum[i]["day" + (j + 1)].split("|");
						if (temp[0] == "0") {
							classStyle = "action1 man-close"
						} else {
							classStyle = "action1"
						};

						tempAuto[j] = {
							"autoNum": temp[0],
							"classStyle": classStyle
						};
						if (temp[1] == "0") {
							classStyle = "action1 man-close"
						} else {
							classStyle = "action1"
						};

						tempHead[j] = {
							"headNum": temp[1],
							"classStyle": classStyle
						};
					};

					$scope.roomNumAuto[id] = tempAuto;
					$scope.roomNumHand[id] = tempHead;
				};

			} else if (monthvalue == 4) {

				for (var i = 0; i < $scope.roomNum.length; i++) {
					var tempAuto = {};
					var tempHead = {};
					var id = $scope.cooped[i]["id"];


					for (var o = daynum; o < ninetysum; o++) {
						tempAuto[o] = {
							"autoNum": "--",
							"classStyle": "stop"
						};
						tempHead[o] = {
							"headNum": "--",
							"classStyle": "stop"
						};
					};

					for (var j = 0; j < daynum; j++) {
						var temp = [];
						var classStyle;
						temp = $scope.roomNum[i]["day" + (j + 1)].split("|");
						if (temp[0] == "0") {
							classStyle = "action1 man-close"
						} else {
							classStyle = "action1"
						};

						tempAuto[j] = {
							"autoNum": temp[0],
							"classStyle": classStyle
						};


						if (temp[1] == "0") {
							classStyle = "action1 man-close"
						} else {
							classStyle = "action1"
						};

						tempHead[j] = {
							"headNum": temp[1],
							"classStyle": classStyle
						};
					};

					$scope.roomNumAuto[id] = tempAuto;
					$scope.roomNumHand[id] = tempHead;
				};


			} else {

				for (var i = 0; i < $scope.roomNum.length; i++) {
					var tempAuto = {};
					var tempHead = {};
					var id = $scope.cooped[i]["id"];


					for (var j = 0; j < daynum; j++) {
						var temp = [];
						var classStyle;
						temp = $scope.roomNum[i]["day" + (j + 1)].split("|");
						if (temp[0] == "0") {
							classStyle = "action1 man-close"
						} else {
							classStyle = "action1"
						};

						tempAuto[j] = {
							"autoNum": temp[0],
							"classStyle": classStyle
						};


						if (temp[1] == "0") {
							classStyle = "action1 man-close"
						} else {
							classStyle = "action1"
						};

						tempHead[j] = {
							"headNum": temp[1],
							"classStyle": classStyle
						};
					};

					$scope.roomNumAuto[id] = tempAuto;
					$scope.roomNumHand[id] = tempHead;
				};



			}



			console.log($scope.roomNumAuto)
			daynum = new Date(year, month, 0).getDate();
			for (var i = 1; i <= daynum; i++) {
				var temp;
				day.setDate(i);
				var tempday = day.getDay();
				var week = weekDay[tempday];
				if (tempday == 0 || tempday == 6) {
					temp = {
						"day": i,
						"weekday": week,
						"textcolor": {
							color: '#23A7F5'
						}
					};
				} else {
					temp = {
						"day": i,
						"weekday": week,
						"textcolor": {
							color: 'black'
						}
					};
				}
				$scope.dayWeekSum.push(temp);

			}

			if(monthvalue==1){
				
				$scope.dayWeekSum[currentDay-1]["day"]="今";
				$scope.dayWeekSum[currentDay-1]["weekday"]="天";
				$scope.dayWeekSum[currentDay-1]["textcolor"]={color: '#F30','font-weight': 'bold'};

			}

		}


	}])


})()