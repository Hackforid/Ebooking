(function() {

	var ratePlanApp = angular.module('ratePlanApp', []);


	ratePlanApp.config(['$httpProvider', function($httpProvider) {

		if (!$httpProvider.defaults.headers.get) {
			$httpProvider.defaults.headers.get = {};
			// $httpProvider.defaults.headers.post = {};    

		}

		$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	}]);



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
			scope.errMessage = '';
			$("#newRatePlanDialog").fadeIn(500);
		}
		this.close = function() {
			$("#newRatePlanDialog").fadeOut(500);
		}
		this.save = function() {
			if (!this.name) {
				scope.errMessage = '请输入有效名称';
				return;
			}


			var checkResult = this.name;

			var resultLen = checkResult.replace(/[\u4E00-\u6FA5]/g, "aa").length;

			if (resultLen > 20) {
				scope.errMessage = "名称不能超过20个字符";
				return;
			}



			scope.errMessage = '';
			//console.log(this.name + this.mealType + this.punishType);

			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomType["cooped_roomtype_id"] + '/rateplan/';
			console.log(url);
			var params = {
				'name': this.name,
				'meal_num': parseInt(this.mealType),
				'punish_type': parseInt(this.punishType)
			};
			console.log(params);

			http.post(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						scope.roomrates.push(resp.result.roomrate);
						scope.rateplans.push(resp.result.rateplan);
						scope.dateCheck(scope.monthvalue);
						$("#newRatePlanDialog").fadeOut(500);

					} else {
						//this.errmsg = resp.errmsg;

						//console.log(resp.errcode);
						if (resp.errcode == "405") {
							scope.errMessage = "名字已经存在";
						}
						if (resp.errcode == "404") {
							scope.errMessage = "没有可用房型";
						}

					}
				})
				.error(function() {
					console.log('network error');
				})
		}

	}

	var RoomHeadPlanDialog = function(scope, http) {
		this.scope = scope;
		this.http = http;
		this.errmsg = '';

		this.eachhide = function(index) {
			var roomRateName;
			roomRateName=scope.rateplans[index].name;

			$(("#roomheadinput"+index)).val(roomRateName);

			var punishValue;
			punishValue=scope.rateplans[index].punish_type;
			console.log(punishValue);

			$(("#roomheadpunish"+index)).val(punishValue);

			$("div.eachroom").eq(index).css("display", "none");





		}
		this.eachshow = function(index) {

			$("div.eachroom").eq(index).css("display", "block");

				var punishValue;
			punishValue=scope.rateplans[index].punish_type;
			$(("#roomheadpunish"+index)).val(punishValue);


			var tempmealsum = scope.roomrates[index].meal1.split("|", 1);
			$("#roomheadmeal" + index).val(tempmealsum[0]);

		}
		this.save = function(index) {
			this.errmsg = '';
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomType["cooped_roomtype_id"] + '/rateplan/' + scope.rateplans[index].id;
			//console.log(url);
			var params = {
				"name": ($("#roomheadinput" + index).val()),
				"meal_num": parseInt($("#roomheadmeal" + index).val()),
				"punish_type": parseInt($("#roomheadpunish" + index).val())
			};
			http.put(url, params)
				.success(function(resp) {
					//console.log(resp);
					if (resp.errcode == 0) {
						$("div.eachroom").eq(index).css("display", "none");

						scope.roomrates[index] = resp.result.roomrate;
						scope.rateplans[index] = resp.result.rateplan;

						scope.dateCheck(scope.monthvalue);
					} else {
						this.errmsg = resp.errmsg;
					}
				})
				.error(function() {
					console.log('network error');
				})
		};

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
			this.errmsg = ' ';
			$("#lowprice").val("");
		}


		/*乘法*/
		this.accMul = function(arg1, arg2) {
			var m = 0,
				s1 = arg1.toString(),
				s2 = arg2.toString();
			try {
				m += s1.split(".")[1].length;
			} catch (e) {}
			try {
				m += s2.split(".")[1].length;
			} catch (e) {}
			return Number(s1.replace(".", "")) * Number(s2.replace(".", "")) / Math.pow(10, m);
		}



		this.save = function() {

			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomType["cooped_roomtype_id"] + '/roomrate/' + scope.roomrates[scope.currentindex].id;
			var timeStart = $("#timeStart").val();
			var timeEnd = $("#timeEnd").val();


			var day = new Date();
			var month = day.getMonth() + 1;
			var year = day.getFullYear();
			var date = day.getDate();

			if (month < 10) {
				month = "0" + month;
			}
			if (date < 10) {
				date = "0" + date;
			}


			var startday = year + "-" + month + "-" + date;

			var ninetytime = day.getTime() + 1000 * 60 * 60 * 24 * 90;
			var ninetyday = new Date(ninetytime);
			var ninetymonth = ninetyday.getMonth() + 1;
			var ninetydate = ninetyday.getDate();
			var ninetyyear = ninetyday.getFullYear();

			if (ninetymonth < 10) {
				ninetymonth = "0" + ninetymonth;
			}
			if (ninetydate < 10) {
				ninetydate = "0" + ninetydate;
			}


			var endday = ninetyyear + "-" + ninetymonth + "-" + ninetydate;

			if (timeEnd == null || timeStart == null || timeEnd == "" || timeStart == "") {
				this.errmsg = '日期为空';
				return;
			} else if (timeEnd < timeStart) {
				this.errmsg = '开始日期大于结束日期';
				return;
			} else if (timeEnd > (endday + "") || timeStart < (startday + "")) {
				this.errmsg = '日期超出范围';
				return;
			}


			var testStr = /^\d+(\.\d{1,2})?$/;
			var priceTest = $.trim($("#lowprice").val());
			//console.log(priceTest);

			if (testStr.test(priceTest) == false) {
				this.errmsg = '房量为整数或小数,精确到小数点后两位';
				return;
			}
			if ((parseInt(priceTest)) > 9999.99) {
				this.errmsg = '房价最大不超过9999.99';
				return;
			}



			this.errmsg = ' ';
			//console.log(url);

			var price = this.accMul($.trim($("#lowprice").val()), 100);
			//console.log(price);
			var params = {
				"start_date": timeStart,
				"end_date": timeEnd,
				"price": price

			};
			http.put(url, params)
				.success(function(resp) {
					//console.log(resp);
					if (resp.errcode == 0) {
						$("#openDiv1").fadeOut(500);
						scope.roomrates[scope.currentindex] = resp.result.roomrate;
						scope.dateCheck(scope.monthvalue);
						$("#lowprice").val("");

					} else {
						this.errmsg = resp.errmsg;
					}
				})
				.error(function() {
					console.log('network error');
				})

		}

	}

	ratePlanApp.controller('ratePlanCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.roomtypes = [];
		$scope.hotel = {};
		$scope.newRatePlanDialog = new NewRatePlanDialog($scope, $http);
		$scope.roomRatePlanDialog = new RoomRatePlanDialog($scope, $http);
		$scope.roomHeadPlanDialog = new RoomHeadPlanDialog($scope, $http);
		$scope.currentRoomType = {};
		$scope.rateplans = {};
		$scope.roomrates = {};
		$scope.monthvalue = 1;
		$scope.months = [];
		$scope.dayWeekSum = [];
		$scope.dayPriceSum = {};
		$scope.currentindex = "";

		$scope.errMessage = "";

		$scope.currentHotelDetail = "";

		$scope.addChangeP = function addChangeP(d, m, c, n) {

			console.log($scope.currentRoomType);
			console.log(n);

			$scope.currentHotelDetail = n;


			var day = new Date();
			var currentDay = day.getDate();

			var ninetytime = new Date().getTime() + 1000 * 60 * 60 * 24 * 90;
			var ninetyday = new Date(ninetytime);
			var ninetycurrentDay = ninetyday.getDate();

			if ($scope.monthvalue == 1 && (c + 1) < currentDay) {
				return;
			}
			if ($scope.monthvalue == $scope.months.length && (c + 1) > ninetycurrentDay) {
				return;
			}


			$scope.currentindex = m;

			$(".div1").hide();

			$("#" + d).after("<div class='div1'><input name='' type='button' value='修改房价' class='btn-number' /></div>").show(0, function() {
				$(".btn-number").click(function() {
					$("#openDiv1").show();


					var month = $scope.months[$scope.monthvalue - 1]["month"];

					var date = c + 1;

					if (month < 10) {
						month = "0" + month;
					}
					if (date < 10) {
						date = "0" + date;
					}

					var inputCurrent = $scope.months[$scope.monthvalue - 1]["year"] + "-" + month + "-" + date;

					/*var day = new Date();

					var month = day.getMonth() + 1;
					var date = day.getDate();

					if (month < 10) {
						month = "0" + month;
					}
					if (date < 10) {
						date = "0" + date;
					}

					var inputCurrent = day.getFullYear() + "-" + month + "-" + date;*/
					$("#timeStart").val(inputCurrent);
					$("#timeEnd").val(inputCurrent);

				});
			});


			$("#" + d).mouseout(function() {

				$("#" + d).next("div").delay(1000).hide(0, function() {
					$("#" + d).next("div").remove();
				});

			});

		}

		function loadRoomTypes(_hotelId) {
			var url = "/api/hotel/" + _hotelId + "/roomtype/?simple=1";
			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.hotel = resp.result.hotel;
						$scope.roomtypes = resp.result.cooped_roomtypes;
						if ($scope.roomtypes.length > 0) {
							$scope.currentRoomType = $scope.roomtypes[0];
						}
					} else {
						console.log(resp.errmsg);
					}
				})
				.error(function() {
					console.log('network error');
				})
		}



		function monthCheck() {
			var day = new Date();
			var month = day.getMonth() + 1;
			var year = day.getFullYear();

			var ninetytime = day.getTime() + 1000 * 60 * 60 * 24 * 90;
			var ninetyday = new Date(ninetytime);
			var ninetymonth = ninetyday.getMonth() + 1;
			var monthcount = (ninetyday.getFullYear() - year) * 12 + (ninetyday.getMonth() + 1 - month) + 1;

			var temp = {};

			$scope.months.push({
				"month": month,
				"year": year
			});
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
				$scope.months.push(temp);
			}

		}

		function init() {
			$(".menu2").find("dd").eq(0).addClass("active");
			loadRoomTypes(hotelId);
			monthCheck();
		}

		init();

		$scope.$watch('currentRoomType', function() {
			if (!$scope.currentRoomType["base_roomtype_id"]) {
				return;
			}
			var url = '/api/hotel/' + hotelId + '/roomtype/' + $scope.currentRoomType["cooped_roomtype_id"] + '/rateplan/';
			//console.log(url);

			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.rateplans = resp.result.rateplans;
						$scope.roomrates = resp.result.roomrates;
					}

					//$scope.roomrates[0].month1 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";
					//$scope.roomrates[0].month12 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";
					//$scope.roomrates[1].month12 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";
					//$scope.roomrates[1].month1 = "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31";

					$scope.dateCheck($scope.monthvalue);
				})
				.error(function() {})
		});

		$scope.$watch('monthvalue', function() {


			$scope.dateCheck($scope.monthvalue);

		});

		$scope.dateCheck = function dateCheck(monthvalue) {
			if (typeof($scope.roomrates) === "object" && !($scope.roomrates instanceof Array)) {
				return;
			}

			$scope.dayWeekSum = [];
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
			var currentDay = day.getDate();


			if (monthvalue == 1) {
				daynum = day.getDate();
			} else if (monthvalue == $scope.months.length) {
				daynum = ninetyday.getDate();

			} else {
				daynum = new Date(year, month, 0).getDate();
			}


			var weekDay = new Array("日", "一", "二", "三", "四", "五", "六");

			for (var i = 0; i < ($scope.roomrates.length); i++) {
				var dayprice = [];
				var dayPriceArr = {};
				var tempdaysum = new Date(year, month, 0).getDate();

				var classstyle;
				var classPrice;
				var tempprice;
				var planid;


				dayprice = $scope.roomrates[i]["month" + month].split("|", tempdaysum);


				if (monthvalue == 1) {

					for (var a = 0; a < daynum - 1; a++) {
						classPrice = {
							"classstyle": "stop",
							"dayprice": "--"
						};
						dayPriceArr[a] = classPrice;

					};


					for (var j = daynum - 1; j < dayprice.length; j++) {

						if (dayprice[j] == "-1") {
							tempprice = "--";
							classstyle = "action5";

						} else if (dayprice[j] == "0") {
							tempprice = dayprice[j];
							classstyle = "action1 man-close";

						} else {
							tempprice = dayprice[j] / 100;
							classstyle = "action5";

						}
						classPrice = {
							"classstyle": classstyle,
							"dayprice": tempprice
						};
						dayPriceArr[j] = classPrice;
					}



				} else if (monthvalue == $scope.months.length) {


					for (var o = daynum; o < dayprice.length; o++) {
						classPrice = {
							"classstyle": "stop",
							"dayprice": "--"
						};
						dayPriceArr[o] = classPrice;

					};


					for (var j = 0; j < daynum; j++) {

						if (dayprice[j] == "-1") {
							tempprice = "--";
							classstyle = "action5";

						} else if (dayprice[j] == "0") {

							tempprice = dayprice[j];
							classstyle = "action1 man-close";


						} else {
							tempprice = dayprice[j] / 100;
							classstyle = "action5";

						}
						classPrice = {
							"classstyle": classstyle,
							"dayprice": tempprice
						};
						dayPriceArr[j] = classPrice;
					}


				} else {

					for (var j = 0; j < dayprice.length; j++) {

						if (dayprice[j] == "-1") {
							tempprice = "--";
							classstyle = "action5";

						} else if (dayprice[j] == "0") {
							tempprice = dayprice[j];
							classstyle = "action1 man-close";

						} else {
							tempprice = dayprice[j] / 100;
							classstyle = "action5";

						}
						classPrice = {
							"classstyle": classstyle,
							"dayprice": tempprice
						};
						dayPriceArr[j] = classPrice;
					}


				}

				/*for (var j = 0; j < dayprice.length; j++) {
					
					if (dayprice[j] == "-1") {
						tempprice = "--";
						classstyle = "stop";
					} else {
						tempprice = dayprice[j] / 100;
						classstyle = "action5";
					}
					temp = {
						"classstyle": classstyle,
						"dayprice": tempprice
					};
					temptwo[j] = temp;
				}*/
				planid = $scope.roomrates[i].rate_plan_id;

				$scope.dayPriceSum[planid] = dayPriceArr;
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
				$scope.dayWeekSum.push(temp);

			}

			if (monthvalue == 1) {

				$scope.dayWeekSum[currentDay - 1]["day"] = "今";
				$scope.dayWeekSum[currentDay - 1]["weekday"] = "天";
				$scope.dayWeekSum[currentDay - 1]["textcolor"] = {
					color: '#F30',
					'font-weight': 'bold'
				};

			}

		}

	}])


})()