(function() {

	var hotelCoopApp = angular.module('hotelCoopedApp', ['myApp.directives']);

	hotelCoopApp.controller('hotelCoopedContentCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.citys = [];
		$scope.hotels = [];

		$scope.searchName = "";
		$scope.searchStatus = "";
		$scope.searchCity = "";
		$scope.searchStar = "";
		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;

		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.paginationId = "pageNumber";
		$scope.messageBox;



		function loadCitys() {
			var url = "/api/city/";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						$scope.citys = resp.result.citys;
					}
				})
				.error(function() {});
		}


		$scope.conditionReset = function conditionReset() {
			$scope.searchName = "";
			$scope.searchStatus = "";
			$scope.searchCity = "";
			$scope.searchStar = "";
		}


		$scope.confirmResult = function confirmResult() {
			$("#acceptDialog").hide();

		}


		$scope.urlCheck = function urlCheck(a) {

			$scope.currentPage = a;
			//console.log("这里是urlCheck url变化的地方");

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/hotel/cooped/?start=' + pageNum;

			if ($scope.searchName.trim() != "" && $scope.searchName != undefined) {
				url = url + "&name=" + $scope.searchName;

			}
			if ($scope.searchCity.trim() != "" && $scope.searchCity != undefined) {
				var cityId = getCityId($scope.searchCity);
				url = url + "&city_id=" + cityId;

			}
			if ($scope.searchStar.trim() != "" && $scope.searchStar != undefined) {
				url = url + "&star=" + $scope.searchStar;

			}

			if ($scope.searchStatus.trim() != "" && $scope.searchStatus != undefined) {
				url = url + "&status=" + $scope.searchStatus;

			}
			if ($scope.itemPerPage.trim() != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}


			$scope.finalUrl = url;

		}



		$scope.searchResult = function searchResult() {

			$http.get($scope.finalUrl)
				.success(function(resp) {
					if (resp.errcode == 0) {
						console.log(resp);
						$scope.hotels = resp.result.hotels;

						$scope.itemPerPage = resp.result.limit;
						$scope.total = resp.result.total;

						if ($scope.total == 0) {
							$("#pageInfo").hide();
						}


						$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.directiveCtl = true;


					} else {

						$scope.messageBox = resp.errmsg;
						$("#acceptDialog").show();

					}

				})
				.error(function() {

					$scope.messageBox = "酒店列表读取失败";
					$("#acceptDialog").show();


				});


		}


		function init() {
			$(".menu2").find("dd").eq(0).addClass("active");

			loadCitys();

			$scope.urlCheck($scope.currentPage);

			$scope.searchResult();


		}

		init();


		$scope.getCityName = function(cityId) {
			for (var i = 0; i < $scope.citys.length; i++) {
				var city = $scope.citys[i];
				if (city.id == cityId) {
					return city.name;
				}
			}

			return '';
		}

		function getCityId(cityName) {
			for (var i = 0; i < $scope.citys.length; i++) {
				var city = $scope.citys[i];
				if (city.name == cityName) {
					return city.id;
				}
			}

			return ' ';
		}

		$scope.redictToInventoryPage = function(hotel) {
			window.location.href = ("/hotel/cooped/" + hotel.id + "/inventory/");
		}
	}])

})()