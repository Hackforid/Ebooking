(function() {
	var adminHotelsApp = angular.module('adminHotelsApp', ['ui.bootstrap']);
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
	adminHotelsApp.controller('adminHotelsCtrl', ['$scope', '$http', function($scope, $http) {

		$scope.citys = [];
		$scope.hotels = [];
		$scope.citysName = [];
		$scope.searchName = "";
		$scope.searchStatus = "";
		$scope.searchCity = "";
		$scope.searchStar = "";
		$scope.finalUrl;
		$scope.currentHotel;
		$scope.currentHotelIndex;
		$scope.changeDistrictName = {};
		$scope.currentRoomtypes;
		$scope.currentHotelId;

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
			$scope.searchResult();
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
			var districtUrl = "/api/city/" + city_id + "/district/";
			console.log(districtUrl);
			$http.get(districtUrl)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.changeDistrictName = resp.result.districts;
						var unlimitedDistrict = {
							id: -100,
							name: "不限"
						};
						$scope.changeDistrictName.unshift(unlimitedDistrict);
					} else {
						console.log(resp.errmsg);
					}
				})
				.error(function() {});
		}
		$scope.getStatus = function(s) {
			if (s == "1") {
				return "正常";
			} else if (s == "0") {
				return "暂停";
			}
		}

		$scope.getHotelStar = function(m) {
			if (m == "0") {
				return "无";
			} else if (m == "1") {
				return "一星级";
			} else if (m == "2") {
				return "二星级";
			} else if (m == "3") {
				return "三星级";
			} else if (m == "4") {
				return "四星级";
			} else if (m == "5") {
				return "五星级";
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
			$scope.searchDistrict = "";
			$scope.changeDistrictName = {};
			$scope.searchName = "";
			$scope.searchStatus = "";
			//$scope.searchCity = "";
			$("#searchCity").val("");
			$scope.searchStar = "";
			$scope.finalUrl = "/api/admin/merchant/" + merchant_id + "/hotels/?start=0";
			$scope.searchResult();
		}

		$scope.urlCheck = function urlCheck() {
			$scope.searchCity = $("#searchCity").val();
			var url = "/api/admin/merchant/" + merchant_id + "/hotels/?start=0";
			if ($.trim($scope.searchName) != "" && $scope.searchName != undefined) {
				url = url + "&name=" + $scope.searchName;
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
			if ($.trim($scope.searchDistrict) != "" && $scope.searchDistrict != undefined && $.trim($scope.searchDistrict) != -100) {
				url = url + "&district_id=" + $scope.searchDistrict;

			}
			$scope.finalUrl = encodeURI(url);
			console.log($scope.finalUrl);
		}

		$scope.searchResult = function searchResult() {
			$http.get($scope.finalUrl)
				.success(function(resp) {
					if (resp.errcode == 0) {
						console.log(resp);
						$scope.hotels = resp.result.hotels;
					} else {
						console.log("酒店列表读取失败");
					}
				})
				.error(function() {
					console.log("酒店列表读取失败");
				});
		}

		function init() {
			loadCitys();
			$scope.urlCheck();
			$scope.searchResult();
		}
		init();
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
		$scope.redictToContractPage = function(hotelId) {
			window.location.href = ("/admin/merchant/" +merchant_id+"/hotel/"+ hotelId + "/contract/");
		}
	}])
})()