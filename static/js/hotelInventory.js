(function() {

	var hotelInventoryApp = angular.module('hotelInventoryApp', []);


	hotelInventoryApp.config(['$httpProvider', function($httpProvider) {

		if (!$httpProvider.defaults.headers.get) {
			$httpProvider.defaults.headers.get = {};
			// $httpProvider.defaults.headers.post = {};    

		}

		$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	}]);



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

	/*$("#roomtype-list .action input").click(function() {
		$("#roomtype-list").fadeOut(500);
	});*/


	var HotelHeadDialog = function(scope, http) {
		this.scope = scope;
		this.http = http;
		this.name = '';
		this.mealType = 0;
		this.punishType = 0;
		this.errmsg = '';

		this.prefixName = "";
		this.remarkName = "";


		/*this.exampleDivIn = function(index) {

			$("#exampleDiv-" + index).after("<span class='example' style='position:relative;'>示例：<b>170元</b></span>").show(0, function() {});

		}
		this.exampleDivLeave = function(index) {

			$("#exampleDiv-" + index).next("span.example").hide(0, function() {
				$("#exampleDiv-" + index).next("span.example").remove();
			});

		}*/


		this.eachhide = function(index) {

			$("div.eachroom").eq(index).css("display", "none");

		}
		this.eachshow = function(index) {

			$("div.eachroom").eq(index).css("display", "block");
			//var tempmealsum = scope.roomrates[index].meal1.split("|", 1);
			//$("#roomheadmeal" + index).val(tempmealsum[0]);

		}

		this.save = function(index) {

			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.cooped[index]["cooped_roomtype_id"] + '/cooped/';

			var params = {
				"prefix_name": $("#prefixId-" + index).val(),
				"remark_name": $("#remarkId-" + index).val()
			}

			//	console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("div.eachroom").eq(index).css("display", "none");

						scope.cooped[index]["prefix_name"] = resp.result.cooped_roomtype["prefix_name"];
						scope.cooped[index]["remark_name"] = resp.result.cooped_roomtype["remark_name"];

					} else {
						this.errmsg = resp.errmsg;
						//	console.log(errmsg);
					}
				})
				.error(function() {
					console.log('network error');
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
			this.errmsg = ' ';
			scope.num = "";
		}


		this.dateCheck = function(timeStart, timeEnd) {
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

			var ninetytime = day.getTime() + 1000 * 60 * 60 * 24 * 364;
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
				return 0;
			} else if (timeEnd < timeStart) {
				this.errmsg = '开始日期大于结束日期';
				return 0;
			} else if (timeEnd > (endday + "") || timeStart < (startday + "")) {
				this.errmsg = '日期超出范围';
				return 0;
			}



			this.errmsg = ' ';

		}

		function timeStartCheck(timeStart) {

			var choosedTime = timeStart.split("-");
			var currentYear = scope.months[scope.monthvalue - 1].year;
			var currentMonth = scope.months[scope.monthvalue - 1].month;


			if (choosedTime[0] == currentYear && parseInt(choosedTime[1]) == currentMonth) {
												
				return 1;
			} else {
				return 0;
			}

		}


		this.roomNumCheck = function() {

			var testStr = /^[0-9]*[1-9][0-9]*$/;
			var roomNumCount = $.trim($("#roomNumCount").val());

			if (testStr.test(roomNumCount) == false) {
				this.errmsg = '房量为正整数';
				return 0;
			}
			if ((parseInt(roomNumCount)) > 99) {
				this.errmsg = '房量最大不超过99间';
				return 0;
			}

			this.errmsg = ' ';
		}



		this.addSave = function() {
			var timeStart = $("#timeStart").val();
			var timeEnd = $("#timeEnd").val();
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomId + '/inventory/';

			if (this.dateCheck(timeStart, timeEnd) == 0) {
				return;
			}

			if (this.roomNumCheck() == 0) {
				return;
			}

			var params = {
				"start_date": timeStart,
				"end_date": timeEnd,
				"change_num": parseInt($.trim($("#roomNumCount").val())),
				"price_type": parseInt(scope.currentPriceType)

			}

			//	console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("#openDiv1").fadeOut(500);

						scope.roomNum = [];

					if (timeStartCheck(timeStart)) {
						
						scope.cooped[scope.currentIndex].inventory = resp.result.inventories[0];

						scope.dateCheck(scope.monthvalue);
					}

						scope.num = "";

					} else {
						this.errmsg = resp.errmsg;
						//	console.log(errmsg);
					}
				})
				.error(function() {
					console.log('network error');
				})



		}
		this.minusSave = function() {
			var timeStart = $("#timeStart").val();
			var timeEnd = $("#timeEnd").val();
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomId + '/inventory/';

			if (this.dateCheck(timeStart, timeEnd) == 0) {
				return;
			}

			if (this.roomNumCheck() == 0) {
				return;
			}

			var params = {
				"start_date": timeStart,
				"end_date": timeEnd,
				"change_num": -parseInt($.trim($("#roomNumCount").val())),
				"price_type": parseInt(scope.currentPriceType)

			}

			//	console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("#openDiv1").fadeOut(500);

						scope.roomNum = [];

					if (timeStartCheck(timeStart)) {
						
						scope.cooped[scope.currentIndex].inventory = resp.result.inventories[0];

						scope.dateCheck(scope.monthvalue);
					}

						scope.num = "";

					} else {
						this.errmsg = resp.errmsg;
						//	console.log(errmsg);
					}
				})
				.error(function() {
					console.log('network error');
				})

		}


		this.zeroSave = function() {

			var tempNum = $.trim($("#" + scope.currentId).html());

			var timeStart = $("#timeStart").val();
			var timeEnd = $("#timeEnd").val();
			var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomId + '/inventory/';

			if (this.dateCheck(timeStart, timeEnd) == 0) {
				return;
			}

			var params = {
				"start_date": timeStart,
				"end_date": timeEnd,
				"change_num": 0,
				"price_type": parseInt(scope.currentPriceType)

			}

			//	console.log(url);
			http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$("#openDiv1").fadeOut(500);

						scope.roomNum = [];

					if (timeStartCheck(timeStart)) {
						
						scope.cooped[scope.currentIndex].inventory = resp.result.inventories[0];

						scope.dateCheck(scope.monthvalue);
					}

						scope.num = "";

					} else {
						this.errmsg = resp.errmsg;
						//	console.log(errmsg);
					}
				})
				.error(function() {
					console.log('network error');
				})



		}


	}



	hotelInventoryApp.controller('hotelInventoryCtrl', ['$scope', '$http', function($scope, $http) {

		//$scope.desResult = false;
		$scope.hotel = {};
		$scope.willCoop = [];
		$scope.cooped = [];
		$scope.selecableMonths = [1, 2, 3];
		$scope.monthvalue = 1;

		$scope.testone;
		$scope.months = [];
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


		$scope.roomDescribeInfo = {};
		$scope.roomBedType = ['单床', '大床', '双床', '三床', '三床-1大2单', '榻榻米', '拼床', '水床', '榻榻米双床', '榻榻米单床', '圆床', '上下铺', '大床或双床'];



		$scope.allFacilityNum = {
			"36": "大床",
			"37": "双床",
			"38": "单人床",
			"39": "特殊床型",
			"40": "其他",
			"41": "大床1.8米",
			"42": "大床1.5米",
			"43": "大床2米",
			"44": "其他",
			"45": "双床1.2米",
			"46": "双床1.1米",
			"47": "双床1.3米",
			"48": "双床1.35米",
			"49": "其他",
			"50": "单人床1.2米",
			"51": "单人床1.1米",
			"52": "单人床1.3米",
			"53": "单人床1.35米",
			"54": "其他",
			"55": "三张床",
			"56": "圆床",
			"57": "水床",
			"58": "上下铺",
			"59": "榻榻米",
			"62": "不能上网",
			"63": "全部房间上网",
			"64": "部分房间上网",
			"65": "免费无线",
			"66": "收费无线",
			"67": "免费有线",
			"68": "收费有线",
			"69": "免费无线",
			"70": "收费无线",
			"71": "免费有线",
			"72": "收费有线",
			"74": "电话",
			"76": "国内长途电话",
			"77": "国际长途电话",
			"78": "一次性洗漱用品",
			"79": "不提供一次性洗漱用品",
			"80": "免费提供一次性洗漱用品",
			"81": "收费提供一次性洗漱用品",
			"82": "电热水壶",
			"84": "无窗",
			"108": "浴缸",
			"109": "拖鞋",
			"110": "电视",
			"111": "独立写字台",
			"112": "吹风机",
			"113": "多种规格电源插座",
			"114": "110V电压插座",
			"115": "浴室放大化妆镜",
			"116": "保险箱",
			"117": "小冰箱",
			"118": "迷你酒吧",
			"119": "免费瓶装水",
			"120": "浴衣",
			"121": "电子磁卡门锁",
			"122": "座椅",
			"123": "雨伞",
			"124": "针线包",
			"125": "熨斗/熨衣板",
			"126": "多功能充电器",
			"127": "办公文具",
			"128": "无烟房",
			"129": "可做无烟处理",
			"130": "220V电压插座",
			"131": "沙发",
			"132": "咖啡机/茶具",
			"133": "厨房",
			"134": "电子称",
			"135": "阳台",
			"136": "电子闹钟",
			"137": "洗衣机/烘干机",
			"138": "音响设备/收音机",
			"139": "播放机",
			"140": "房间免费报纸",
			"141": "微波沪",
			"142": "电子遥控窗帘",
			"143": "电热水器",
			"144": "卫星频道",
			"145": "传真机",
			"146": "餐具",
			"147": "提供直饮水",
			"148": "卫生间",
			"149": "室内卫生间",
			"150": "公共卫生间",
			"151": "电脑",
			"152": "全部房间收费电脑",
			"153": "全部房间免费电脑",
			"154": "部分房间免费电脑",
			"155": "洗浴间",
			"156": "室内洗浴间",
			"157": "公共洗浴间",
			"248": "淋浴",
			"249": "麻将桌",
			"266": "大/双床",
			"267": "大/双床",
			"677": "有窗"
		};



		$scope.confirmCancel=false;
		$scope.cancelIndex;


		$('#timeStart').datepicker({

			format: "yyyy-mm-dd",
			language: "zh-CN",
			orientation: "top auto",
			autoclose: true,
			enableOnReadonly: true,
			showOnFocus: true


		});

		$('#timeEnd').datepicker({

			format: "yyyy-mm-dd",
			language: "zh-CN",
			orientation: "top auto",
			autoclose: true,
			enableOnReadonly: true,
			showOnFocus: true


		});


		$scope.conventIdInt=function(id){
			
			return (parseInt(id)+1);

		}


		$scope.confirmOk=function(){ 

			
			var url="/api/hotel/" + hotelId + "/roomtype/"+$scope.cooped[$scope.cancelIndex].cooped_roomtype_id+"/cooped";

			console.log(url);

			$http({method: 'DELETE', url: url})
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$scope.willCoop.push($scope.cooped[$scope.cancelIndex]);
						$scope.cooped.splice($scope.cancelIndex,1);
						$scope.confirmCancel=false;
						
					} else {
						console.log(resp.errmsg);
					}
				})
				.error(function() {
					console.log('network error');
				})



		}

		$scope.cancelBtn=function(index){
			//console.log(index);
			$scope.confirmCancel=true;
			$scope.cancelIndex=index;

		}





		$scope.filterNum = function(n) {
			if (n > 0) {
				var numResult;
				numResult = "(" + n + ")";
				return numResult;
			}
		}



		$scope.nameTest = function(e) {
			return e != null;
		}



		$scope.roomDescribe = function roomDescribe(index) {

			$scope.roomDescribeInfo = $scope.cooped[index];

			var bedTypeIndex = $scope.roomDescribeInfo['bed_type'];
			$scope.roomDescribeInfo['bed_type'] = $scope.roomBedType[bedTypeIndex];


			if (typeof $scope.roomDescribeInfo['facility'] === 'string') {
				var facilityNumber = [];
				facilityNumber = $scope.roomDescribeInfo['facility'].split(",");
				var facilitys = [];

				for (var i = 0; i < facilityNumber.length; i++) {
					facilitys.push($scope.allFacilityNum[facilityNumber[i]]);

				};

				$scope.roomDescribeInfo['facility'] = facilitys;
			}

			$("#cool-roomtype").show();



		}



		$scope.willroomDescribe = function roomDescribe(index) {


			$scope.roomDescribeInfo = $scope.willCoop[index];

			var bedTypeIndex = $scope.roomDescribeInfo['bed_type'];
			$scope.roomDescribeInfo['bed_type'] = $scope.roomBedType[bedTypeIndex];


			if (typeof $scope.roomDescribeInfo['facility'] === 'string') {
				var facilityNumber = [];
				facilityNumber = $scope.roomDescribeInfo['facility'].split(",");
				var facilitys = [];

				for (var i = 0; i < facilityNumber.length; i++) {
					facilitys.push($scope.allFacilityNum[facilityNumber[i]]);

				};

				$scope.roomDescribeInfo['facility'] = facilitys;
			}


			$("#cool-roomtype").show();


		}



		$scope.roomDescribeClose = function roomDescribeClose() {
			//$scope.desResult = false;
			$("#cool-roomtype").hide();

		}


		$scope.changeNum = function changeNum(d, c, i, p, m, w) {


			if (c != "stop") {
				$scope.currentRoomId = i;
				$scope.currentIndex = p;
				$scope.currentPriceType = m;
				$scope.currentId = d;

				$(".div1").hide();

				$("#" + d).after("<div class='div1'><input name='' type='button' value='修改房量' class='btn-number' /></div>").show(0, function() {
					$(".btn-number").click(function() {
						$("#openDiv1").show();


						var month = $scope.months[$scope.monthvalue - 1]["month"];

						var date = w + 1;

						if (month < 10) {
							month = "0" + month;
						}
						if (date < 10) {
							date = "0" + date;
						}


						/*var day = new Date();
						var month = day.getMonth() + 1;
						var date = day.getDate();

						if (month < 10) {
							month = "0" + month;
						}
						if (date < 10) {
							date = "0" + date;
						}*/


						var inputCurrent = $scope.months[$scope.monthvalue - 1]["year"] + "-" + month + "-" + date;
						$("#timeStart").val(inputCurrent).datepicker('update');
						$("#timeEnd").val(inputCurrent).datepicker('update');

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

		}

		$scope.saveNewRoomType = function() {
			var shouldCooped = [];
			for (var i = 0; i < $scope.willCoop.length; i++) {
				if ($scope.willCoop[i].isChecked) {
					shouldCooped.push($scope.willCoop[i].id);
				}
			}

			var url = "/api/hotel/" + hotelId + "/roomtype/";
			//console.log(url);
			//console.log(shouldCooped);
			$http.post(url, {
					'roomtype_ids': shouldCooped
				})
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						loadHotelMsg(hotelId);

						$("#roomtype-list").fadeOut(500);


					} else {
						//console.log(resp.errmsg);
					}
				})
				.error(function() {
					console.log('network error');
				})
		}

		$scope.closeRoomType = function() {
			$("#roomtype-list").fadeOut(500);

		}

		function initMonthWatch() {

			$scope.$watch('monthvalue', function() {
				if ($scope.monthvalue == undefined) {
					return;
				}
				$scope.roomNum = [];

				loadHotelMsg(hotelId);
			});
		}


		function loadHotelMsg(hotel_id) {
			var url = "/api/hotel/" + hotel_id + "/roomtype/?year=" + $scope.months[$scope.monthvalue - 1].year + "&month=" + $scope.months[$scope.monthvalue - 1].month;
			console.log(url);
			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.hotel = resp.result.hotel;
						$scope.willCoop = resp.result.will_coop_roomtypes;
						$scope.cooped = resp.result.cooped_roomtypes;

						//$scope.cooped[1].inventory = $scope.cooped[0].inventory;

						$scope.dateCheck($scope.monthvalue);

					} else {
						console.log(resp.errmsg);
					}
				})
				.error(function() {
					console.log('network error');
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
			$(".menu2").find("dd").eq(0).addClass("active");

			monthCheck();
			initMonthWatch();
		}

		init();


		function monthCheck() {
			var day = new Date();
			var month = day.getMonth() + 1;
			var year = day.getFullYear();

			var ninetytime = day.getTime() + 1000 * 60 * 60 * 24 * 364;
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



		$scope.dateCheck = function dateCheck(monthvalue) {

			if (typeof($scope.roomrates) === "object" && !($scope.roomrates instanceof Array)) {
				return;
			}

			var day = new Date();
			var year = $scope.months[monthvalue - 1].year;
			var month = $scope.months[monthvalue - 1].month;
			day.setFullYear(year);
			day.setMonth(month - 1);

			var ninetytime = new Date().getTime() + 1000 * 60 * 60 * 24 * 364;
			var ninetyday = new Date(ninetytime);
			var ninetyyear = ninetyday.getFullYear();
			var ninetymonth = ninetyday.getMonth() + 1;

			var ninetysum = new Date(ninetyyear, ninetymonth, 0).getDate();
			var daynum;
			var currentDay = day.getDate();
			$scope.dayWeekSum = [];


			if (monthvalue == 1) {
				daynum = day.getDate();
			} else if (monthvalue == $scope.months.length) {
				daynum = ninetyday.getDate();

			} else {
				daynum = new Date(year, month, 0).getDate();
			}


			var weekDay = new Array("日", "一", "二", "三", "四", "五", "六");

			/*赋值部分*/
			$scope.roomNum = [];
			for (var i = 0; i < $scope.cooped.length; i++) {
				if ($scope.cooped[i].inventory != undefined && $scope.cooped[i].inventory != null) {
					$scope.roomNum.push($scope.cooped[i].inventory);
				} else {
					var tempInventory = {

						day1: "-1|-1",
						day2: "-1|-1",
						day3: "-1|-1",
						day4: "-1|-1",
						day5: "-1|-1",
						day6: "-1|-1",
						day7: "-1|-1",
						day8: "-1|-1",
						day9: "-1|-1",
						day10: "-1|-1",
						day11: "-1|-1",
						day12: "-1|-1",
						day13: "-1|-1",
						day14: "-1|-1",
						day15: "-1|-1",
						day16: "-1|-1",
						day17: "-1|-1",
						day18: "-1|-1",
						day19: "-1|-1",
						day20: "-1|-1",
						day21: "-1|-1",
						day22: "-1|-1",
						day23: "-1|-1",
						day24: "-1|-1",
						day25: "-1|-1",
						day26: "-1|-1",
						day27: "-1|-1",
						day28: "-1|-1",
						day29: "-1|-1",
						day30: "-1|-1",
						day31: "-1|-1"

					};

					$scope.roomNum.push(tempInventory);
				}
			};
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
							classStyle = "action1 man-close";
						} else if (temp[0] == "-1") {
							classStyle = "action1";
							temp[0] = "--";
						} else {
							classStyle = "action1";
						};

						tempAuto[j] = {
							"autoNum": temp[0],
							"classStyle": classStyle
						};
						if (temp[1] == "0") {
							classStyle = "action1 man-close"
						} else if (temp[1] == "-1") {
							classStyle = "action1";
							temp[1] = "--";
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

			} else if (monthvalue == $scope.months.length) {

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
						} else if (temp[0] == "-1") {
							classStyle = "action1";
							temp[0] = "--";
						} else {
							classStyle = "action1"
						};

						tempAuto[j] = {
							"autoNum": temp[0],
							"classStyle": classStyle
						};


						if (temp[1] == "0") {
							classStyle = "action1 man-close"
						} else if (temp[1] == "-1") {
							classStyle = "action1";
							temp[1] = "--";
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
						} else if (temp[0] == "-1") {
							classStyle = "action1";
							temp[0] = "--";
						} else {
							classStyle = "action1"
						};

						tempAuto[j] = {
							"autoNum": temp[0],
							"classStyle": classStyle
						};


						if (temp[1] == "0") {
							classStyle = "action1 man-close";
						} else if (temp[1] == "-1") {
							classStyle = "action1";
							temp[1] = "--";
						} else {
							classStyle = "action1";
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