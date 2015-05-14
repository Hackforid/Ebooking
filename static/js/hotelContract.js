(function() {
	var contractApp = angular.module('contractApp', []);
	contractApp.controller('contractCtrl', ['$scope', '$http', function($scope, $http) {
		function loadContracts() {
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						var contractHotel = resp.result.contract_hotel;
						if (isEmptyObject(contractHotel)) {
							$("#payTypeContract").hide();
						} else {
							$("#payTypeContract").show();
						}
					}
				});
		}

		function isEmptyObject(obj) {
			for (var n in obj) {
				return false;
			}
			return true;
		}
		loadContracts();
	}])
})()