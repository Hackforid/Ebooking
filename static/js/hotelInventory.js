(function() {

var hotelInventoryApp = angular.module('hotelInventoryApp', []);

$("#roomtype-list .action input").click( function() {
    $("#roomtype-list").fadeOut(500);
});

hotelInventoryApp.controller('hotelInventoryCtrl',
	['$scope', '$http', function($scope, $http) {

	$scope.hotel = {};
	$scope.willCoop = [];
	$scope.cooped = [];
	$scope.selecableMonths = [1,2,3];
	$scope.currentMonth = undefined;


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

		var url = "/api/hotel/" + hotelId + "/roomtype/?m=" + $scope.currentMonth.m;
		$http.post(url, {'roomtype_ids': shouldCooped})
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					// Todo loading anime
					loadHotelMsg(hotelId);
				} else {
					console.log(resp.errmsg);
				}
			})
			.error(function() {
				alert('network error');
			})
	}

	// -----------------------------




	function initMonthWatch() {
		$scope.$watch('currentMonth', function() {
			if ($scope.currentMonth.m == undefined) {
				return;
			}
			loadHotelMsg(hotelId);
		});
	}


	function loadHotelMsg(hotel_id) {
		var url = "/api/hotel/" + hotel_id + "/roomtype/?m=" + $scope.currentMonth.m;
		console.log(url);
		$http.get(url)
			.success(function(resp) {
				console.log(resp)
				if (resp.errcode == 0) {
					$scope.hotel = resp.result.hotel;
					$scope.willCoop = resp.result.will_coop_roomtypes;
					$scope.cooped = resp.result.cooped_roomtypes;
				} else {
					alert(resp.errmsg);
				}
			})
			.error(function() {
				alert('network error');
			})
	}

	function computeSelecableDate() {
		var date = new Date();
		var month0 = date.getMonth() + 1;
		var month1 = month0 + 1 > 12 ? 1 : month0 + 1;
		var month2 = month1 + 1 > 12 ? 1 : month1 + 1;

		$scope.selecableMonths = [{'m': 0, 'name': month0 + '月'},
			{'m':1, 'name':month1 + '月'} , {'m':2, 'name':month2 + '月'}];
		$scope.currentMonth = $scope.selecableMonths[0];
	}

	function init() {
		computeSelecableDate();
		initMonthWatch();
	}

	init();

}])


})()
