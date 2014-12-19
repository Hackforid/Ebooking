(function() {

	var ratePlanApp = angular.module('ratePlanApp', []);

	ratePlanApp.filter('orderObjectBy', function() {
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

	var NewRatePlanDialog = function(scope, http) {
		this.scope = scope;
		this.http = http;

		this.name = '';
		this.mealType = 0;
		this.punishType = 0;

		this.errmsg = '';

		this.open = function() {
			this.name = '';
			this.mealType = 0;
			this.punishType = 0;
			this.errmsg = '';
			$("#newRatePlanDialog").fadeIn(500);
		}
		this.close = function() {
			$("#newRatePlanDialog").fadeOut(500);
		}
		this.save = function() {
			if (!this.name) {
				this.errmsg = '请输入有效名称';
				return;
			}

			this.errmsg = '';
			console.log(this.name + this.mealType + this.punishType);

			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomType.id + '/rateplan/';
			console.log(url);
			var params = {
				'name': this.name,
				'meal_type': this.mealType,
				'punish_type': this.punishType
			};
			console.log(params);
			http.post(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {} else {
						this.errmsg = resp.errmsg;
					}
				})
				.error(function() {
					this.errmsg = '网络错误';
				})
		}

	}

	var RoomRatePlanDialog = function(scope, http) {
		this.scope = scope;
		this.http = http;

		this.name = '';
		this.mealType = 0;
		this.punishType = 0;

		this.errmsg = '';
		this.close = function() {

			$("#openDiv1").fadeOut(500);
		}
		this.save = function() {

			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomType.id + '/roomrate/' + scope.currentid;
			var time1 = $("#time1").val();
			var time2 = $("#time2").val();
			var price = parseInt($("#lowprice").val());

			if (time2 < time1) {
				this.errmsg = '开始日期大于结束日期';
			}
			if (time2 == null || time1 == null || time2 == "" || time1 == "") {
				console.log("null");
				this.errmsg = '日期为空';
			}

			console.log(url);
			var params = {
				"start_date": time1,
				"end_date": time2,
				"price": price

			};
			console.log(params);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$("#openDiv1").fadeOut(500);
					} else {
						this.errmsg = resp.errmsg;
					}
				})
				.error(function() {
					this.errmsg = '网络错误';
				})



		}

	}



	ratePlanApp.controller('ratePlanCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.roomtypes = [];
		$scope.hotel = {};
		$scope.newRatePlanDialog = new NewRatePlanDialog($scope, $http);
		$scope.roomRatePlanDialog = new RoomRatePlanDialog($scope, $http);
		$scope.currentRoomType = {};
		$scope.rateplans = {};
		$scope.roomrates = {};
		$scope.monthvalue = 1;
		$scope.months = {};
		$scope.dayWeekSum = [];
		$scope.dayPriceSum = {};
		$scope.currentid = "";

		$scope.addChangeP = function addChangeP(d, c) {

			if (c == "action5") {
				var temp = d.split("-", 1);
				$scope.currentid = temp[0];


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


		$scope.eachhide = function(index) {

			$("div.eachroom").eq(index).css("display", "none");
		}
		$scope.eachshow = function(index) {

			$("div.eachroom").eq(index).css("display", "block");

		}

		function loadRoomTypes(_hotelId) {
			var url = "/api/hotel/" + _hotelId + "/roomtype/?simple=1";
			$http.get(url)
				.success(function(resp) {
					console.log(resp)
					if (resp.errcode == 0) {
						$scope.hotel = resp.result.hotel;
						$scope.roomtypes = resp.result.cooped_roomtypes;
						if ($scope.roomtypes.length > 0) {
							$scope.currentRoomType = $scope.roomtypes[0];
						}
					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})
		}

		loadRoomTypes(hotelId);


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
			console.log($scope.months);
		}

		monthCheck();

		$scope.$watch('currentRoomType', function() {
			if (!$scope.currentRoomType.id) {
				return;
			}
			var url = '/api/hotel/' + hotelId + '/roomtype/' + $scope.currentRoomType.id + '/rateplan/';
			console.log(url);

			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.rateplans = resp.result.rateplans;
						$scope.roomrates = resp.result.roomrates;
					}
					console.log($scope.roomrates);

					$scope.roomrates[0].month12 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";

					dateCheck($scope.monthvalue);
				})
				.error(function() {})
		});

		$scope.$watch('monthvalue', function() {
			//$scope.dayPriceSum = {};
			$scope.dayWeekSum = [];
			dateCheck($scope.monthvalue);

		});


		function dateCheck(monthvalue) {
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
			var daynum;


			if (monthvalue == 1) {
				daynum = day.getDate();
			} else if (monthvalue == 4) {
				daynum = ninetyday.getDate();

			} else {
				daynum = new Date(year, month, 0).getDate();
			}



			/*测试测试*/
			//$scope.roomrates[0].month1 = "99|66|45|-1|33|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1";

			//$scope.roomrates[0].month12 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";
			//$scope.roomrates[0].month3 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";


			//	$scope.roomrates[1].month12 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";

			var weekDay = new Array("日", "一", "二", "三", "四", "五", "六");


			for (var i = 0; i < ($scope.roomrates.length); i++) {
				var dayprice = [];
				var temptwo = {};
				var tempdaysum = new Date(year, month, 0).getDate();

				dayprice = $scope.roomrates[i]["month" + month].split("|", tempdaysum);

				if (monthvalue == 1) {
					//console.log(daynum);
					for (var a = 0; a < daynum - 1; a++) {
						dayprice[a] = "-1"
					};
					//console.log(dayprice);								

				} else if (monthvalue == 4) {
					for (var o = daynum; o < ninetysum; o++) {
						dayprice[o] = "-1"
					};

				}


				for (var j = 0; j < dayprice.length; j++) {
					var classstyle;
					var temp;
					var tempprice;
					if (dayprice[j] == "-1") {
						tempprice = "--";
						classstyle = "stop";
					} else {
						tempprice = dayprice[j];
						classstyle = "action5";
					}
					temp = {
						"classstyle": classstyle,
						"dayprice": tempprice
					};
					//console.log("temp");console.log(temp);
					temptwo[j] = temp;
				}
				var planid = $scope.roomrates[i].rate_plan_id;

				$scope.dayPriceSum[planid] = temptwo;
			}

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
				//var temp={"day":i,"weekday":week};
				$scope.dayWeekSum.push(temp);

			}



			//console.log($scope.dayPriceSum);
			//console.log($scope.months);

			//console.log($scope.currentRoomType );


		}



	}])


})()