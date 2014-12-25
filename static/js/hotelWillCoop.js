(function() {

	var hotelWillCoopApp = angular.module('hotelWillCoopApp', []);

	hotelWillCoopApp.controller('hotelWillCoopContentCtrl', ['$scope', '$http', function($scope, $http) {

			$scope.citys = [];
			$scope.hotels = [];


			$scope.serchName = "";
			$scope.serchCity = "";
			$scope.serchStar = "";
			$scope.itemPerPage = "20";
			$scope.currentPage = 1;
			$scope.total;

			function setPage(count, pageindex) {
				var count = count;
				var pageindex = pageindex;
				var a = [];
				//总页数少于10 全部显示 大于10 显示前3 后3 中间3 其余....
				if (pageindex == 1) {
					a[a.length] = "<span  href='#' class='disabled' >&lt; 上一页</span>";
				} else {
					a[a.length] = "<a  href='#' >&lt; 上一页</a>";
				}

				function setPageList() {
						if (pageindex == i) {
							a[a.length] = "<a  href='#' class='current'>" + i + "</a>";
						} else {
							a[a.length] = "<a  href='#'>" + i + "</a>";
						}
					}
					//总页数小于10
				if (count <= 10) {
					for (var i = 1; i <= count; i++) {
						setPageList();
					}
				}
				//总页数大于10页
				else {
					if (pageindex <= 4) {
						for (var i = 1; i <= 5; i++) {
							setPageList();
						}
						a[a.length] = "...<a  href='#'>" + count + "</a>";
					} else if (pageindex >= count - 3) {
						a[a.length] = "<a href='#'>1</a>...";
						for (var i = count - 4; i <= count; i++) {
							setPageList();
						}
					} else { //当前页在中间部分
						a[a.length] = "<a href='#'>1</a>...";
						for (var i = pageindex - 2; i <= pageindex + 2; i++) {
							setPageList();
						}
						a[a.length] = "...<a  href='#'>" + count + "</a>";
					}
				}
				if (pageindex == count) {
					a[a.length] = "<span  href='#' class='disabled'>下一页  &gt;</span>";
				} else {
					a[a.length] = "<a  href='#' >下一页  &gt;</a>";
				}

				$("#pageNumber").html(a.join(""));

				//事件点击
				var pageClick = function() {
					var aLink = $("#pageNumber").find("a");
					var initPage = pageindex; //初始的页码
					aLink[0].onclick = function() { //点击上一页
						if (initPage == 1) {
							return;
						}
						initPage--;
						setPage(count, initPage);
						$scope.currentPage = initPage;

						$scope.searchHotel();
						return;
					}
					for (var i = 1; i < aLink.length - 1; i++) { //点击页码
						aLink[i].onclick = function() {
							initPage = parseInt(this.innerHTML);

							$scope.currentPage = initPage;

							setPage(count, initPage);
							$scope.searchHotel();
							return;
						}
					}
					aLink[aLink.length - 1].onclick = function() { //点击下一页
						if (initPage == count) {
							return;
						}
						initPage++;
						setPage(count, initPage);
						$scope.currentPage = initPage;

						$scope.searchHotel();
						return;
					}
				}()
			}


			$scope.$watch('itemPerPage', function() {


				$scope.currentPage = 1;
				$scope.searchHotel();


			});



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


			function loadHotels() {

				var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

				var url = '/api/hotel/willcoop/?start=' + pageNum + '&limit=' + $scope.itemPerPage;

				console.log(url);

				$http.get(url)
					.success(function(resp) {
						if (resp.errcode == 0) {

							console.log(resp);
							$scope.itemPerPage = resp.result.limit;
							$scope.total = resp.result.total;

							$scope.hotels = resp.result.hotels;

							var pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

							setPage(pageCount, $scope.currentPage);


						} else {
							alert(resp.errmsg);
						}

					})
					.error(function() {
						alert('酒店列表读取失败');
					});
			}

			$scope.searchHotel = function searchHotel() {

				var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

				var url = '/api/hotel/willcoop/?start=' + pageNum;

				if ($scope.serchName.trim() != "" && $scope.serchName != undefined) {
					url = url + "&name=" + $scope.serchName;

				}
				if ($scope.serchCity.trim() != "" && $scope.serchCity != undefined) {
					var cityId = getCityId($scope.serchCity);
					url = url + "&city_id=" + cityId;


				}
				if ($scope.serchStar.trim() != "" && $scope.serchStar != undefined) {
					url = url + "&star=" + $scope.serchStar;

				}
				if ($scope.itemPerPage.trim() != "" && $scope.itemPerPage != undefined) {
					url = url + "&limit=" + $scope.itemPerPage;

				}


				console.log(url);
				$http.get(url)
					.success(function(resp) {
						if (resp.errcode == 0) {
							console.log(resp);

							$scope.itemPerPage = resp.result.limit;
							$scope.total = resp.result.total;

							$scope.hotels = resp.result.hotels;

							var pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

							setPage(pageCount, $scope.currentPage);


						} else {
							alert(resp.errmsg);
						}

					})
					.error(function() {
						alert('酒店列表读取失败');
					});


			}

			$scope.cooprate = function(hotel) {

				var url = '/api/hotel/coop/' + hotel.id;
				$http.post(url)
					.success(function(resp) {
						if (resp.errcode == 0) {
							alert("合作成功");
						} else {
							alert(resp.errmsg);
						}
					})
					.error(function() {
						alert("网络错误");
					});

			}

			function init() {
				$(".menu2").find("dd").eq(1).addClass("active");
				loadCitys();
				$scope.searchHotel();


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