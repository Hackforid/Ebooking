(function() {
	var contractApp = angular.module('contractApp', ['ui.bootstrap']);
	contractApp.controller('contractCtrl', ['$scope', '$http', '$modal', '$rootScope', '$timeout',function($scope, $http, $modal, $rootScope,$timeout) {
		$scope.payTypeContract = false;
		$scope.hotelName;
		$scope.currentSaveFlag = 1; /*1 新增 0 修改*/
		$scope.errMessage = "";
		$scope.roomErrMessage = "";
		$scope.allRoomType = {};
		$scope.currentPayType;
		$scope.weekShow = false;
		$scope.weekSelectShow = true;
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
				'selected': false
			}, {
				'day': '周日',
				'selected': false
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
				$scope.weekSelectShow = true;
				$scope.saveContract();
			} else {
				$scope.weekShow = true;
				$("#week").val("确定");
				$scope.weekSelectShow = false;
			}
		}
		$scope.hotelInfo = {
			"merchant_id": merchantID,
			"hotel_id": hotelID,
		};
		$scope.openSpecialPrice = function(currentRoom, currentPayType) {
			currentRoom["pay_type"] = currentPayType;
			var modalInstance = $modal.open({
				templateUrl: 'specialPrice.html',
				controller: 'specialPriceCtrl',
				size: 'lg',
				resolve: {
					special: function() {
						return currentRoom;
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
			}, function() {
				console.log('dismiss');
			});
		}

		$rootScope.loadContracts = function loadContracts() {
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			$http.get(url)
				.success(function(resp) {
					if (resp.errcode == 0) {
						console.log(resp);
						$scope.currentSelectItem = [];
						var contractHotel = resp.result.contract_hotel;
						$scope.hotelName = resp.result.hotel.base_hotel['name'];
						$scope.hotelInfo['base_hotel_id'] = resp.result.hotel['base_hotel_id'];
						$scope.allRoomType = resp.result.roomtypes;
						var contractRoomtypes = resp.result.contract_roomtypes;
						if (isEmptyObject(contractHotel)) {
							console.log("zeng");
							$scope.payTypeContract = false;
							$scope.currentSaveFlag = 1;
							$scope.currentSelectItem = [5, 6];
							$scope.weekItem[4]['selected'] = true;
							$scope.weekItem[5]['selected'] = true;
						} else {
							$scope.currentSaveFlag = 0;
							var selectedWeek;
							if(contractHotel.weekend!=""){
								selectedWeek = contractHotel.weekend.split(",");
							}else{
								selectedWeek=[];
							}
							for (var i = 0; i < selectedWeek.length; i++) {
								var index = (selectedWeek[i]) - 1;
								$scope.currentSelectItem.push((selectedWeek[i]));
								$scope.weekItem[index]['selected'] = true;
							};
							console.log("gai");
							$scope.payTypeContract = true;
							$scope.hotelInfo = contractHotel;
						}
						var currentcontractRoomType = {
							"merchant_id": merchantID,
							"weekday_base_price": "",
							"weekend_base_price": "",
							"retain_num": "",
							"cancel_rule": "",
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
			$scope.errMessage = "";
			$scope.hotelInfo['weekend'] = $scope.currentSelectItem.join(",");
			console.log($scope.hotelInfo);
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/contract";
			if ($scope.currentSaveFlag == 1) {
				console.log("新增");
				$http.post(url, $scope.hotelInfo)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							$scope.payTypeContract = true;
							$scope.currentSaveFlag = 0;
							$scope.errMessage = "保存成功";
							$timeout(function(){$scope.errMessage = "";},2000);
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
							$scope.errMessage = "保存成功";
							$timeout(function(){$scope.errMessage = "";},2000);
						}
					}).error(function() {
						console.log('network error');
					});
			}
		}
		$rootScope.loadContracts();
	}])

	contractApp.controller('roomContranctCtrl', function($scope, $http, $modalInstance, $rootScope, contract) {
		$scope.currentallRoomType = contract;
		$scope.currentPayallRoomType = {
			"current": {
				"merchant_id": merchantID,
				"weekday_base_price": "",
				"weekend_base_price": "",
				"retain_num": "",
				"cancel_rule": "",
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
			if (($.trim(finalContract.cancel_rule) == "") && (finalContract.pay_type == 1)) {
				$scope.roomErrMessage = "取消政策不能为空";
				return;
			}
			if ($.trim(finalContract.breakfast) == "") {
				$scope.roomErrMessage = "早餐不能为空";
				return;
			}
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/roomtype/" + $scope.currentallRoomType.id + "/pay_type/" + $scope.currentallRoomType["pay_type"] + "/contract";
			console.log(url);
			console.log(finalContract);
			if (($scope.currentallRoomType.preContractRoomTypes.flag == 1) && ($scope.currentallRoomType["pay_type"] == 1)) {
				delete finalContract["flag"];
				delete finalContract["pay_type"];
				$http.post(url, finalContract)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							$modalInstance.dismiss('cancel');
							$rootScope.loadContracts();
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
							$rootScope.loadContracts();
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
							$rootScope.loadContracts();
						}
					})
					.error(function() {
						console.log('network error');
					});
			}
		}
		$scope.cancel = function() {
			$modalInstance.dismiss('cancel');
			$rootScope.loadContracts();
		};
	});

	contractApp.controller('specialPriceCtrl', function($scope, $http, $modalInstance, special) {
		$scope.addPrice = "";
		$scope.addRemark = "";
		$scope.priceErrMessage;
		$scope.currentSpecialPrice = special;
		$scope.existSpecial;
		$scope.existSpecialShow = false;
		$scope.flag = 0; /*0新增1修改*/
		$scope.currentModifyObj; /*0新增1修改*/
		$scope.cancelModify = function() {
			$scope.flag = 0;
			$("#addbutton").html("增加");
			$("#startTime").val("");
			$("#endTime").val("");
			$scope.addPrice = "";
			$scope.addRemark = "";
		}

		$scope.checkSpecial = function() {
			$scope.priceErrMessage = "";
			if ($.trim($("#startTime").val()) == "") {
				$scope.priceErrMessage = "开始时间不能为空";
				return;
			}
			if ($.trim($("#endTime").val()) == "") {
				$scope.priceErrMessage = "结束时间不能为空";
				return;
			}
			if ($.trim($scope.addPrice) == "") {
				$scope.priceErrMessage = "价格不能为空";
				return;
			}
			if ($.trim($("#startTime").val()) > $.trim($("#endTime").val())) {
				$scope.priceErrMessage = "开始时间不能大于结束时间";
				return;
			}
			if ($scope.flag == 0) {
				var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/roomtype/" + $scope.currentSpecialPrice.id + "/pay_type/" + $scope.currentSpecialPrice.pay_type + "/spec_price/";
				var obj = {
					"start_date": $("#startTime").val(),
					"end_date": $("#endTime").val(),
					"price": $scope.addPrice,
					"remark": $scope.addRemark
				};
				$http.post(url, obj)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							getSpecial();
							$scope.cancelModify();
						}
					})
					.error(function() {
						console.log('network error');
					});
			} else if ($scope.flag == 1) {
				var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/roomtype/" + $scope.currentModifyObj.roomtype_id + "/spec_price/" + $scope.currentModifyObj.id;
				var specialObj = {
					"start_date": $("#startTime").val(),
					"end_date": $("#endTime").val(),
					"price": $scope.addPrice,
					"remark": $scope.addRemark
				}
				console.log(url);
				console.log(specialObj);
				$http.put(url, specialObj)
					.success(function(resp) {
						console.log(resp);
						if (resp.errcode == 0) {
							getSpecial();
							$scope.cancelModify();
						}
					})
					.error(function() {
						console.log('network error');
					});
			}
		}

		function getSpecial() {
			var url = "/api/admin/merchant/" + merchantID + "/hotel/" + hotelID + "/roomtype/" + $scope.currentSpecialPrice.id + "/pay_type/" + $scope.currentSpecialPrice.pay_type + "/spec_price/";
			console.log(url);
			console.log($scope.currentSpecialPrice);
			$http.get(url)
				.success(function(resp) {
					console.log(resp);
					if (resp.errcode == 0) {
						$scope.existSpecial = resp.result.contract_spec_prices;
						if ($scope.existSpecial.length != 0) {
							$scope.existSpecialShow = true;
						}
					}
				})
				.error(function() {
					console.log('network error');
				});
		}

		getSpecial();
		$scope.modifySpecial = function(specialprice) {
			$scope.flag = 1; /*修改为1*/
			$("#startTime").val(specialprice.start_date);
			$("#endTime").val(specialprice.end_date);
			$scope.addPrice = specialprice.price;
			$scope.addRemark = specialprice.remark;
			$("#addbutton").html("保存修改");
			$scope.currentModifyObj = specialprice;
		}
		$scope.today = function() {
			$scope.dt = new Date();
			$scope.dt1 = new Date();
		};
		//$scope.today();

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

		$scope.open = function($event, index) {
			$scope.opened = false;
			$scope.opened1 = false;
			$event.preventDefault();
			$event.stopPropagation();
			if (index == 0) {
				$scope.opened = true;
			} else if (index == 1) {
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