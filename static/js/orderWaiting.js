(function() {

	var orderWaitingApp = angular.module('orderWaitingApp', []);
	orderWaitingApp.controller('orderWaitingCtrl', ['$scope', '$http', function($scope, $http) {

		
		$scope.orderList = {};$scope.refuseReson;

		$scope.priceDivIn = function(index) {


			$("#orderPrice-" + index).after("<div class='room-info'>取消规则：一经预订不可取消，扣除全额房费.<br />价格类别：普通售价<br />每日价格：<b>09-28</b>170元，<b>09-30</b>180元</div>").show(0, function() {});

		}

		$scope.priceDivOut = function(index) {
			console.log(index);
			$("#orderPrice-" + index).next("div.room-info").hide(0, function() {
				$("#orderPrice-" + index).next("div.room-info").remove();
			});

		}

		$scope.detailDivIn = function(index) {

			var detailDiv = "<div class='classthree'>" +
				"<div style='width:100%;height:30px;text-align:center;font-size:15px'>订单详情</div>" +
				"<div> <span class='classone'>订单确认号：</span>  <span  class='classtwo'>" + "98789855555555555555555555555555555555555" + "</span> </div>" +
				"<div> <span class='classone'>酒店名称：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['hotel_name']) + "</span></div>" +
				"<div> <span class='classone'>房型：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['room_type_name']) + "</span></div>" +
				"<div> <span class='classone'>入离日期：</span>  <span class='classtwo'>" + ($scope.orderList[index]['checkin_date']) + "至" + ($scope.orderList[index]['checkout_date']) + "</span></div>" +
				"<div><span class='classone'>预订时间：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['create_time'].join(" ")) + "</span> </div>" +
				"<div><span class='classone'>入住人：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['hotel_name']) + "</span> </div>" +
				"<div><span class='classone'>联系人：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['contact_name']) + "</span> </div>" +
				"<div><span class='classone'>联系电话：</span>  <span class='classtwo' >" + ($scope.orderList[index]['contact_mobile']) + "</span> </div>" +
				"<div><span class='classone'>取消规则：</span>  <span  class='classtwo'>e" + ($scope.orderList[index]['hotel_name']) + "</span> </div>" +
				"<div><span class='classone'>价格代码名称：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['hotel_name']) + "</span> </div>" +
				"<div><span class='classone'>每日价格：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['everyday_price']) + "</span> </div>" +
				"<div><span class='classone'>总价：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['total_price']) + "</span> </div>" +
				"<div><span class='classone'>备注：</span>  <span  class='classtwo'>" + ($scope.orderList[index]['total_price']) + "</span> </div></div>";



			$("#orderConfimId-" + index).after(detailDiv).show(0, function() {});



		}
		$scope.detailDivOut = function(index) {
			console.log("222");

			$("#orderConfimId-" + index).next("div.classthree").hide(); 

		}

		$scope.acceptOrder = function() {
			
			var url = "/api/order/67/operate/";

			$http.post(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}

		$scope.refuseOrder = function() {

			if($scope.refuseReson.trim()==""||$scope.refuseReson==undefined)
			{
				alert("不能为空");return;

			}
			
			var url = "/api/order/67/operate/?reson=" +$scope.refuseReson;
			
			$http.delete(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {

					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}


		$scope.showInfo1=function(){$("#infoDiv1").show();}
		$scope.hideInfo1=function(){$("#infoDiv1").hide();}
		$scope.showInfo2=function(){$("#infoDiv2").show();}
		$scope.hideInfo2=function(){$("#infoDiv2").hide();}


		function init() {

			var url = "/api/order/waiting/";

			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.orderList = resp.result.orders;


						for (var i = 0; i < $scope.orderList.length; i++) {

							var temp = $scope.orderList[i]["customer_info"];
							var tempobj = eval(temp);
							$scope.orderList[i]["customer_info"] = tempobj;

							$scope.orderList[i]["everyday_price"] = ($scope.orderList[i]["everyday_price"]) / 100;

							var temptime = $scope.orderList[i]["create_time"].split(" ");
							$scope.orderList[i]["create_time"] = temptime;

						};
						console.log($scope.orderList);



					} else {
						alert(resp.errmsg);
					}
				})
				.error(function() {
					alert('network error');
				})

		}
		init();



	}])



})()