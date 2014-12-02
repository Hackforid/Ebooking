(function() {

var loginApp = angular.module('LoginApp', []);

loginApp.controller('LoginCtrl', ['$scope', '$http', 
	function($scope, $http) {

	$scope.merchantId = null;
	$scope.username = null;
	$scope.password = null;
	$scope.errMsg = null;

	$scope.login = function() {
		var url = "/login/";
		var params = {
			'merchant_id': $scope.merchantId,
			'username': $scope.username,
			'password': $scope.password};
		$http.post(url, params)
			.success(function(resp) {
				if (resp.errcode == 0) {
					alert('login success');
				} else {
					$scope.errMsg = resp.errmsg;
				}
			})
			.error(function() {
				$scope.errMsg = '网络异常';
			});
	}
}]);



})()
