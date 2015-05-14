(function() {
	var contractApp = angular.module('contractApp', []);
	contractApp.controller('contractCtrl', ['$scope', '$http', function($scope, $http) {
		$scope.payTypeContract = false;
		$scope.hotelName;
		$scope.currentSaveFlag = 1; /*1 新增 0 修改*/
		$scope.hotelInfo = {
			"receptionist_phone": "",
			"fax": "",
			"margin": "",
			"business1_name": "",
			"business1_tel": "",
			"business2_name": "",
			"business2_tel": "",
			"finance_name": "",
			"finance_tel": "",
			"commission": "",
			"settle_cycle": "",
			"settle_date": "",
			"cooperation_mode": "",
			"account_name": "",
			"finance_qq": "",
			"settle_order_method": "",
			"account_bank_name": "",
			"account_bank_id": ""
		};

		function loadContracts() {
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						console.log(resp);
						var contractHotel = resp.result.contract_hotel;
						$scope.hotelName = resp.result.hotel.base_hotel['name'];
						if (isEmptyObject(contractHotel)) {
							payTypeContract = false;
							$scope.currentSaveFlag = 1;
						} else {
							payTypeContract = true;
							$scope.currentSaveFlag = 0;
							$scope.hotelInfo = resp.result.hotel.base_hotel;
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

		$scope.saveContract = function() {
			console.log($scope.hotelInfo);

			if ($.trim($scope.hotelInfo.fax) == "") {
				$scope.errMessage = "传真不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.margin) == "") {
				$scope.errMessage = "保证金额不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.business1_name) == "") {
				$scope.errMessage = "业务联系人1不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.business1_tel) == "") {
				$scope.errMessage = "电话1不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.business2_name) == "") {
				$scope.errMessage = "业务联系人2不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.business2_tel) == "") {
				$scope.errMessage = "电话2不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.finance_name) == "") {
				$scope.errMessage = "财务联系人不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.finance_tel) == "") {
				$scope.errMessage = "联系电话不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.commission) == "") {
				$scope.errMessage = "佣金不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.settle_cycle) == "") {
				$scope.errMessage = "结算周期不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.settle_date) == "") {
				$scope.errMessage = "对账时间不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.cooperation_mode) == "") {
				$scope.errMessage = "合作模式不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.account_name) == "") {
				$scope.errMessage = "开户名称不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.finance_qq) == "") {
				$scope.errMessage = "QQ不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.settle_order_method) == "") {
				$scope.errMessage = "结算订单日期不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.account_bank_name) == "") {
				$scope.errMessage = "开户行不能为空";
				return;
			}
			if ($.trim($scope.hotelInfo.account_bank_id) == "") {
				$scope.errMessage = "账号不能为空";
				return;
			}
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			var obj={
				"contract_hotel":$scope.hotelInfo
			};
			if ($scope.currentSaveFlag == 1) {
				$http.post(url, obj)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							
						}
					});

			} else {
				$http.put(url, obj)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							
						}
					});
			}
		}
		loadContracts();
	}])
})()