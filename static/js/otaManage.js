(function() {
var adminApp = angular.module('adminApp', ['ui.bootstrap']);

adminApp.controller('otaCtrl', ['$scope', '$http', '$modal', function($scope, $http, $modal) {
	$scope.otas = [];

	function checkId(otas) {
		for (var i = 0; i < otas.length; i++) {
			if (otas[i].id == 13) {
				return true;
			}
		}
		return false;
	}

	function loadAllOtas() {
		var url = "/api/admin/ota/all";
		$http.get(url)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					$scope.otas=resp.result;
					if(!checkId(resp.result)){
						var appOta = {description: "APP特惠",id: 13};
						$scope.otas.push(appOta);
					}
				}
			})
	}

	$scope.readict = function(otaId){
		window.location.href = ("/admin/ota/" + otaId + "/hotels/");
	}
	loadAllOtas();
}])
})()
