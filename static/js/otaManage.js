(function() {
var adminApp = angular.module('adminApp', ['ui.bootstrap']);

adminApp.controller('otaCtrl', ['$scope', '$http', '$modal', function($scope, $http, $modal) {
	$scope.otas = [];
	function loadAllOtas() {
		var url = "/api/admin/ota/all";
		$http.get(url)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					$scope.otas=resp.result;
				}
			})
	}
	$scope.readict = function(otaId){
		window.location.href = ("/admin/ota/" + otaId + "/hotels/");
	}
	loadAllOtas();
}])
})()
