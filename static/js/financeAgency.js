var financeApp = angular.module('financeApp', ['myApp.service']);


financeApp.config(['$httpProvider', function($httpProvider) {

	if (!$httpProvider.defaults.headers.get) {
		$httpProvider.defaults.headers.get = {};
		// $httpProvider.defaults.headers.post = {};    

	}

	$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
}]);


financeApp.controller('financeAppCtrl', ['$scope', '$http','log', function($scope, $http,log) {



	$scope.currentAccept;
	$scope.searchOtaId = "0";
	$scope.searchYear;
	$scope.searchMonth;
	$scope.finalUrl;
	$scope.yearOption;

	$scope.otaIncomes;
	$scope.otaOrders;

	$scope.incomeDetail = false;
	$scope.currentOtaIncome;
	$scope.currentOtaId;
	$scope.currentOtaOrders;

	$scope.addDetail = false;
	$scope.orderDetail = false;

	$scope.timeDetail = "";
	$scope.moneyDetail = "";
	$scope.remarkDetail = "";

	$scope.remarkErrMsg = "";



	$scope.currentOrder;
	$scope.detailOrder = false;

	$scope.detailInfo;


	$scope.allSumShow = false;



	//$scope.otaNames = ["全部", "去哪儿(优品房源)", "淘宝旅行", "美团", "携程(预付)", "艺龙", "去哪儿(酒店联盟)", "去哪儿(快团)", "去哪儿(酒店直销)", "百达屋", "携程(团购)"];

	$scope.otaNames = ["全部", "去哪儿", "淘宝旅行", "美团", "携程", "艺龙", "", "", "", "百达屋"];


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

			if ($.trim(currentBedType) != "" && currentBedType != undefined && currentBedType != null)

			{
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



	$scope.getAllSum = function(order) {

		var sum = 0;
		for (var i in order) {

			sum = parseFloat(sum) + parseFloat(order[i]['commission']);

		}

		return sum.toFixed(2);

	}


	$scope.getAllIncome = function(income) {

		var sum = 0;
		for (var i in income) {

			sum = sum + income[i]['sum'];

		}

		return sum;

	}



	$scope.getCurrentOrder = function(order) {

		$scope.currentOrder = order;
		$scope.detailInfo = $scope.infoconvent(order.customer_info);
		$scope.detailOrder = true;

	}

	$scope.resonStatusCheck = function(a, b) {

		if (a == "拒绝") {
			return b;
		} else {
			return "无";
		}


	}


	$scope.getCancelStatus = function(m,n) {

			var cancel;

			if (m == "0") {
				cancel="不可取消";
			} else if (m == "1") {
				cancel="自由取消";
			} else if (m == "2") {
				cancel="提前取消";
			}

			var punish;

			if (n == "0") {
				punish="不扣任何费用";
			} else if (n == "1") {
				punish="扣首晚房费";
			} else if (n == "2") {
				punish="扣全额房费";
			}else if (n == "3") {
				punish="扣定额";
			}else if (n == "4") {
				punish="扣全额房费百分比";
			}

			var cancelResult=cancel+",取消时"+punish;

			return cancelResult;



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


	$scope.incomeCheck = function(inc) {

		if (inc == undefined || inc == null) {

			return "0";

		} else {
			return inc;
		}

	}


	function dateTimeChecker(a, b, c) {
		var day = new Date();

		day.setFullYear(a);
		day.setMonth((b-1), 1);
		day.setDate(c);

		var dayTime = day.getTime();
		return dayTime;

	}


	$scope.ordDetail = function(id, ord) {

		$scope.currentOtaOrders = ord;
		log.log(ord);
		$scope.orderDetail = true;

	}

	$scope.timeConvert = function(time) {

		var creatTime = time.split(" ");
		return creatTime;

	}


	$scope.infoconvent = function(info) {

		var infoobj;

		try {

			infoobj = eval(info);

		} catch (e) {

			infoobj = [{
				"name": " "
			}];

		}

		return infoobj;

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


	function accMul(arg1, arg2) {
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



	$scope.addIncDetail = function() {

		if ($.trim($scope.moneyDetail) == null || $.trim($scope.moneyDetail) == undefined) {
			$scope.remarkErrMsg = "金额不能为空";
			return;

		}

		var testStr = /^-?\d+(\.\d{1,2})?$/;


		if (testStr.test($.trim($scope.moneyDetail)) == false) {
			$scope.remarkErrMsg = '金额为整数或小数,精确到小数点后两位';
			return;
		}



		var nameCheckValue = $.trim($scope.remarkDetail);
		var nameLength = nameCheckValue.replace(/[\u4e00-\u9fa5]/g, "aa").length;
		if (nameLength > 40) {

			$scope.remarkErrMsg = "备注长度不能超过20个字";
			return;

		}

		$scope.remarkErrMsg = "";

		var inTime = $scope.timeDetail;
		var splitTime = inTime.split("-");


		var currentOtaIds = [];
		/*if($scope.currentOtaId==1){

			currentOtaIds=[1,6,7,8];

		}else if($scope.currentOtaId==4){
			currentOtaIds=[4,10];

		}else{

			currentOtaIds.push($scope.currentOtaId);

		}*/

		currentOtaIds.push(parseInt($scope.currentOtaId));



		var params = {
			'remark': $.trim($scope.remarkDetail),
			'value': accMul($.trim($scope.moneyDetail), 100),
			'month': parseInt($scope.searchMonth),
			'year': parseInt($scope.searchYear),
			'ota_ids': currentOtaIds, //parseInt($scope.currentOtaId),
			'pay_type': 0

		};
		log.log(params);


		$http.post('/api/income/', params)
			.success(function(resp) {
				log.log(resp);
				if (resp.errcode == 0) {
					var otaInc = resp.result.income;

					if (otaInc.ota_id == 6 || otaInc.ota_id == 7 || otaInc.ota_id == 8 || otaInc.ota_id == 11 || otaInc.ota_id == 12) {

						otaInc.ota_id = 1;

					} else if (otaInc.ota_id == 10) {

						otaInc.ota_id = 4;

					}



					if ($scope.otaIncomes[$scope.currentOtaId] == undefined || $scope.otaIncomes[$scope.currentOtaId] == null) {

						var incVal = {};
						incVal = {

							"sum": parseInt(otaInc.value) / 100,
							"incomes": [otaInc],
							"name": $scope.otaNames[otaInc.ota_id] //otaInc.ota_name  

						};
						$scope.otaIncomes[otaInc.ota_id] = incVal;


					} else {
						$scope.otaIncomes[$scope.currentOtaId].incomes.push(resp.result.income);
						$scope.otaIncomes[$scope.currentOtaId].sum = parseInt($scope.otaIncomes[$scope.currentOtaId].sum) + parseInt(otaInc.value) / 100;
					}


					$scope.currentOtaIncome = $scope.otaIncomes[$scope.currentOtaId]; //.incomes.push(resp.result.income);
					log.log($scope.currentOtaIncome);


					log.log($scope.otaIncomes);



					$scope.addDetail = false;



				} else {


				}
			})
			.error(function() {
				log.log('network error');
			})

	}


	$scope.incDetail = function(id, inc) {
		$scope.incomeDetail = true;
		$scope.currentOtaIncome = inc;
		$scope.currentOtaId = id;
		log.log(inc);
		log.log(id);
	}


	$scope.closeDetail = function() {
		$scope.incomeDetail = false;

	}



	function init() {
		var day = new Date();
		var currentYear = day.getFullYear();
		var currentMonth = day.getMonth() + 1;

		$scope.searchYear = currentYear;
		$scope.searchMonth = currentMonth;

		$scope.yearOption = [{
			"value": currentYear
		}, {
			"value": (parseInt(currentYear) - 1)
		}];


		var currentDate = day.getDate();

		if (currentMonth < 10) {
			currentMonth = "0" + currentMonth;
		}
		if (currentDate < 10) {
			currentDate = "0" + currentDate;
		}


		var currentDayTime = currentYear + "-" + currentMonth + "-" + currentDate;


		$scope.timeDetail = currentDayTime;


	}



	$scope.urlCheck = function urlCheck() {

		if ($.trim($scope.searchOtaId) == "" || $scope.searchOtaId == undefined || $.trim($scope.searchYear) == "" || $scope.searchYear == undefined || $.trim($scope.searchMonth) == "" || $scope.searchMonth == undefined) {
			log.log("空值");
			return;
		}


		var url = '/api/finance/?year=' + parseInt($scope.searchYear) + "&month=" + parseInt($scope.searchMonth) + "&pay_type=0";

		if ($scope.searchOtaId != "0") {

			if ($scope.searchOtaId == 1) {

				url = url + "&ota_ids=[1,6,7,8,11,12]";

			} else if ($scope.searchOtaId == 4) {

				url = url + "&ota_ids=[4,10]";

			} else {


				url = url + "&ota_ids=[" + $.trim($scope.searchOtaId) + "]";

			}


		}


		log.log(url);
		$scope.finalUrl = encodeURI(url);
		log.log($scope.finalUrl);

		$scope.searchResult();

	}

	$scope.searchResult = function searchResult() {

		$http.get($scope.finalUrl)
			.success(function(resp) {
				log.log(resp);
				if (resp.errcode == 0) {


					/*数据测试*/
					/*resp = {
						"errcode": 0,
						"errmsg": null,
						"result": {
							"orders": [{
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:28:03",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 3,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 92,
								"customer_remark": "",
								"customer_info": "[{'name':'华丽'}]",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "10000",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 100,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "美团",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:30:34",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 3,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 93,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "10000",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 101,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "美团",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:31:15",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 9,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 94,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 102,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 2,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 8,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 7,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 6,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 4,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 1,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "test",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 4,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 10,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 4,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 4,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 7,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 6,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "testone",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 6,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "去哪儿(酒店联盟)",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 2,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}, {
								"confirm_type": 2,
								"extra": "",
								"punish_value": 0,
								"guarantee_start_time": "00:00:00",
								"create_time": "2015-01-22 15:33:50",
								"contact_name": "",
								"guarantee_info": "",
								"ota_id": 2,
								"breakfast": "",
								"roomtype_id": 105,
								"pay_type": 1,
								"guarantee_type": 0,
								"rateplan_id": 98,
								"id": 95,
								"customer_remark": "",
								"customer_info": "",
								"status": 300,
								"roomtype_name": "",
								"customer_num": 0,
								"hotel_id": 187,
								"arrival_time": "18:00:00",
								"contact_email": "",
								"cancel_type": 1,
								"contact_mobile": "",
								"checkin_date": "2015-01-22",
								"checkout_date": "2015-01-23",
								"hotel_name": "",
								"everyday_price": "0",
								"total_price": 1000,
								"currency_type": "0",
								"bed_type": 0,
								"punish_type": 0,
								"main_order_id": 103,
								"rateplan_name": "",
								"room_num_record": "0|2",
								"ota_name": "淘宝旅行",
								"room_num": 2
							}],
							"incomes": [{
								"pay_type": 1,
								"remark": "",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "淘宝旅行",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 2,
								"id": 1
							}, {
								"pay_type": 1,
								"remark": "",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "淘宝旅行",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 2,
								"id": 1
							}, {
								"pay_type": 1,
								"remark": "",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "淘宝旅行",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 2,
								"id": 1
							}, {
								"pay_type": 1,
								"remark": "欢迎欢迎欢迎欢迎欢迎欢迎欢迎欢迎欢迎欢迎",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "淘宝旅行",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 2,
								"id": 1
							}, {
								"pay_type": 1,
								"remark": "",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "淘宝旅行",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 2,
								"id": 1
							}, {
								"pay_type": 1,
								"remark": "",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "淘宝旅行",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 2,
								"id": 1
							}, {
								"pay_type": 1,
								"remark": "",
								"create_date": "2015-02-04",
								"is_delete": 0,
								"value": 1000,
								"month": 1,
								"ota_name": "美团",
								"year": 2015,
								"merchant_id": 1,
								"ota_id": 0,
								"id": 1
							}]
						}
					};*/

					/*income*/

					var otaInc = resp.result.incomes;
					var allOtaInc = {};
					for (var i = 0; i < otaInc.length; i++) {

						if (otaInc[i].ota_id == 6 || otaInc[i].ota_id == 7 || otaInc[i].ota_id == 8 || otaInc[i].ota_id == 11 || otaInc[i].ota_id == 12) {

							otaInc[i].ota_id = 1;

						} else if (otaInc[i].ota_id == 10) {

							otaInc[i].ota_id = 4;

						}



						if ((otaInc[i].ota_id != 0) && ($scope.otaNames[otaInc[i].ota_id] != undefined)) {
							if (allOtaInc[otaInc[i].ota_id] == undefined || allOtaInc[otaInc[i].ota_id] == null) {

								var incVal = {};
								incVal = {

									"sum": parseInt(otaInc[i].value) / 100,
									"incomes": [otaInc[i]],
									"name": $scope.otaNames[otaInc[i].ota_id] //otaInc[i].ota_name

								};
								allOtaInc[otaInc[i].ota_id] = incVal;

							} else {
								allOtaInc[otaInc[i].ota_id]['sum'] = parseInt(allOtaInc[otaInc[i].ota_id]['sum']) + parseInt(otaInc[i].value) / 100;
								allOtaInc[otaInc[i].ota_id]['incomes'].push(otaInc[i]);

							}

						}



					};



					log.log(allOtaInc);
					$scope.otaIncomes = allOtaInc;


					/*order*/
					var otaOrd = resp.result.orders;
					var allotaOrd = {};
					for (var i = 0; i < otaOrd.length; i++) {



						if (otaOrd[i].ota_id == 6 || otaOrd[i].ota_id == 7 || otaOrd[i].ota_id == 8 || otaOrd[i].ota_id == 11 || otaOrd[i].ota_id == 12) {

							otaOrd[i].ota_id = 1;

						} else if (otaOrd[i].ota_id == 10) {

							otaOrd[i].ota_id = 4;

						}



						if ((otaOrd[i].ota_id != 0) && ($scope.otaNames[otaOrd[i].ota_id] != undefined)) {
							if (allotaOrd[otaOrd[i].ota_id] == undefined || allotaOrd[otaOrd[i].ota_id] == null) {

								var ordVal = {};
								ordVal = {

									"sum": parseInt(otaOrd[i].total_price) / 100,
									"commission": parseInt(otaOrd[i].commission) / 100,
									"orders": [otaOrd[i]],
									"name": $scope.otaNames[otaOrd[i].ota_id] //otaOrd[i].ota_name

								};
								allotaOrd[otaOrd[i].ota_id] = ordVal;
								allotaOrd[otaOrd[i].ota_id]['commission']=allotaOrd[otaOrd[i].ota_id]['commission'].toFixed(2);

							} else {
								allotaOrd[otaOrd[i].ota_id]['sum'] = parseInt(allotaOrd[otaOrd[i].ota_id]['sum']) + parseInt(otaOrd[i].total_price) / 100;
								allotaOrd[otaOrd[i].ota_id]['commission'] = parseFloat(allotaOrd[otaOrd[i].ota_id]['commission']) + parseFloat(otaOrd[i].commission / 100) ;
								allotaOrd[otaOrd[i].ota_id]['commission']=allotaOrd[otaOrd[i].ota_id]['commission'].toFixed(2);
								allotaOrd[otaOrd[i].ota_id]['orders'].push(otaOrd[i]);

							}
						}



					};

					log.log(allotaOrd);


					$scope.otaOrders = allotaOrd;
					/*var otaOrd=resp.result.orders;


					$scope.otaIncomes;
					$scope.otaOrders;*/

					if ($scope.searchOtaId == "0") {

						if (isEmptyObject($scope.otaOrders)) {
							$scope.allSumShow = false;

						} else {
							$scope.allSumShow = true;

						}



					} else {
						$scope.allSumShow = false;
					}



				} else {


				}
			})
			.error(function() {
				log.log('network error');
			})


	}

	function isEmptyObject(obj) {
		for (var n in obj) {
			return false;
		}
		return true;
	}

	$scope.conditionReset = function conditionReset() {

		$scope.searchOtaId = "";
		$scope.searchYear = "";
		$scope.searchMonth = "";


	}

	$(".menu4").find("dd").eq(1).addClass("active");

	init();
	$scope.urlCheck();



}]);
