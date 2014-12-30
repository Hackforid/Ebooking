(function() {

	var hotelWillCoopApp = angular.module('hotelWillCoopApp', ['myApp.directives']);


	hotelWillCoopApp.controller('hotelWillCoopContentCtrl', ['$scope', '$http', function($scope, $http) {

			$scope.citys = [];
			$scope.hotels = [];


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



			//$scope.cityList = [];


			$scope.checkedHotel=function checkedHotel() { 
			//$("[name='checkBox']").attr("checked",'true');//全选
			 //$("[name='checkBox']").removeAttr("checked");//取消全选

			 var hotelIds=[];
			 var checkbox=$("[name='checkBox']");
			 for (var i = 0; i < checkbox.length; i++) {
			 	if($(checkbox[i]).is(':checked'))
			 	{hotelIds.push(i);
			 	}
			 };


			 var url = "/api/hotel/coops/";
				$http.post(url,{'hotel_ids': [1,2,3]})
					.success(function(resp) {
						if (resp.errcode == 0) {
							console.log(resp);
						}
					})
					.error(function() {});


		}




			$scope.urlCheck = function urlCheck(a) {
				$scope.currentPage = a;
				//console.log("这里是urlCheck url变化的地方");

				var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

				var url = '/api/hotel/willcoop/?start=' + pageNum;

				if ($scope.searchName.trim() != "" && $scope.searchName != undefined) {
					url = url + "&name=" + $scope.searchName;

				}
				if ($scope.searchCity.trim() != "" && $scope.searchCity != undefined) {
					var cityId = getCityId($scope.searchCity);
					url = url + "&city_id=" + cityId;


				}
				if ($scope.searchStar.trim() != "" && $scope.searchStar != undefined) {
					url = url + "&star=" + $scope.searchStar;

				}
				if ($scope.itemPerPage.trim() != "" && $scope.itemPerPage != undefined) {
					url = url + "&limit=" + $scope.itemPerPage;

				}
				$scope.finalUrl = url;

			}


			function loadCitys() {

				var url = "/api/city/";
				$http.get(url)
					.success(function(resp) {
						if (resp.errcode == 0) {
							$scope.citys = resp.result.citys;
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

				$scope.searchName = "";
				$scope.searchCity = "";
				$scope.searchStar = "";
			}


			$scope.confirmResult = function confirmResult() {
				$("#acceptDialog").hide();

			}


			$scope.searchResult = function searchResult() {

				//console.log($scope.finalUrl);
				$http.get($scope.finalUrl)
					.success(function(resp) {
						if (resp.errcode == 0) {
							console.log(resp);

							$scope.itemPerPage = resp.result.limit;
							$scope.total = resp.result.total;

							if ($scope.total == 0) {
								$("#pageInfo").hide();
							}

							$scope.hotels = resp.result.hotels;

							$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

							$scope.directiveCtl = true;
							//console.log("数据库操作");

						} else {

							$scope.messageBox = resp.errmsg;
							$("#acceptDialog").show();
						}

					})
					.error(function() {
						$scope.messageBox = "酒店列表读取失败";
						$("#acceptDialog").show();

					});


			}

			$scope.cooprate = function(hotel, index) {

				var url = '/api/hotel/coop/' + hotel.id;
				$http.post(url)
					.success(function(resp) {
						if (resp.errcode == 0) {
							$scope.messageBox = "合作成功";

							$("#acceptDialog").show();

							$scope.hotels.splice(index, 1);

						} else {

							$scope.messageBox = resp.errmsg;

							$("#acceptDialog").show();
						}
					})
					.error(function() {

						$scope.messageBox = "网络错误";

						$("#acceptDialog").show();

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

				return ' ';
			}

		}])
		/*.controller('hotelWillCoopPageIndicatorCtrl',
				['$scope', function($scope) {
			$scope.itemPerPage = 10;
		}])*/
})()