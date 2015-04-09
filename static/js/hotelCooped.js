(function() {

	var hotelCoopApp = angular.module('hotelCoopedApp', ['myApp.service','myhotelApp.directives', 'ui.bootstrap']);


	hotelCoopApp.directive('ngEnter', function() {
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



	hotelCoopApp.config(['$httpProvider', function($httpProvider) {

		if (!$httpProvider.defaults.headers.get) {
			$httpProvider.defaults.headers.get = {};
			// $httpProvider.defaults.headers.post = {};    

		}

		$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	}]);



	hotelCoopApp.controller('hotelCoopedContentCtrl', ['$scope', '$http','log', function($scope, $http,log) {

		$scope.citys = [];
		$scope.hotels = [];


		$scope.citysName = [];


		$scope.searchName = "";
		$scope.searchStatus = "";
		$scope.searchCity = "";
		$scope.searchStar = "";
		$scope.itemPerPage = "20";
		$scope.currentPage = 1;
		$scope.total;

		$scope.pageCount;
		$scope.directiveCtl = false;
		$scope.finalUrl;
		$scope.paginationId = "pageNumber";
		$scope.messageBox;



		$scope.currentHotel;

		$scope.currentHotelIndex;

		log.log("logtest");



		$scope.hotelFacilitys = {
			"3": "免费宽带",
			"4": "收费宽带",
			"5": "免费停车场",
			"6": "收费停车场",
			"15": "专职行李员",
			"16": "擦鞋服务",
			"17": "行李寄存",
			"18": "票务服务",
			"19": "外币兑换服务",
			"20": "夜床服务",
			"21": "快速入住服务",
			"22": "免费班车接送",
			"23": "代客泊车服务",
			"24": "24小时前台接待服务",
			"25": "雨伞租借服务",
			"26": "秘书服务",
			"27": "书吧",
			"28": "放映厅",
			"29": "公共音响系统",
			"158": "棋牌室",
			"159": "桑拿浴室",
			"160": "健身中心",
			"161": "美容美发室",
			"162": "卡拉OK厅",
			"164": "台球室",
			"165": "SPA",
			"166": "足浴/足疗",
			"167": "乒乓球室",
			"168": "按摩保健",
			"169": "网球场",
			"170": "夜总会",
			"171": "休闲会所",
			"172": "私家沙滩",
			"173": "篮球场",
			"174": "温泉",
			"175": "羽毛球馆",
			"176": "歌舞厅",
			"177": "保龄球馆",
			"178": "垂钓",
			"179": "壁球室",
			"180": "海边娱乐",
			"181": "儿童乐园",
			"182": "水上运动",
			"183": "电子游戏室",
			"184": "网吧",
			"185": "沙弧球馆",
			"186": "排球场",
			"187": "桌上游戏",
			"188": "康乐中心",
			"189": "日光浴场",
			"190": "射击",
			"191": "空中花园",
			"192": "游船游艇",
			"193": "采摘园",
			"194": "攀岩",
			"195": "停车",
			"196": "无停车场",
			"197": "免费停车",
			"198": "收费停车",
			"199": "电梯",
			"200": "无电梯",
			"201": "有电梯",
			"202": "公共区域上网",
			"203": "不能上网",
			"206": "前台保险柜",
			"208": "会议设施",
			"209": "自助取款机",
			"210": "免费旅游交通图",
			"211": "茶室",
			"212": "商品部",
			"213": "安全消防系统",
			"214": "大堂吧",
			"215": "公共区域闭路电视监控系统",
			"216": "残障人客房",
			"217": "咖啡厅",
			"218": "酒吧",
			"219": "电子结账系统",
			"220": "大堂免费报纸",
			"221": "无烟楼层",
			"222": "无障碍通道",
			"223": "行政酒廊",
			"224": "24小时热水",
			"225": "中餐厅",
			"226": "西餐厅",
			"227": "大堂提供上网电脑",
			"228": "烧烤",
			"229": "雪茄吧",
			"230": "休息区",
			"231": "轮椅",
			"232": "公共区域空调",
			"233": "日餐厅",
			"234": "中西自助餐厅",
			"235": "旋转餐厅",
			"236": "宴会厅",
			"237": "医疗支援",
			"238": "邮政服务",
			"239": "婴儿或儿童看护",
			"240": "叫车服务",
			"241": "房间消毒",
			"243": "租借笔记本电脑",
			"244": "多种语言服务人员",
			"245": "自行车租借服务",
			"246": "管家服务",
			"247": "婚宴服务",
			"251": "高尔夫"
		};


		$scope.confirmCancel=false;
		$scope.cancelIndex;

		$scope.changeDistrictName = {};

		$scope.roomConfirmCancel = false;
		$scope.roomCloseIndex;
		$scope.currentIsOnline;

		$scope.allRoomClose=function(isonline){

			$scope.roomConfirmCancel = true;

			$scope.currentIsOnline=isonline;

		}

		$scope.roomCloseConfirm = function() {

			//var url = "/api/hotel/" + hotelId + "/roomtype/" + $scope.cooped[$scope.roomCloseIndex].cooped_roomtype_id + "/online";
			var url="/api/merchant/roomtype/online";
			log.log(url);
			log.log({
					"is_online": parseInt($scope.currentIsOnline)
				});


			$http.put(url, {
					"is_online": parseInt($scope.currentIsOnline)
				})
				.success(function(resp) {
					log.log(resp);
					if (resp.errcode == 0) {

						$scope.roomConfirmCancel = false;

					} else {
						log.log(resp.errmsg);
					}
				})
				.error(function() {
					log.log('network error');
				})


		}



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
				/*空过滤*/
				if($.trim($scope.citysName.selected) == ""){
					$scope.changeDistrictName = {};
					return;
				}
				/*英文字符过滤*/
				if(isChinese($.trim($scope.citysName.selected))){
					var selectCity = $scope.citysName.selected;
					var Len = selectCity.replace(/[\u4E00-\u6FA5]/g, "aa").length;
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

						} else {
							log.log(resp.errmsg);
						}
					})
					.error(function() {});


			}

		$scope.confirmOk=function(){ 

			
			var url="/api/hotel/cooped/"+$scope.hotels[$scope.cancelIndex].id;

			log.log(url);

			$http({method: 'DELETE', url: url})
				.success(function(resp) {
					log.log(resp);
					if (resp.errcode == 0) {

						$scope.hotels.splice($scope.cancelIndex,1);

						$scope.confirmCancel=false;
						
						
					} else {
						log.log(resp.errmsg);
					}
				})
				.error(function() {
					log.log('network error');
				})



		}

		$scope.cancelBtn=function(index){
			//console.log(index);
			$scope.confirmCancel=true;
			$scope.cancelIndex=index;

		}





		$scope.mapshow = function() {
			//$("#hotel-detail").hide();
			$("#mapDetail").show();

			$("#mapShowDiv").append("<div id='map" + $scope.currentHotel['id'] + "' style='width:600px;height:400px'></div>");

			var xShow = $scope.currentHotel['glog'];
			var yShow = $scope.currentHotel['glat'];

			var mp = new BMap.Map(('map' + $scope.currentHotel['id']));

			mp.centerAndZoom(new BMap.Point(xShow, yShow), 14);

			//在地图上面描点
			var marker = new BMap.Marker(new BMap.Point(xShow, yShow)); // 创建标注
			mp.addOverlay(marker);
			$("#mapDetail").show();

			// setTimeout(function(){$("#mapShowDiv").find("*").remove();},5000);

		}



		$scope.closeMapDetail = function() {
			$("#mapDetail").hide();
			$("#mapShowDiv").find("*").remove();
		}



		function loadJScript() {
			var script = document.createElement("script");
			script.type = "text/javascript";
			script.src = "http://api.map.baidu.com/api?v=1.4";
			document.body.appendChild(script);
		}



		$scope.changeStatus = function(id) {


			var radioBox = $("[name='status']");
			var statusRemark;


			if ($(radioBox[0]).is(':checked')) {
				statusRemark = 1;
			} else if ($(radioBox[1]).is(':checked')) {

				statusRemark = 0;

			}

			var url = "/api/hotel/cooped/" + id + "/online/" + statusRemark + "/";
			log.log(url);
			$http.put(url)
				.success(function(resp) {
					log.log(resp);
					if (resp.errcode == 0) {
						//console.log($scope.hotels[index]);
						$scope.hotels[$scope.currentHotelIndex]['is_online'] = resp.result.cooperate_hotel.is_online;
						$("#hotel-detail").hide();

					}
				})
				.error(function() {});



		}



		$scope.checkBook = function(a, b) {
			var checkBookResult;
			if (a == "0") {
				checkBookResult = "不允许外国人入住";

			} else {
				checkBookResult = "允许外国人入住";
			}
			if (b == "0") {
				checkBookResult = checkBookResult + "预定不需要身份证";
			} else {

				checkBookResult = checkBookResult + "预定需要身份证";
			}

			return checkBookResult;

		}



		$scope.hotelDetail = function(m) {

			$scope.currentHotelIndex = m;

			$scope.currentHotel = $scope.hotels[m];
			log.log($scope.currentHotel);

			if (typeof $scope.currentHotel['facilities'] === 'string') {

				var facilityNumber = [];

				facilityNumber = $scope.currentHotel['facilities'].split(",");
				var facilitys = [];

				for (var i = 0; i < facilityNumber.length; i++) {
					if ($scope.hotelFacilitys[facilityNumber[i]] != undefined) {
						facilitys.push($scope.hotelFacilitys[facilityNumber[i]]);
					}

				};

				$scope.currentHotel['facilities'] = facilitys;

			}


			$("#hotel-detail").show();

		}

		$scope.closeHotelDetail = function() {
			$("#hotel-detail").hide();

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

			$scope.changeDistrictName = {};
			$scope.searchName = "";
			$scope.searchStatus = "";
			//$scope.searchCity = "";
			$("#searchCity").val("");
			$scope.searchStar = "";

			$scope.finalUrl = '/api/hotel/cooped/?start=0&limit=' + $scope.itemPerPage;
			$scope.searchResult();
		}


		$scope.confirmResult = function confirmResult() {
			$("#acceptDialog").hide();

		}


		$scope.urlCheck = function urlCheck(a) {

			/*if ($scope.flag == "0" && $.trim($scope.searchName) == "" && $.trim($scope.searchStar) == "" && $.trim($scope.searchStatus) == "") {
		
				$scope.finalUrl = '/api/hotel/cooped/?start=0&limit=' + $scope.itemPerPage;
				$scope.searchResult();
				
				return;
			}*/

			$scope.currentPage = a;
			$scope.searchCity = $("#searchCity").val();
			//console.log("这里是urlCheck url变化的地方");

			var pageNum = ($scope.currentPage - 1) * ($scope.itemPerPage);

			var url = '/api/hotel/cooped/?start=' + pageNum;

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

			if ($.trim($scope.searchStatus) != "" && $scope.searchStatus != undefined && $scope.searchStatus != "2") {
				url = url + "&is_online=" + $scope.searchStatus;

			}
			if ($.trim($scope.itemPerPage) != "" && $scope.itemPerPage != undefined) {
				url = url + "&limit=" + $scope.itemPerPage;

			}

			if ($.trim($scope.searchDistrict) != "" && $scope.searchDistrict != undefined) {
					url = url + "&district_id=" + $scope.searchDistrict;

			}

			$scope.finalUrl = encodeURI(url);
			log.log($scope.finalUrl);

		}



		$scope.searchResult = function searchResult() {

			$http.get($scope.finalUrl)
				.success(function(resp) {
					if (resp.errcode == 0) {
						log.log(resp);
						$scope.hotels = resp.result.hotels;

						$scope.itemPerPage = resp.result.limit;
						$scope.total = resp.result.total;


						if ($scope.total != 0) {
							$("#pageInfo").show();
						} else {
							$("#pageInfo").hide();
						}


						//$scope.pageCount = Math.ceil(($scope.total) / ($scope.itemPerPage));

						$scope.pageCount = resp.result.hotels.length;

						$scope.directiveCtl = true;


					} else {

						//$scope.messageBox = resp.errmsg;
						//$("#acceptDialog").show();

					}

				})
				.error(function() {


					log.log("酒店列表读取失败");


				});


		}


		function init() {
			$(".menu2").find("dd").eq(0).addClass("active");

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

		$scope.redictToInventoryPage = function(hotel) {
			window.location.href = ("/hotel/cooped/" + hotel.id + "/inventory/");
		}
	}])

})()



function loadScript() {　
	//console.log("loadScript开始");

	var script = document.createElement("script");　

	script.src = "http://api.map.baidu.com/api?v=1.4&callback=''";　

	document.body.appendChild(script);
}
window.onload = loadScript;