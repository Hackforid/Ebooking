(function() {
	var adminHotelsApp = angular.module('adminHotelsApp', ['ui.bootstrap', 'ngSanitize', 'ui.select']);
	adminHotelsApp.directive('ngEnter', function() {
		return function(scope, element, attrs) {
			element.bind("keydown keypress", function(event) {
				if (event.which === 13) {
					scope.$apply(function() {
						scope.$eval(attrs.ngEnter);
					});
					event.preventDefault();
				}
			});
		};
	});
	adminHotelsApp.filter('propsFilter', function() {
		return function(items, props) {
			var out = [];
			if (angular.isArray(items)) {
				items.forEach(function(item) {
					var itemMatches = false;
					var keys = Object.keys(props);
					for (var i = 0; i < keys.length; i++) {
						var prop = keys[i];
						var text = props[prop].toLowerCase();
						if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
							itemMatches = true;
							break;
						}
					}
					if (itemMatches) {
						out.push(item);
					}
				});
			} else {
				out = items;
			}
			return out;
		};
	});

	adminHotelsApp.controller('adminHotelsCtrl', ['$scope', '$http', '$rootScope', '$modal', '$timeout', function($scope, $http, $rootScope, $modal, $timeout) {

		$scope.citys = [];
		$scope.hotels = [];
		$scope.citysName = [];
		$scope.searchName = "";
		$scope.searchCity = "";
		$scope.searchStar = 0;
		$scope.searchMerchant = [];
		$scope.currentOtaName = "";
		$scope.finalUrl;
		$scope.currentHotel;
		$scope.currentHotelIndex;
		$scope.changeDistrictName = {};
		$scope.currentRoomtypes;
		$scope.currentHotelId;
		$scope.checkedItem = [false, false, false];
		$scope.checktest = function(item) {
			$scope.checkedItem[item] = ($scope.checkedItem[item] == false ? true : false);
			if (item == 0) {
				if ($scope.checkedItem[0] == false) {
					$scope.checkedItem[1] = false;
					$scope.checkedItem[2] = false;
				} else if ($scope.checkedItem[0] == true) {
					$scope.checkedItem[1] = true;
					$scope.checkedItem[2] = true;
				}
			}
			if (($scope.checkedItem[1] == true) && ($scope.checkedItem[2] == true)) {
				$scope.checkedItem[0] = true;
			}
			if (($scope.checkedItem[1] == false) || ($scope.checkedItem[2] == false)) {
				$scope.checkedItem[0] = false;
			}
		}

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
						$scope.otas = resp.result;
						if(!checkId(resp.result)){
							var appOta = {description: "APP特惠",id: 13,isOnline: 1};
							$scope.otas.push(appOta);
						}
						for (var i = 0; i < $scope.otas.length; i++) {
							if ($scope.otas[i].id == ota_id) {
								$scope.currentOtaName = $scope.otas[i].description;
							}
						};
					}
				})
		}

		$scope.modifyStatus = function(hotel) {
			var currentOtaIds = angular.copy($scope.otas);
			var currentHotelOtaIds = hotel.ota_ids;
			for (var i = 0; i < currentHotelOtaIds.length; i++) {
				for (var j = 0; j < currentOtaIds.length; j++) {
					if (currentOtaIds[j].id == currentHotelOtaIds[i]) {
						currentOtaIds[j]['checked'] = true;
					}
				};
			};
			var modalInstance = $modal.open({
				templateUrl: 'onlinestatus.html',
				controller: 'onLineStatus',
				size: 'lg',
				resolve: {
					otas: function() {
						return currentOtaIds;
					},
					hotelId: function() {
						return (hotel.id);
					}
				}
			});
			modalInstance.result.then(function() {}, function() {});
		}

		$scope.confirmStatus = function(hotelId, status, onlineOta) {
			var modalInstance = $modal.open({
				templateUrl: 'confirmLineManage.html',
				controller: 'confirmLineManage',
				size: 'sm',
				resolve: {
					status: function() {
						return status;
					},
					hotelId: function() {
						return (hotelId);
					},
					otaId: function() {
						return ota_id;
					},
					currentOtaName: function() {
						return $scope.currentOtaName;
					},
					onlineOta: function() {
						return onlineOta;
					}
				}
			});
			modalInstance.result.then(function() {}, function() {});
		}

		function isChinese(cityInput) {
			var re = /[^\u4e00-\u9fa5]/;
			if (re.test(cityInput)) {
				return false;
			}
			return true;
		}
		$scope.$watch('finalUrl', function(newValue, oldValue) {
			if (newValue == oldValue) {
				return;
			}
			$rootScope.searchResult();
		});
		$scope.$watch('citysName.selected', function(newValue, oldValue) {
			if (newValue == oldValue) {
				return;
			} else {
				$scope.cityBlur();
			}
		});
		$scope.cityBlur = function() {
			$scope.searchDistrict = "";
			/*空过滤*/
			if ($.trim($scope.citysName.selected) == "") {
				$scope.changeDistrictName = {};
				return;
			}
			/*英文字符过滤*/
			if (isChinese($.trim($scope.citysName.selected))) {
				var selectCity = $scope.citysName.selected;
				var Len = selectCity.replace(/[\u4e00-\u9fa5]/g, "aa").length;
				if (Len < 3) {
					$scope.changeDistrictName = {};
					return;
				}
			} else {
				$scope.changeDistrictName = {};
				return;
			}
			$scope.changeDistrictName = {};
			var city_id = getCityId($scope.citysName.selected);
			if (city_id == -1 || city_id == false) {
				$scope.changeDistrictName = {};
				return;
			}
		}

		$scope.checkOtaLineStatus = function(hotel) {
			var currentOtaIds = hotel.ota_ids;
			for (var i = 0; i < currentOtaIds.length; i++) {
				if (ota_id == currentOtaIds[i]) {
					return 1;
				}
			};
			return 0;
		}

		function getAllMerchant() {
			var url = "/api/admin/merchant/all";
			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.allMerchants = resp.result.merchants;

						$scope.searchMerchant = resp.result.merchants;
						$scope.searchMerchant['selected'] = $scope.searchMerchant[0];

						$scope.urlCheck();
						$rootScope.searchResult();
					} else {
						console.log(resp.errmsg);
					}
				})
				.error(function() {});
		}

		$scope.getHotelStar = function(m) {
			if (m == "0") {
				return "无";
			} else if (m == "1") {
				return "一星";
			} else if (m == "2") {
				return "二星";
			} else if (m == "3") {
				return "三星";
			} else if (m == "4") {
				return "四星";
			} else if (m == "5") {
				return "五星";
			}
		}

		function loadCitys() {
			var url = "/api/city/";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						$scope.citys = resp.result.citys;
						for (var i = 0; i < $scope.citys.length; i++) {
							$scope.citysName.push($scope.citys[i]['name']);
						};
					}
				})
				.error(function() {});
		}
		$scope.conditionReset = function conditionReset() {
			$scope.checkedItem = [false, false, false];
			$scope.searchName = "";
			$("#searchCity").val("");
			$scope.searchStar = 0;
			$scope.urlCheck();
		}

		$scope.urlCheck = function urlCheck() {
			$scope.searchCity = $("#searchCity").val();
			var url = "/api/admin/ota/" + ota_id + "/hotels/?";
			if ($scope.checkedItem[0] == false) {
				if ($scope.checkedItem[1] == true) {
					url = url + "status=1";
				} else if ($scope.checkedItem[2] == true) {
					url = url + "status=2";
				} else {
					url = url + "status=0";
				}
			} else {
				url = url + "status=0";
			}
			if ($.trim($scope.searchMerchant.selected.id) != "" && $scope.searchMerchant.selected.id != undefined) {
				url = url + "&merchant_id=" + $scope.searchMerchant.selected.id;
			}
			if ($.trim($scope.searchName) != "" && $scope.searchName != undefined) {
				url = url + "&hotel_name=" + $scope.searchName;
			}
			if ($.trim($scope.searchCity) != "" && $scope.searchCity != undefined) {
				var cityId = getCityId($scope.searchCity);
				if (cityId == false) {
					$("#pageInfo").hide();
					$scope.hotels = [];
					cityId = "10000";
				}
				url = url + "&city_id=" + cityId;
			}
			if ($.trim($scope.searchStar) != "" && $scope.searchStar != undefined && $scope.searchStar != "0") {
				url = url + "&star=" + $scope.searchStar;
			}
			$scope.finalUrl = encodeURI(url);
			console.log($scope.finalUrl);
		}

		$rootScope.searchResult = function searchResult() {
			$http.get($scope.finalUrl)
				.success(function(resp) {
					if (resp.errcode == 0) {
						console.log(resp);
						$scope.hotels = resp.result.hotels;
					} else {}
				})
				.error(function() {});
		}

		function init() {
			loadCitys();
			loadAllOtas();
			getAllMerchant();
		}
		init();
		$scope.singleHotelOnline = function(hotel_id, is_online) {
			var url = "/api/admin/ota/" + ota_id + "/hotel/" + hotel_id + "/online/" + is_online;
			console.log(url);
			$http.put(url, {})
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$rootScope.searchResult();
					} else {}
				})
				.error(function() {});
		}

		$scope.getCityName = function(cityId) {
			for (var i = 0; i < $scope.citys.length; i++) {
				var city = $scope.citys[i];
				if (city.id == cityId) {
					return city.name;
				}
			}
			return '';
		}

		function getCityId(cityName) {
			for (var i = 0; i < $scope.citys.length; i++) {
				var city = $scope.citys[i];
				if (city.name == cityName) {
					return city.id;
				}
			}
			return false;
		}
	}])

	adminHotelsApp.controller('onLineStatus', function($scope, $http, $rootScope, $modalInstance, otas, hotelId) {

		$scope.allCurrentOtas = angular.copy(otas);
		$scope.currentOtas = [];
		$scope.allOtaStatus = {
			status: false
		};
		$scope.otaErrMessage = "";
		function init() {
			for (var i = 0; i < $scope.allCurrentOtas.length; i++) {
				if (($scope.allCurrentOtas[i]['isOnline'] == 1)||($scope.allCurrentOtas[i]['id'] == 13)) {
					$scope.currentOtas.push($scope.allCurrentOtas[i]);
				}
			};
		}
		init();
		$scope.allOtaSelect = function() {
			var currentStatus = $scope.allOtaStatus.status;
			if (currentStatus == false) {
				for (var i = 0; i < $scope.currentOtas.length; i++) {
					$scope.currentOtas[i]['checked'] = true;
				};
			} else if (currentStatus == true) {
				for (var i = 0; i < $scope.currentOtas.length; i++) {
					$scope.currentOtas[i]['checked'] = false;
				};
			}
		}
		$scope.cancel = function() {
			$modalInstance.dismiss('cancel');
		};
		$scope.onLineManage = function() {
			$scope.otaErrMessage = "";
			var url = "/api/admin/ota/hotel/" + hotelId + "/modify";
			var params;
			var selectedOtas = [];
			for (var i = 0; i < $scope.currentOtas.length; i++) {
				if ($scope.currentOtas[i]['checked'] == true) {
					selectedOtas.push($scope.currentOtas[i].id);
				}
			};
			var params = {
				"ota_ids": selectedOtas
			};
			console.log(url);
			console.log(params);
			$http.put(url, params)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$modalInstance.dismiss('cancel');
						$rootScope.searchResult();
					} else {
						$scope.otaErrMessage = "操作失败";
					}
				})
				.error(function() {
					$scope.otaErrMessage = "操作失败";
				});
		}
	});

	adminHotelsApp.controller('confirmLineManage', function($scope, $http, $rootScope, $modalInstance, status, hotelId, otaId, currentOtaName, onlineOta) {
		$scope.currentName = currentOtaName;
		$scope.currentStatus = status;
		$scope.errorMessage = "";
		$scope.cancel = function() {
			$modalInstance.dismiss('cancel');
		};
		$scope.singleHotelOnline = function() {
			$scope.errorMessage = "";
			var finalStatus = ($scope.currentStatus == 0) ? 1 : 0;
			var url = "/api/admin/ota/" + otaId + "/hotel/" + hotelId + "/online/" + finalStatus;
			console.log(url);
			$http.put(url, {})
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$rootScope.searchResult();
						$modalInstance.dismiss('cancel');
					} else {
						$scope.errorMessage = "操作失败";
					}
				})
				.error(function() {
					$scope.errorMessage = "操作失败";
				});
		}

	});

})()