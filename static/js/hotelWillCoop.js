(function() {

var hotelWillCoopApp = angular.module('hotelWillCoopApp', []);

hotelWillCoopApp.controller('hotelWillCoopContentCtrl',
	['$scope', '$http', function($scope, $http) {
	
	$scope.citys = [];
	$scope.hotels = [];

	function loadCitys() {
		var url = "/api/city/";
		$http.get(url)
			.success(function(resp) {
				if (resp.errcode == 0) {
					$scope.citys = resp.result.citys;
				}
			})
			.error(function() {
			});
	}


	function loadHotels() {
		var url = '/api/hotel/willcoop/';

		$http.get(url)
			.success(function(resp) {
				if (resp.errcode == 0) {
					$scope.hotels = resp.result.hotels;
				} else {
					alert(resp.errmsg);
				}

			})
			.error(function() {
				alert('酒店列表读取失败');
			});
	}

	$scope.cooprate = function(hotel) {

		var url = '/api/hotel/coop/' + hotel.id;
		$http.post(url)
			.success(function(resp) {
				if (resp.errcode == 0) {
					alert("合作成功");
				} else {
					alert(resp.errmsg);
				}
			})
			.error(function() {
				alert("网络错误");
			});

	}

	loadCitys();
	loadHotels();

	$scope.getCityName = function(cityId) {
		for (var i = 0; i < $scope.citys.length; i++) {
			var city = $scope.citys[i];
			if (city.id == cityId) {
				return city.name;
			}
		}

		return '';
	}
}])
.controller('hotelWillCoopPageIndicatorCtrl',
		['$scope', function($scope) {
	$scope.itemPerPage = 10;
}])





})()
