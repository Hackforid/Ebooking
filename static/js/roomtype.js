(function() {

var ratePlanApp = angular.module('ratePlanApp', []);

var NewRatePlanDialog = function(scope, http) {
	this.scope = scope;
	this.http = http;

	this.name = '';
	this.mealType = 0;
	this.punishType = 0;

	this.errmsg = '';

	this.open = function() {
		this.name = '';
		this.mealType = 0;
		this.punishType = 0;
		this.errmsg = '';
		$("#newRatePlanDialog").fadeIn(500);
	}
	this.close = function() {
		$("#newRatePlanDialog").fadeOut(500);
	}
	this.save = function() {
		if (!this.name) {
			this.errmsg = '请输入有效名称';
			return;
		}

		this.errmsg = '';
		console.log(this.name + this.mealType + this.punishType);

		var url = '/api/hotel/' + hotelId + '/roomtype/' + scope.currentRoomType.id + '/rateplan/';
		console.log(url);
		var params = {'name': this.name, 'meal_type': this.mealType, 'punish_type': this.punishType};
		console.log(params);
		http.post(url, params)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
				} else {
					this.errmsg = resp.errmsg;
				}
			})
			.error(function() {
				this.errmsg = '网络错误';
			})
	}

}

ratePlanApp.controller('ratePlanCtrl',
	['$scope', '$http', function($scope, $http) {

	$scope.roomtypes = [];
	$scope.hotel = {};
	$scope.newRatePlanDialog = new NewRatePlanDialog($scope, $http);
	$scope.currentRoomType = {};
	$scope.rateplans = {};
	$scope.roomrates = {};

	function loadRoomTypes(_hotelId) {
		var url = "/api/hotel/" + _hotelId + "/roomtype/?simple=1";
		$http.get(url)
			.success(function(resp) {
				console.log(resp)
				if (resp.errcode == 0) {
					$scope.hotel = resp.result.hotel;
					$scope.roomtypes = resp.result.cooped_roomtypes;
					if ($scope.roomtypes.length > 0) {
						$scope.currentRoomType = $scope.roomtypes[0];
					}
				} else {
					alert(resp.errmsg);
				}
			})
			.error(function() {
				alert('network error');
			})
	}

	loadRoomTypes(hotelId);


	$scope.$watch('currentRoomType', function() {
		if (!$scope.currentRoomType.id) {
			return;
		}
		var url = '/api/hotel/' + hotelId + '/roomtype/' + $scope.currentRoomType.id + '/rateplan/';
		console.log(url);

		$http.get(url)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					$scope.rateplans = resp.result.rateplans;
					$scope.roomrates = resp.result.roomrates;
				}
			})
			.error(function() {
			})
	});


}])


})()
