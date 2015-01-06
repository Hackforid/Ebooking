(function() {

	var hotelCoopApp = angular.module('hotelCoopedApp', ['myApp.directives', 'ui.bootstrap']);


	hotelCoopApp.config(['$httpProvider', function($httpProvider) {

		if (!$httpProvider.defaults.headers.get) {
			$httpProvider.defaults.headers.get = {};
			// $httpProvider.defaults.headers.post = {};    

		}

		$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	}]);



	hotelCoopApp.controller('hotelCoopedContentCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.citys = [];
		$scope.hotels = [];


		$scope.citysName = [];


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



		$scope.currentHotel;


		$scope.hotelDetail = function(m) {

			$scope.currentHotel = $scope.hotels[m];
			//console.log($scope.currentHotel);
			$("#hotel-detail").show();

		}

		$scope.closeHotelDetail = function() {
			$("#hotel-detail").hide();

		}


		$scope.getStatus = function(s) {
			if (s == "1") {
				return "正常";
			} else if (s == "0") {
				return "暂停";
			}
		}


		$scope.getHotelStar = function(m) {
			if (m == "0") {
				return "无";
			} else if (m == "1") {
				return "一星级";
			} else if (m == "2") {
				return "二星级";
			} else if (m == "3") {
				return "三星级";
			} else if (m == "4") {
				return "四星级";
			} else if (m == "5") {
				return "五星级";
			}

		}

		function loadCitys() {
			var url = "/api/city/";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						$scope.citys = resp.result.citys;

						for (var i = 0; i < $scope.citys.length; i++) {
							$scope.citysName.push($scope.citys[i]['name']);
						};


					}
				})
				.error(function() {});
		}


		$scope.conditionReset = function conditionReset() {
			$scope.searchName = "";
			$scope.searchStatus = "";
			//$scope.searchCity = "";
			$("#searchCity").val("");
			$scope.searchStar = "";

			$scope.finalUrl = '/api/hotel/cooped/?start=0&limit=' + $scope.itemPerPage;
			$scope.searchResult();
		}


		$scope.confirmResult = function confirmResult() {
			$("#acceptDialog").hide();

		}


		$scope.urlCheck = function urlCheck(a) {

			$scope.currentPage = a;
			$scope.searchCity = $("#searchCity").val();
			//console.log("这里是urlCheck url变化的地方");

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/hotel/cooped/?start=' + pageNum;

			if ($.trim($scope.searchName) != "" && $scope.searchName != undefined) {
				url = url + "&name=" + $scope.searchName;

			}
			if ($.trim($scope.searchCity) != "" && $scope.searchCity != undefined) {
				var cityId = getCityId($scope.searchCity);

				if (cityId == false) {
					$("#pageInfo").hide();
					$scope.hotels = [];
					return;
				}


				url = url + "&city_id=" + cityId;

			}
			if ($.trim($scope.searchStar) != "" && $scope.searchStar != undefined && $scope.searchStar != "0") {
				url = url + "&star=" + $scope.searchStar;

			}

			if ($.trim($scope.searchStatus) != "" && $scope.searchStatus != undefined && $scope.searchStatus != "0") {
				url = url + "&status=" + $scope.searchStatus;

			}
			if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}


			$scope.finalUrl = encodeURI(url);
			//console.log($scope.finalUrl);

		}



		$scope.searchResult = function searchResult() {

			$http.get($scope.finalUrl)
				.success(function(resp) {
					if (resp.errcode == 0) {
						//console.log(resp);
						$scope.hotels = resp.result.hotels;

						$scope.itemPerPage = resp.result.limit;
						$scope.total = resp.result.total;


						if ($scope.total != 0) {
							$("#pageInfo").show();
						} else {
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

			return false;
		}

		$scope.redictToInventoryPage = function(hotel) {
			window.location.href = ("/hotel/cooped/" + hotel.id + "/inventory/");
		}
	}])

})()