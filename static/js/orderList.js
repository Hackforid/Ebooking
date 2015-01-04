(function() {

	var orderListApp = angular.module('orderListApp', ['myApp.directives']);
	orderListApp.controller('orderListBookCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.todayBook = {};
		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;
		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.paginationId = "pagebookNumber";


		$scope.urlCheck = function urlCheck(a) {
			$scope.currentPage = a;

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/order/todaybook/?start=' + pageNum;

			if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}
			$scope.finalUrl = url;

		}

		$scope.searchResult = function searchResult() {

			//console.log($scope.finalUrl);
			$http.get($scope.finalUrl)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.todayBook = resp.result.orders;

						$scope.total = resp.result.total;
						if ($scope.total != 0) {
							$("#pagebookInfo").show();
						} else {
							$("#pagebookInfo").hide();
						}

						var todayBookLength = $scope.todayBook.length;

						for (var i = 0; i < $scope.todayBook.length; i++) {

							/*过滤状态为200的*/
							var bookStatus = $scope.todayBook[i]["status"];
							if (bookStatus == "200") {
								$scope.todayBook.splice(i, 1);
								i--;
								continue;
							}
							/*过滤状态为200的*/
							else {

								var temp = $scope.todayBook[i]["customer_info"];
								var tempobj = eval(temp);
								$scope.todayBook[i]["customer_info"] = tempobj;
								$scope.todayBook[i]["everyday_price"] = ($scope.todayBook[i]["everyday_price"]) / 100;
								var temptime = $scope.todayBook[i]["create_time"].split(" ");
								$scope.todayBook[i]["create_time"] = temptime;


								if (bookStatus == "100") {

									$scope.todayBook[i]["status"] = "待确定";

								} else if (bookStatus == "300") {

									$scope.todayBook[i]["status"] = "接受";

								} else if (bookStatus == "400") {

									$scope.todayBook[i]["status"] = "拒绝";

								} else if (bookStatus == "500" || bookStatus == "600") {

									$scope.todayBook[i]["status"] = "服务器取消";

								}

							}

						};

						$scope.itemPerPage = resp.result.limit;

						$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.directiveCtl = true;

					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}

		$scope.urlCheck(1);
		$scope.searchResult();
		$(".menu1").find("dd").eq(1).addClass("active");


	}])


	orderListApp.controller('orderListCheckCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.todayCheckIn = {};

		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;
		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.paginationId = "pagecheckNumber";


		$scope.urlCheck = function urlCheck(a) {
			$scope.currentPage = a;

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/order/todaycheckin/?start=' + pageNum;

			if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}
			$scope.finalUrl = url;

		}

		$scope.searchResult = function searchResult() {

			//console.log($scope.finalUrl);
			$http.get($scope.finalUrl)
				.success(function(resp) {
					//console.log(resp);
					if (resp.errcode == 0) {
						$scope.todayCheckIn = resp.result.orders;

						$scope.total = resp.result.total;

						if ($scope.total != 0) {
							$("#pagecheckInfo").show();
						} else {
							$("#pagecheckInfo").hide();
						}

						/*for (var i = 0; i < $scope.todayCheckIn.length; i++) {

							var temp = $scope.todayCheckIn[i]["customer_info"];
							var tempobj = eval(temp);
							$scope.todayCheckIn[i]["customer_info"] = tempobj;
							$scope.todayCheckIn[i]["everyday_price"] = ($scope.todayCheckIn[i]["everyday_price"]) / 100;
							var temptime = $scope.todayCheckIn[i]["create_time"].split(" ");
							$scope.todayCheckIn[i]["create_time"] = temptime;
						};*/

						for (var i = 0; i < $scope.todayCheckIn.length; i++) {

							/*过滤状态为200的*/
							var checkStatus = $scope.todayCheckIn[i]["status"];
							if (checkStatus == "200") {
								$scope.todayCheckIn.splice(i, 1);
								i--;
								continue;
							}
							/*过滤状态为200的*/
							else {

								var temp = $scope.todayCheckIn[i]["customer_info"];
								var tempobj = eval(temp);
								$scope.todayCheckIn[i]["customer_info"] = tempobj;
								$scope.todayCheckIn[i]["everyday_price"] = ($scope.todayCheckIn[i]["everyday_price"]) / 100;
								var temptime = $scope.todayCheckIn[i]["create_time"].split(" ");
								$scope.todayCheckIn[i]["create_time"] = temptime;


								if (checkStatus == "100") {

									$scope.todayCheckIn[i]["status"] = "待确定";

								} else if (checkStatus == "300") {

									$scope.todayCheckIn[i]["status"] = "接受";

								} else if (checkStatus == "400") {

									$scope.todayCheckIn[i]["status"] = "拒绝";

								} else if (checkStatus == "500" || bookStatus == "600") {

									$scope.todayCheckIn[i]["status"] = "服务器取消";

								}

							}

						};

						$scope.itemPerPage = resp.result.limit;

						$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.directiveCtl = true;


					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}

		$scope.urlCheck(1);
		$scope.searchResult();


	}])



	orderListApp.controller('orderListQueryCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.queryList = {};
		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;
		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.paginationId = "pagequeryNumber";


		$scope.searchOrderId = "";
		$scope.searchHotelName = "";
		$scope.searchInPeople = "";
		$scope.searchStatus = "";
		$scope.messageLive = "";
		$scope.messageList = "";



		$scope.conditionReset = function conditionReset() {

			$scope.searchOrderId = "";
			$scope.searchHotelName = "";
			$scope.searchInPeople = "";
			$scope.searchStatus = "";
			$("#liveStarTime").val("");
			$("#liveEndTime").val("");
			$("#ListStarTime").val("");
			$("#ListEndTime").val("");
		}


		$scope.urlCheck = function urlCheck(a) {

			$scope.currentPage = a;
			var liveStarTime = $("#liveStarTime").val();
			var liveEndTime = $("#liveEndTime").val();
			var ListStarTime = $("#ListStarTime").val();
			var ListEndTime = $("#ListEndTime").val();
			$scope.messageLive = "";
			$scope.messageList = "";

			if (liveStarTime > liveEndTime) {
				$scope.messageLive = "起始日期大于结束日期";
				return;
			}
			if (ListStarTime > ListEndTime) {
				$scope.messageList = "起始日期大于结束日期";
				return;
			}

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/order/search/?start=' + pageNum;

			if ($.trim($scope.searchOrderId) != "" && $scope.searchOrderId != undefined) {
				url = url + "&order_id=" + $scope.searchOrderId;

			}

			if ($.trim($scope.searchHotelName) != "" && $scope.searchHotelName != undefined) {
				url = url + "&hotel_name=" + $scope.searchHotelName;

			}

			if ($.trim(liveStarTime) != "" && liveStarTime != undefined) {
				url = url + "&checkin_date=" + liveStarTime;

			}

			if ($.trim(liveEndTime) != "" && liveEndTime != undefined) {
				url = url + "&checkout_date=" + liveEndTime;

			}

			if ($.trim($scope.searchInPeople) != "" && $scope.searchInPeople != undefined) {
				url = url + "&customer=" + $scope.searchInPeople;

			}

			if ($.trim($scope.searchStatus) != "" && $scope.searchStatus != undefined) {

				if ($scope.searchStatus == "500") {
					url = url + "&order_status=" + $scope.searchStatus + "&order_status=600";
				} else {
					url = url + "&order_status=" + $scope.searchStatus;
				}

			}

			if ($.trim(ListStarTime) != "" && ListStarTime != undefined) {
				url = url + "&create_time_start=" + ListStarTime;

			}
			if ($.trim(ListEndTime) != "" && ListEndTime != undefined) {
				url = url + "&create_time_end=" + ListEndTime;

			}
			if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}

			$scope.finalUrl = encodeURI(url);


		}

		$scope.searchResult = function searchResult() {

			//console.log($scope.finalUrl);
			$http.get($scope.finalUrl)
				.success(function(resp) {
					//console.log(resp);
					if (resp.errcode == 0) {
						$scope.queryList = resp.result.orders;

						$scope.total = resp.result.total;
						if ($scope.total != 0) {
							$("#pagequeryInfo").show();
						} else {
							$("#pagequeryInfo").hide();
						}

						for (var i = 0; i < $scope.queryList.length; i++) {

							var queryStatus = $scope.queryList[i]["status"];
							if (queryStatus == "200") {
								$scope.queryList.splice(i, 1);
								i--;
								continue;
							} else {

								var temp = $scope.queryList[i]["customer_info"];
								var tempobj = eval(temp);
								$scope.queryList[i]["customer_info"] = tempobj;
								$scope.queryList[i]["everyday_price"] = ($scope.queryList[i]["everyday_price"]) / 100;
								var temptime = $scope.queryList[i]["create_time"].split(" ");
								$scope.queryList[i]["create_time"] = temptime;


								if (queryStatus == "100") {

									$scope.queryList[i]["status"] = "待确定";

								} else if (queryStatus == "300") {

									$scope.queryList[i]["status"] = "接受";

								} else if (queryStatus == "400") {

									$scope.queryList[i]["status"] = "拒绝";

								} else if (queryStatus == "500" || bookStatus == "600") {

									$scope.queryList[i]["status"] = "服务器取消";

								}

							}

						};

						$scope.itemPerPage = resp.result.limit;

						$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.directiveCtl = true;

					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}

		$scope.urlCheck(1);
		$scope.searchResult();
		$(".menu1").find("dd").eq(1).addClass("active");


	}])



})()