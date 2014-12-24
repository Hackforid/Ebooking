(function() {

	var orderListApp = angular.module('orderListApp', []);
	orderListApp.controller('orderListCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.todayBook = {};
		$scope.todayCheckIn = {};



		function initBook() {

			var url = "/api/order/todaybook";

			console.log(url);
			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.todayBook = resp.result.orders;

						console.log($scope.todayBook);
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
					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}

		function initCheckin() {

			var url = "/api/order/todaycheckin";

			console.log(url);
			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.todayCheckIn = resp.result.orders;

						for (var i = 0; i < $scope.todayCheckIn.length; i++) {

							var temp = $scope.todayCheckIn[i]["customer_info"];
							var tempobj = eval(temp);
							$scope.todayCheckIn[i]["customer_info"] = tempobj;
							$scope.todayCheckIn[i]["everyday_price"] = ($scope.todayCheckIn[i]["everyday_price"]) / 100;
							var temptime = $scope.todayCheckIn[i]["create_time"].split(" ");
							$scope.todayCheckIn[i]["create_time"] = temptime;
						};
					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}

		initBook();
		initCheckin();

	}])



})()