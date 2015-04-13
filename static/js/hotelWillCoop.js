(function() {

	var hotelWillCoopApp = angular.module('hotelWillCoopApp', ['myApp.service','myhotelApp.directives', 'ui.bootstrap']);



	hotelWillCoopApp.directive('ngEnter', function() {
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



	hotelWillCoopApp.config(['$httpProvider', function($httpProvider) {

		if (!$httpProvider.defaults.headers.get) {
			$httpProvider.defaults.headers.get = {};
			// $httpProvider.defaults.headers.post = {};    

		}

		$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	}]);



	hotelWillCoopApp.controller('hotelWillCoopContentCtrl', ['$scope', '$http','log', function($scope, $http,log) {

			$scope.citys = [];
			$scope.hotels = [];


			$scope.citysName = [];


			$scope.searchName = "";
			$scope.searchCity = "";
			$scope.searchStar = "";
			$scope.itemPerPage = "20";
			$scope.currentPage = 1;
			$scope.total;
			$scope.pageCount;
			$scope.directiveCtl = false;
			$scope.finalUrl;
			$scope.messageBox;
			$scope.paginationId = "pageNumber";

			$scope.checkStatus = false;

			$scope.changeDistrictName = {};


			function isChinese(cityInput) {
				var re = /[^\u4e00-\u9fa5]/;
				if (re.test(cityInput)) {
					return false;
				}
				return true;
			}

			//$scope.cityList = [];

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
				if($.trim($scope.citysName.selected) == ""){
					$scope.changeDistrictName = {};
					return;
				}
				/*英文字符过滤*/
				if(isChinese($.trim($scope.citysName.selected))){
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

				log.log(districtUrl);

				$http.get(districtUrl)
					.success(function(resp) {
						log.log(resp);
						if (resp.errcode == 0) {
							$scope.changeDistrictName = resp.result.districts;

							var unlimitedDistrict = {
								id: -100,
								name: "不限"
							};
							$scope.changeDistrictName.unshift(unlimitedDistrict);

						} else {
							log.log(resp.errmsg);
						}
					})
					.error(function() {});


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



			$scope.checkedHotel = function checkedHotel() {

				var hotelIds = [];
				var checkbox = $("[name='checkBox']");
				for (var i = 0; i < checkbox.length; i++) {
					if ($(checkbox[i]).is(':checked')) {
						hotelIds.push($scope.hotels[i].id);
					}
				};


				var url = "/api/hotel/coops/";

				$http.post(url, {
						'hotel_ids': hotelIds
					})
					.success(function(resp) {
						if (resp.errcode == 0) {
							log.log(resp);
							var hotelResult = resp.result.hotel_cooprate;


							if (hotelResult.length != 0)

							{
								$scope.messageBox = "合作成功";
								$("#acceptDialog").show();
							}



							for (var i = 0; i < $scope.hotels.length; i++) {
								for (var j = 0; j < hotelResult.length; j++) {
									if ($scope.hotels[i]["id"] == hotelResult[j]["base_hotel_id"]) {
										$scope.hotels.splice(i, 1);
										hotelResult.splice(j, 1);
										i--;
										break;
									}
								};
							};



							$scope.searchResult();

						} else {

							//$scope.messageBox = resp.errmsg;

							//$("#acceptDialog").show();
						}

					})
					.error(function() {

						log.log('network error');

					});

			}



			$scope.urlCheck = function urlCheck(a) {
				$scope.currentPage = a;
				$scope.searchCity = $("#searchCity").val();

				//console.log("这里是urlCheck url变化的地方");

				var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

				var url = '/api/hotel/willcoop/?start=' + pageNum;

				if ($.trim($scope.searchName) != "" && $scope.searchName != undefined) {
					url = url + "&name=" + $scope.searchName;

				}
				if ($.trim($scope.searchCity) != "" && $scope.searchCity != undefined) {
					var cityId = getCityId($scope.searchCity);

					if (cityId == false) {
						$("#pageInfo").hide();
						$scope.hotels = [];

						cityId = "10000";
						//return;
					}


					url = url + "&city_id=" + cityId;


				}
				if ($.trim($scope.searchStar) != "" && $scope.searchStar != undefined && $scope.searchStar != "0") {
					url = url + "&star=" + $scope.searchStar;

				}
				if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
					url = url + "&limit=" + $scope.itemPerPage;

				}

				if ($.trim($scope.searchDistrict) != "" && $scope.searchDistrict != undefined && $.trim($scope.searchDistrict) != -100) {
					url = url + "&district_id=" + $scope.searchDistrict;

				}

				$scope.finalUrl = encodeURI(url);

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



			/*$scope.$watch('searchCity', function(newValue, oldValue) {
				//console.log("watch");
				if (newValue == oldValue) {
					return;
				}

				for (var i = 0; i < $scope.citys.length; i++) {
					if ($scope.citys[i]["name"] == newValue) {
						$("#cityShow").hide();
						return;
					}
				};

				$("#cityShow").show();
				$scope.cityList = [];

				for (var i = 0; i < $scope.citys.length; i++) {
					if (($scope.citys[i]["name"].indexOf($scope.searchCity)) >= 0) {
						$scope.cityList.push($scope.citys[i]["name"]);

					}

				};

			});

			$scope.cityChoose = function cityChoose(a) {
				$scope.searchCity = a;
				$("#cityShow").hide();
			}*/


			$scope.conditionReset = function conditionReset() {

				$scope.checkStatus = false;

				$scope.changeDistrictName = {};

				$scope.searchName = "";
				//$scope.searchCity = "";
				$("#searchCity").val("");
				$scope.searchStar = "";

				$scope.finalUrl = '/api/hotel/willcoop/?start=0&limit=' + $scope.itemPerPage;
				$scope.searchResult();
			}


			$scope.confirmResult = function confirmResult() {
				$("#acceptDialog").hide();

			}


			$scope.searchResult = function searchResult() {

				//console.log("数据库请求");

				log.log($scope.finalUrl);
				$http.get($scope.finalUrl)
					.success(function(resp) {
						if (resp.errcode == 0) {
							log.log(resp);

							$scope.itemPerPage = resp.result.limit;
							$scope.total = resp.result.total;


							if ($scope.total != 0) {
								$("#pageInfo").show();
							} else {
								$("#pageInfo").hide();
							}

							$scope.hotels = resp.result.hotels;

							//$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

							$scope.pageCount = resp.result.hotels.length;



							$scope.directiveCtl = true;
							//console.log("数据库操作");

						} else {

							//$scope.messageBox = resp.errmsg;
							//$("#acceptDialog").show();
						}

					})
					.error(function() {

						log.log("酒店列表读取失败");

					});


			}

			$scope.cooprate = function(hotel, index) {

				var url = '/api/hotel/coop/' + hotel.id;
				$http.post(url)
					.success(function(resp) {
						if (resp.errcode == 0) {
							$scope.messageBox = "合作成功";

							$("#acceptDialog").show();
							//console.log(resp);
							var hotelResult = [];
							hotelResult.push(resp.result.hotel_cooprate);

							if (hotelResult.length != 0) {
								$scope.hotels.splice(index, 1);
							}

						} else {

							//$scope.messageBox = resp.errmsg;

							//$("#acceptDialog").show();
						}
					})
					.error(function() {


						log.log("网络错误");

					});

			}

			function init() {
				$(".menu2").find("dd").eq(1).addClass("active");
				loadCitys();
				$scope.urlCheck($scope.currentPage);
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

		}])
		/*.controller('hotelWillCoopPageIndicatorCtrl',
				['$scope', function($scope) {
			$scope.itemPerPage = 10;
		}])*/
})()