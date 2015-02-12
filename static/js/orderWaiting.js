(function() {

	var orderWaitingApp = angular.module('orderWaitingApp', ['myApp.directives']);


	orderWaitingApp.config(['$httpProvider', function($httpProvider) {

		if (!$httpProvider.defaults.headers.get) {
			$httpProvider.defaults.headers.get = {};
			// $httpProvider.defaults.headers.post = {};    

		}

		$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	}]);



	orderWaitingApp.controller('orderWaitingCtrl', ['$scope', '$http', function($scope, $http) {


		$scope.orderList = {};
		$scope.refuseReason = "";
		$scope.currentIndex = "";



		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;
		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.messageBox;
		$scope.paginationId = "pageNumber";


		$scope.currentOrder;



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



		$scope.orderPrint = function(m) {

			$scope.currentOrder = m;


			$(".header").hide();
			$(".main-left").hide();
			$("#ng-app").children("div").not($("#printweb")).hide();
			$("#printweb").show();

			setTimeout(function() {
				window.print();

				$("#printweb").hide();
				$(".header").show();
				$(".main-left").show();

				$(".main").show();
				$("#notice").show();
			}, 0);


		}



		$scope.orderDetail = function(m) {

			$scope.currentOrder = $scope.orderList[m];

			$("#hotel-detail").show();

		}


		$scope.closeDetail = function() {
			$("#hotel-detail").hide();

		}



		function dateTimeChecker(a, b, c) {
			var day = new Date();

			day.setFullYear(a);
			day.setMonth(b);
			day.setDate(c);

			var dayTime = day.getTime();
			return dayTime;

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



		$scope.priceDivIn = function(index) {


			$("#orderPrice-" + index).after("<div class='room-info'>取消规则：一经预订不可取消，扣除全额房费.<br />价格类别：普通售价<br />每日价格：<b>09-28</b>170元，<b>09-30</b>180元</div>").show(0, function() {});

		}

		$scope.priceDivOut = function(index) {

			$("#orderPrice-" + index).next("div.room-info").hide(0, function() {
				$("#orderPrice-" + index).next("div.room-info").remove();
			});

		}

		/*$scope.detailDivIn = function(index) {

			var detailDiv = "<div class='classthree'>" +
				"<div style='width:100%;height:30px;text-align:center;font-size:15px'>订单详情</div>" +
				"<div> <span class='classone'>订单确认号：</span>  <span  class='classtwo'>" + "98789855555555555555555555555555555555555" + "</span> </div>" +
				"<div> <span class='classone'>酒店名称：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['hotel_name']) + "</span></div>" +
				"<div> <span class='classone'>房型：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['room_type_name']) + "</span></div>" +
				"<div> <span class='classone'>入离日期：</span>  <span class='classtwo'>" + ($scope.orderList[index]['checkin_date']) + "至" + ($scope.orderList[index]['checkout_date']) + "</span></div>" +
				"<div><span class='classone'>预订时间：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['create_time'].join(" ")) + "</span> </div>" +
				"<div><span class='classone'>入住人：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['hotel_name']) + "</span> </div>" +
				"<div><span class='classone'>联系人：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['contact_name']) + "</span> </div>" +
				"<div><span class='classone'>联系电话：</span>  <span class='classtwo' >" + ($scope.orderList[index]['contact_mobile']) + "</span> </div>" +
				"<div><span class='classone'>取消规则：</span>  <span  class='classtwo'>e" + ($scope.orderList[index]['hotel_name']) + "</span> </div>" +
				"<div><span class='classone'>价格代码名称：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['hotel_name']) + "</span> </div>" +
				"<div><span class='classone'>每日价格：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['everyday_price']) + "</span> </div>" +
				"<div><span class='classone'>总价：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['total_price']) + "</span> </div>" +
				"<div><span class='classone'>备注：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['total_price']) + "</span> </div></div>";

			$("#orderConfimId-" + index).after(detailDiv).show(0, function() {});

		}*/

		/*$scope.detailDivOut = function(index) {

			$("#orderConfimId-" + index).next("div.classthree").hide();

		}*/


		$scope.acceptOrder = function() {

			var url = "/api/order/" + $scope.orderList[$scope.currentIndex]["id"] + "/confirm/";

			//console.log(url);

			$http.post(url)
				.success(function(resp) {
					//	console.log(resp);
					if (resp.errcode == 0) {

						$scope.orderList.splice($scope.currentIndex, 1);
						$("#acceptDialog").hide();

					} else {

						$scope.messageBox = "接受订单失败";
						$("#messageDialog").show();
					}
				})
				.error(function() {

					console.log('network error');


				})

		}

		$scope.refuseOrder = function() {

			if ($.trim($scope.refuseReason) == "" || $scope.refuseReason == undefined) {
				$scope.messageBox = "拒绝理由不能为空";
				return;

			}


			var checkResult = $scope.refuseReason;

			var resultLen = checkResult.replace(/[\u4E00-\u6FA5]/g, "aa").length;

			if (resultLen > 100) {
				$scope.messageBox = "拒绝理由不能超过100字符";
				return;
			}

			$scope.messageBox = " ";



			var url = "/api/order/" + $scope.orderList[$scope.currentIndex]["id"] + "/cancel/";

			//console.log(url);

			$http.post(url, {
					"reason": $scope.refuseReason
				})
				.success(function(resp) {
					//	console.log(resp);
					if (resp.errcode == 0) {

						$scope.orderList.splice($scope.currentIndex, 1);
						$("#refuseDialog").hide();

					} else {

						$scope.messageBox = "拒绝订单失败";
						$("#messageDialog").show();
					}
				})
				.error(function() {

					console.log('network error');

				})

		}


		$scope.acceptShow = function(m) {
			$scope.currentIndex = m;
			$("#acceptDialog").show();
		}
		$scope.acceptHide = function() {
			$("#acceptDialog").hide();
		}
		$scope.refuseShow = function(m) {
			$scope.currentIndex = m;
			$("#refuseDialog").show();
		}
		$scope.refuseHide = function() {
			$("#refuseDialog").hide();
		}


		$scope.confirmResult = function confirmResult() {
			$("#messageDialog").hide();

		}


		$scope.urlCheck = function urlCheck(a) {
			$scope.currentPage = a;
			//console.log("这里是urlCheck url变化的地方");

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/order/waiting/?start=' + pageNum;


			if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}
			$scope.finalUrl = url;

		}



		$scope.searchResult = function searchResult() {

			//var url = "/api/order/waiting/";
			//console.log($scope.finalUrl);

			$http.get($scope.finalUrl)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.orderList = resp.result.orders;

						$scope.total = resp.result.total;
						if ($scope.total != 0) {
							$("#pageInfo").show();
							$("#orderPoint").show();
						} else {
							$("#pageInfo").hide();
						}

						for (var i = 0; i < $scope.orderList.length; i++) {

							var temp = $scope.orderList[i]["customer_info"];

							var tempobj;

							try{

								tempobj = eval(temp);

							}catch(e){

								tempobj=[{"name":" "}];


							}

							
							$scope.orderList[i]["customer_info"] = tempobj;

							$scope.orderList[i]["everyday_price"] = ($scope.orderList[i]["everyday_price"]) / 100;

							$scope.orderList[i]["total_price"] = ($scope.orderList[i]["total_price"]) / 100;

							var temptime = $scope.orderList[i]["create_time"].split(" ");
							$scope.orderList[i]["create_time"] = temptime;

						};

						$scope.itemPerPage = resp.result.limit;

						$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.directiveCtl = true;


					} else {

						console.log(resp.errmsg);

						//$scope.messageBox = resp.errmsg;
						//$("#messageDialog").show();
					}
				})
				.error(function() {

					console.log('network error');
				})

		}

		$(".menu1").find("dd").eq(0).addClass("active");
		$scope.urlCheck(1);
		$scope.searchResult();



	}])



})()