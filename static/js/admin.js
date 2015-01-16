(function() {
var adminApp = angular.module('adminApp', ['ui.bootstrap']);

adminApp.controller('merchantCtrl', ['$scope', '$http', '$modal', function($scope, $http, $modal) {

	$scope.merchants = [];


	function loadMerchants() {
		var url = "/api/admin/merchant/all";
		$http.get(url)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					$scope.merchants = resp.result.merchants;
				}
			})
	}

	$scope.openMerchantModal = function(merchant) {
		var modalInstance = $modal.open({
			templateUrl: 'merchantModal.html',
			controller: 'MerchantModalCtrl',
			size: 'lg',
			resolve: {
				merchant: function() {
					return merchant;
				}
			}
		});

		modalInstance.result.then(function() {
			console.log('close');
			loadMerchants();
		}, function() {
			console.log('dismiss');
		});
	}

	$scope.getMerchantTypeName = function(type) {
		switch(type) {
			case 0:
				return '旅行社';
			case 1:
				return '单体酒店';
			default:
				return '';
		}
	}




	// -- run --
	loadMerchants();
}])

adminApp.controller('MerchantModalCtrl', function($scope, $http, $modalInstance, merchant) {
	$scope.title = merchant ? '修改' : '新建';
	$scope.merchant = angular.copy(merchant) ? merchant : {'type': 1};
	$scope.admin = {};
	$scope.root = {};
	$scope.errmsg = '';

	$scope.ok = function() {
		console.log($scope.merchant);
		console.log($scope.admin);
		console.log($scope.root);
		if (merchant) {
			modifyMerchant();
		} else {
			newMerchant();
		}

	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};

	function modifyMerchant() {
		if (!($scope.merchant.name)) {
			$scope.errmsg = "请填写完整信息";
			return;
		}
		var url = '/api/admin/merchant/modify/';

		var params = {'merchant': $scope.merchant}
		if ($scope.admin.password) {
			params.admin_pwd = hex_md5($scope.admin.password);
		}
		if ($scope.root.password) {
			params.root_pwd = hex_md5($scope.root.password);
		}

		$http.put(url, params)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					$modalInstance.close();
				} else {
					$scope.errmsg = resp.errmsg;
				}
			})
			.error(function() {
				$scope.errmsg = '修改失败 请联系管理员';
			});

	}

	function newMerchant() {
		if (!($scope.merchant.name && $scope.merchant && $scope.admin.password && $scope.root.password)) {
			$scope.errmsg = "请填写完整信息";
			return;
		}

		var url = '/api/admin/merchant/modify/';

		var params = {'merchant': $scope.merchant,
		   	'admin_pwd': hex_md5($scope.admin.password),
		   	'root_pwd': hex_md5($scope.root.password)};

		$http.post(url, params)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					$modalInstance.close();
				} else {
					$scope.errmsg = resp.errmsg;
				}
			})
			.error(function() {
				$scope.errmsg = '新建失败 请联系管理员';
			});
	}
});


})()
