(function() {
	var contractApp = angular.module('contractApp', ['ui.bootstrap']);
	contractApp.controller('contractCtrl', ['$scope', '$http', '$modal', function($scope, $http, $modal) {
		$scope.payTypeContract = false;
		$scope.hotelName;
		$scope.currentSaveFlag = 1; /*1 新增 0 修改*/
		$scope.errMessage = "";
		$scope.roomErrMessage = "";
		$scope.allRoomType = {};
		//$scope.currentallRoomType={};
		$scope.currentPayType;
		$scope.weekShow = false;
		$scope.weekSelectShow = true;
		/*$scope.contractRoomType = {
			"base_roomtype_id": 6,
			"merchant_id": merchantID,
			"weekday_base_price": "1",
			"weekend_base_price": "1",
			"retain_num": "1",
			"breakfest": "1",
			"remark": "1"
		};*/
		$scope.currentSelectItem = [];
		$scope.weekItem = [{
				'day': '周一',
				'selected': false
			}, {
				'day': '周二',
				'selected': false
			}, {
				'day': '周三',
				'selected': false
			}, {
				'day': '周四',
				'selected': false
			}, {
				'day': '周五',
				'selected': false
			}, {
				'day': '周六',
				'selected': true
			}, {
				'day': '周日',
				'selected': true
			}

		];

		$scope.weekSave = function() {
			$scope.currentSelectItem = [];

			if ($scope.weekShow == true) {
				$scope.weekShow = false;
				$("#week").val("周末定义");

				for (var i = 0; i < $scope.weekItem.length; i++) {
					if ($scope.weekItem[i]['selected'] == true) {
						var index = i + 1;
						$scope.currentSelectItem.push(index);

					}
				};
				console.log($scope.currentSelectItem);
				$scope.weekSelectShow = true;

			} else {
				$scope.weekShow = true;
				$("#week").val("确定");
				$scope.weekSelectShow = false;
			}

		}
		$scope.test = function() {
			console.log($scope.weekItem);
		}
		$scope.hotelInfo = {
			"merchant_id": merchantID,
			"hotel_id": hotelID,
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
		$scope.openSpecialPrice = function() {
			var modalInstance = $modal.open({
				templateUrl: 'specialPrice.html',
				controller: 'specialPriceCtrl',
				size: 'lg',
				resolve: {
					contract: function() {
						return 1;
					}
				}
			});

			modalInstance.result.then(function() {
				console.log('close');
			}, function() {
				console.log('dismiss');
			});
		}


		$scope.openModify = function(currentRoom, currentPayType) {

			/*$scope.currentallRoomType=currentRoom;
			$scope.currentPayType=currentPayType;
			console.log($scope.currentallRoomType);*/
			currentRoom["pay_type"] = currentPayType;
			console.log(currentRoom);
			var modalInstance = $modal.open({
				templateUrl: 'contractHotelModal.html',
				controller: 'roomContranctCtrl',
				size: 'lg',
				resolve: {
					contract: function() {
						return currentRoom;
					}
				}
			});

			modalInstance.result.then(function() {
				console.log('close');
				//loadMerchants();
			}, function() {
				console.log('dismiss');
			});
		}

		function loadContracts() {
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						console.log(resp);
						var contractHotel = resp.result.contract_hotel;
						$scope.hotelName = resp.result.hotel.base_hotel['name'];
						$scope.hotelInfo['base_hotel_id'] = resp.result.hotel['base_hotel_id'];
						$scope.allRoomType = resp.result.roomtypes;
						var contractRoomtypes = resp.result.contract_roomtypes;
						if (isEmptyObject(contractHotel)) {
							console.log($scope.payTypeContract);
							console.log("zeng");
							$scope.payTypeContract = false;
							$scope.currentSaveFlag = 1;
						} else {
							var selectedWeek = contractHotel.weekend.split("|");
							for (var i = 0; i < selectedWeek.length; i++) {
								var index = (selectedWeek[i]) - 1;
								console.log(index);
								console.log($scope.weekItem[index]);
								$scope.currentSelectItem.push((selectedWeek[i]));
								$scope.weekItem[index]['selected'] = true;
							};
							console.log("gai");
							$scope.payTypeContract = true;
							$scope.currentSaveFlag = 0;
							$scope.hotelInfo = contractHotel;
						}
						var currentcontractRoomType = {
							"merchant_id": merchantID,
							"weekday_base_price": "",
							"weekend_base_price": "",
							"retain_num": "",
							"breakfast": "",
							"remark": "",
							"weekday_sell_price": "",
							"weekend_sell_price": ""
						};
						currentcontractRoomType['base_hotel_id'] = resp.result.hotel['base_hotel_id'];
						for (var i = 0; i < $scope.allRoomType.length; i++) {
							$scope.allRoomType[i]["preContractRoomTypes"] = currentcontractRoomType;
							$scope.allRoomType[i]["comeContractRoomTypes"] = currentcontractRoomType;
							$scope.allRoomType[i]["preContractRoomTypes"]['flag'] = "1";
							$scope.allRoomType[i]["comeContractRoomTypes"]['flag'] = "1";
							$scope.allRoomType[i]["preContractRoomTypes"]['base_roomtype_id'] = $scope.allRoomType[i]["base_roomtype_id"];
							$scope.allRoomType[i]["comeContractRoomTypes"]['base_roomtype_id'] = $scope.allRoomType[i]["base_roomtype_id"];
							for (var j = 0; j < contractRoomtypes.length; j++) {
								if ($scope.allRoomType[i]['id'] == contractRoomtypes[j]['roomtype_id'] && contractRoomtypes[j]['pay_type'] == "1") {
									$scope.allRoomType[i]["preContractRoomTypes"] = contractRoomtypes[j];
									$scope.allRoomType[i]["preContractRoomTypes"]['flag'] = "0"; /*修改*/
								} else if ($scope.allRoomType[i]['id'] == contractRoomtypes[j]['roomtype_id'] && contractRoomtypes[j]['pay_type'] == "0") {
									$scope.allRoomType[i]["comeContractRoomTypes"] = contractRoomtypes[j];
									$scope.allRoomType[i]["comeContractRoomTypes"]['flag'] = "0"; /*修改*/
								}
							};
						};
						console.log($scope.allRoomType);
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
			$scope.errMessage = "";
			$scope.hotelInfo['weekend'] = $scope.currentSelectItem.join("|");
			console.log($scope.hotelInfo);
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			if ($scope.currentSaveFlag == 1) {
				console.log("新增");
				$http.post(url, $scope.hotelInfo)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {

						}
					})
					.error(function() {
						console.log('network error');
					});

			} else {
				console.log("修改");
				$http.put(url, $scope.hotelInfo)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {

						}
					}).error(function() {
						console.log('network error');
					});
			}
		}
		loadContracts();
	}])

	contractApp.controller('roomContranctCtrl', function($scope, $http, $modalInstance, contract) {
		$scope.currentallRoomType = contract;
		console.log(contract);

		$scope.currentPayallRoomType = {
			"current": {
				"merchant_id": merchantID,
				"weekday_base_price": "",
				"weekend_base_price": "",
				"retain_num": "",
				"breakfast": "",
				"remark": "",
				"weekday_sell_price": "",
				"weekend_sell_price": ""
			}
		};
		$scope.currentPayallRoomType["current"]["base_hotel_id"] = $scope.currentallRoomType["base_hotel_id"];
		$scope.currentPayallRoomType["current"]["base_roomtype_id"] = $scope.currentallRoomType["base_roomtype_id"];
		$scope.currentPayallRoomType["current"]["pay_type"] = $scope.currentallRoomType["pay_type"]
		if (($scope.currentallRoomType["pay_type"] == "1") && ($scope.currentallRoomType.preContractRoomTypes['flag'] == "0")) {
			$scope.currentPayallRoomType["current"] = $scope.currentallRoomType.preContractRoomTypes;

		} else if ($scope.currentallRoomType["pay_type"] == "0" && ($scope.currentallRoomType.comeContractRoomTypes['flag'] == "0")) {
			$scope.currentPayallRoomType["current"] = $scope.currentallRoomType.comeContractRoomTypes;

		}

		$scope.saveRoomTypeContract = function() {
			$scope.allRoomType;
			var finalContract = $scope.currentPayallRoomType['current'];
			/*if ($scope.currentallRoomType["pay_type"] == "1") {
				finalContract = $scope.currentallRoomType.preContractRoomTypes;
				console.log("1");console.log(finalContract);
			} else {
				finalContract = $scope.currentallRoomType.comeContractRoomTypes;
				console.log("0");console.log(finalContract);
			}*/

			/*if ($.trim(finalContract.retain_num) == "") {
				$scope.roomErrMessage = "保留房数不能为空";
				return;
			}*/
			if ($.trim(finalContract.weekday_base_price) == "") {
				$scope.roomErrMessage = "平日底价不能为空";
				return;
			}
			/*if ($.trim(finalContract.weekend_base_price) == "") {
				$scope.roomErrMessage = "周末底价不能为空";
				return;
			}*/
			if ($.trim(finalContract.breakfast) == "") {
				$scope.roomErrMessage = "早餐不能为空";
				return;
			}
			/*if ($.trim(finalContract.remark) == "") {
				$scope.roomErrMessage = "备注不能为空";
				return;
			}*/
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/roomtype/" + $scope.currentallRoomType.id + "/pay_type/" + $scope.currentallRoomType["pay_type"] + "/contract";
			console.log(url);
			console.log(finalContract);
			//return;
			if (($scope.currentallRoomType.preContractRoomTypes.flag == 1) && ($scope.currentallRoomType["pay_type"] == 1)) {
				delete finalContract["flag"];
				delete finalContract["pay_type"];
				$http.post(url, finalContract)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							$modalInstance.dismiss('cancel');
							$scope.currentallRoomType.preContractRoomTypes = resp.result.contract_roomtype;
						}
					})
					.error(function() {
						console.log('network error');
					});

			} else if (($scope.currentallRoomType.comeContractRoomTypes.flag == 1) && ($scope.currentallRoomType["pay_type"] == 0)) {
				delete finalContract["flag"];
				delete finalContract["pay_type"];
				$http.post(url, finalContract)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							$modalInstance.dismiss('cancel');
							$scope.currentallRoomType.comContractRoomTypes = resp.result.contract_roomtype;
						}
					})
					.error(function() {
						console.log('network error');
					});

			} else {
				delete finalContract["id"];
				delete finalContract["flag"];
				delete finalContract["pay_type"];
				delete finalContract["roomtype_id"];
				delete finalContract["hotel_id"];
				console.log(finalContract);
				$http.put(url, finalContract)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							$modalInstance.dismiss('cancel');

						}
					})
					.error(function() {
						console.log('network error');
					});
			}
		}
		$scope.cancel = function() {
			$modalInstance.dismiss('cancel');
		};
	});

	contractApp.controller('specialPriceCtrl', function($scope, $http, $modalInstance) {
		$scope.addStartDate = "";
		$scope.addEndDate = "";
		$scope.addPrice = "";
		$scope.addRemark = "";
		$scope.priceErrMessage;
		$scope.today = function() {
			$scope.dt = new Date();
			$scope.dt1 = new Date();
		};
		$scope.today();

		$scope.clear = function() {
			$scope.dt = null;
		};
		$scope.disabled = function(date, mode) {
			return (mode === 'day' && (date.getDay() === 0 || date.getDay() === 6));
		};

		$scope.toggleMin = function() {
			$scope.minDate = $scope.minDate ? null : new Date();
		};
		$scope.toggleMin();

		$scope.open = function($event,index) {
			$event.preventDefault();
			$event.stopPropagation();
			if(index==0){
				$scope.opened = true;
			}else if(index==1){
				$scope.opened1 = true;
			}
		};

		$scope.dateOptions = {
			formatYear: 'yy',
			startingDay: 1
		};

		$scope.formats = ['yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
		$scope.format = $scope.formats[0];

		var tomorrow = new Date();
		tomorrow.setDate(tomorrow.getDate() + 1);
		var afterTomorrow = new Date();
		afterTomorrow.setDate(tomorrow.getDate() + 2);
		$scope.events =
			[{
				date: tomorrow,
				status: 'full'
			}, {
				date: afterTomorrow,
				status: 'partially'
			}];

		$scope.getDayClass = function(date, mode) {
			if (mode === 'day') {
				var dayToCheck = new Date(date).setHours(0, 0, 0, 0);

				for (var i = 0; i < $scope.events.length; i++) {
					var currentDay = new Date($scope.events[i].date).setHours(0, 0, 0, 0);

					if (dayToCheck === currentDay) {
						return $scope.events[i].status;
					}
				}
			}

			return '';
		};
		$scope.cancel = function() {
			$modalInstance.dismiss('cancel');
		};
		$scope.saveSpecialPrice = function() {

			var url;
			$http.post(url, finalContract)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$modalInstance.dismiss('cancel');
					}
				})
				.error(function() {
					console.log('network error');
				});

		}

	});



})()