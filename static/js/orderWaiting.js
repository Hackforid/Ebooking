(function() {

	var orderWaitingApp = angular.module('orderWaitingApp', ['myApp.directives']);
	orderWaitingApp.controller('orderWaitingCtrl', ['$scope', '$http', function($scope, $http) {


		$scope.orderList = {};
		$scope.refuseReson = "";
		$scope.currentIndex = "";



		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;
		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.messageBox;
		$scope.paginationId = "pageNumber";



		$scope.priceDivIn = function(index) {


			$("#orderPrice-" + index).after("<div class='room-info'>取消规则：一经预订不可取消，扣除全额房费.<br />价格类别：普通售价<br />每日价格：<b>09-28</b>170元，<b>09-30</b>180元</div>").show(0, function() {});

		}

		$scope.priceDivOut = function(index) {

			$("#orderPrice-" + index).next("div.room-info").hide(0, function() {
				$("#orderPrice-" + index).next("div.room-info").remove();
			});

		}

		$scope.detailDivIn = function(index) {

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

		}

		$scope.detailDivOut = function(index) {

			$("#orderConfimId-" + index).next("div.classthree").hide();

		}


		$scope.acceptOrder = function() {

			var url = "/api/order/" + $scope.orderList[$scope.currentIndex]["id"] + "/confirm/";

			console.log(url);

			$http.post(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$scope.orderList.splice($scope.currentIndex, 1);
						$("#acceptDialog").hide();

					} else {

						$scope.messageBox = resp.errmsg;
						$("#messageDialog").show();
					}
				})
				.error(function() {

					$scope.messageBox = 'network error';
					$("#messageDialog").show();

				})

		}

		$scope.refuseOrder = function() {

			if ($scope.refuseReson.trim() == "" || $scope.refuseReson == undefined) {
				alert("不能为空");
				return;

			}

			var url = "/api/order/" + $scope.orderList[$scope.currentIndex]["id"] + "/cancel/";

			console.log(url);

			$http.post(url, {
					"reason": $scope.refuseReson
				})
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

						$scope.orderList.splice($scope.currentIndex, 1);
						$("#refuseDialog").hide();

					} else {

						$scope.messageBox = resp.errmsg;
						$("#messageDialog").show();
					}
				})
				.error(function() {

					$scope.messageBox = 'network error';
					$("#messageDialog").show();

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


			if ($scope.itemPerPage.trim() != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}
			$scope.finalUrl = url;

		}



		$scope.searchResult = function searchResult() {

			//var url = "/api/order/waiting/";
			console.log($scope.finalUrl);

			$http.get($scope.finalUrl)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.orderList = resp.result.orders;

						$scope.total = resp.result.total;
						if ($scope.total == 0) {
							$("#pageInfo").hide();
						}

						for (var i = 0; i < $scope.orderList.length; i++) {

							var temp = $scope.orderList[i]["customer_info"];
							var tempobj = eval(temp);
							$scope.orderList[i]["customer_info"] = tempobj;

							$scope.orderList[i]["everyday_price"] = ($scope.orderList[i]["everyday_price"]) / 100;

							var temptime = $scope.orderList[i]["create_time"].split(" ");
							$scope.orderList[i]["create_time"] = temptime;

						};

						$scope.itemPerPage = resp.result.limit;
						
						$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.directiveCtl = true;


					} else {

						$scope.messageBox = resp.errmsg;
						$("#messageDialog").show();
					}
				})
				.error(function() {

					$scope.messageBox = 'network error';
					$("#messageDialog").show();
				})

		}

		$(".menu1").find("dd").eq(0).addClass("active");
		$scope.urlCheck(1);
		$scope.searchResult();



	}])



})()