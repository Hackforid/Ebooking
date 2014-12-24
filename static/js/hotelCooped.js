(function() {

var hotelCoopApp = angular.module('hotelCoopedApp', []);

hotelCoopApp.controller('hotelCoopedContentCtrl',
	['$scope', '$http', function($scope, $http) {
	
	$scope.citys = [];
	$scope.hotels = [];



	$scope.serchName="";$scope.serchStatus="";
	$scope.serchCity="";
	$scope.serchStar="";
	$scope.itemPerPage = 10;
	$scope.currentPage;
	$scope.total;



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
		var url = '/api/hotel/cooped/';

		$http.get(url)
			.success(function(resp) {
				console.log(resp)
				console.log(resp);
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

	/*$scope.cooprate = function(hotel) {


	}*/



	$scope.searchHotel=function(){

	console.log($scope.serchName);
	console.log($scope.serchCity);
	console.log($scope.serchStar);
	console.log($scope.itemPerPage); //$scope.currentPage;
	console.log($scope.serchStatus);
	var url = '/api/hotel/cooped/?start=0';

	if($scope.serchName.trim()!="" && $scope.serchName!=undefined){
		url=url+"&name="+$scope.serchName;

	}
	if($scope.serchCity.trim()!="" && $scope.serchCity!=undefined){

		var cityId=getCityId($scope.serchCity);

   		url=url+"&city_id="+cityId;
 	
	}
	if($scope.serchStar.trim()!="" && $scope.serchStar!=undefined){
		url=url+"&star="+$scope.serchStar;

	}

	/*if($scope.serchStatus.trim()!="" && $scope.serchStatus!=undefined){
		url=url+"&status="+$scope.serchStatus;

	}*/
	if($scope.serchStatus.trim()!="" && $scope.serchStatus!=undefined){
		url=url+"&status="+$scope.serchStatus;

	}




	console.log(url);
	//url='/api/hotel/willcoop/?star=1&city_id';

	$http.get(url)
			.success(function(resp) {
				if (resp.errcode == 0) {
					console.log(resp);
					$scope.hotels = resp.result.hotels;
				} else {
					alert(resp.errmsg);
				}

			})
			.error(function() {
				alert('酒店列表读取失败');
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


	function getCityId (cityName) {
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
