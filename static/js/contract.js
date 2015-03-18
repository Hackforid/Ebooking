var contractApp = angular.module('contractApp', ['myApp.service']);


contractApp.config(['$httpProvider', function($httpProvider) {

	if (!$httpProvider.defaults.headers.get) {
		$httpProvider.defaults.headers.get = {};
		// $httpProvider.defaults.headers.post = {};    

	}

	$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
}]);


contractApp.controller('contractAppCtrl', ['$scope', '$http','log', function($scope, $http,log) {



	$scope.addcontract = false;
	$scope.changeContract = false;



	$scope.addName = "";
	$scope.addPayType = "";
	$scope.addMonery = "";
	$scope.addBankName = "";
	$scope.addBank = "";
	$scope.addCard = "";

	$scope.changeName = "";
	$scope.changePayType = "";
	$scope.changeMonery = "";
	$scope.changeBankName = "";
	$scope.changeBank = "";
	$scope.changeCard = "";

	$scope.moneryShow = true;
	$scope.changemoneryShow = true;


	$scope.contracts;
	$scope.currentContract;
	$scope.currentIndex;

	$scope.changeContractMsg;
	$scope.addContractMsg;



	$scope.checkType = function(type) {
		if (type == "0") {

			return "现付";

		} else if (type == "1") {

			return "预付";

		}

	}

	$scope.checkCommission = function(type, commission) {
		if (type == "0") {

			return (commission+"%");

		} else if (type == "1") {

			return "--";

		}

	}



	$scope.change = function(index) {

		$scope.currentIndex = index;



		$scope.currentContract = $scope.contracts[index];
		log.log($scope.currentContract);

		$scope.changeName = $scope.currentContract.name;
		$scope.changePayType = $scope.currentContract.type;
		$scope.changeMonery = $scope.currentContract.commission;
		$scope.changeBankName = $scope.currentContract.bank_account_name;
		$scope.changeBank = $scope.currentContract.bank_name;
		$scope.changeCard = $scope.currentContract.bank_account_id;
		$scope.changeContract = true;


	}


	$scope.addContractBtn = function() {
		log.log($scope.contracts.length);
		if ($scope.contracts.length == 2) {
			return;
		}
		$scope.addcontract = true;

	}
	$scope.addCancel = function() {
		$scope.addName = "";
		$scope.addPayType = "";
		$scope.addMonery = "";
		$scope.addBankName = "";
		$scope.addBank = "";
		$scope.addCard = "";
		$scope.addcontract = false;

	}

	$scope.$watch("addPayType", function(newValue, oldValue) {

		if (newValue == oldValue) {
			return;
		}

		if (newValue == 0) {

			$scope.moneryShow = true;

		} else if (newValue == 1) {

			$scope.moneryShow = false;

		}

		$scope.addMonery = "";
		$scope.addContractMsg = "";



	});



	$scope.addCurrentContract = function() {

		if($scope.contracts.length == 2){

			$scope.addContractMsg = "已添加过两种类型的合同";
			return;

		}

		if ($scope.contracts.length == 1 && $scope.contracts[0].type == $scope.addPayType) {

			$scope.addContractMsg = "已添加过该类型的合同";
			return;

		}



		if ($.trim($scope.addPayType) == "" || $.trim($scope.addName) == "" || $.trim($scope.addBankName) == "" || $.trim($scope.addBank) == "" || $.trim($scope.addCard) == "") {

			$scope.addContractMsg = "输入内容不能为空";
			return;

		}

		if ($.trim($scope.addMonery) == "" && $scope.addPayType == 0) {

			$scope.addContractMsg = "输入内容不能为空";
			return;

		}


		var testStr = /^[0-9]*[1-9][0-9]*$/;
		var contractMon = $.trim($scope.addMonery);



		if (testStr.test(contractMon) == false && $scope.addPayType == 0) {

			$scope.addContractMsg = "佣金为正整数";
			return;

		}


		if(parseInt(contractMon)>100 && $scope.addPayType == 0) {

			$scope.addContractMsg = "佣金为百分比，需小于100";
			return;

		}





		var testString = /^\d+$/;

		var cardNumber=$.trim($scope.addCard);

		if (testString.test(cardNumber) == false) {

			$scope.addContractMsg = "卡号为整数";
			return;

		}




		$scope.addContractMsg = "";



		var url = '/api/contract';

		var params = {
			"name": $scope.addName,
			"type": parseInt($scope.addPayType),
			"commission": parseInt($scope.addMonery),
			"bank_name": $scope.addBank,
			"bank_account_id": $scope.addCard,
			"bank_account_name": $scope.addBankName
		};


		log.log(params);

		$http.post(url, params)
			.success(function(resp) {
				log.log(resp);
				if (resp.errcode == 0) {

					$scope.contracts.push(resp.result.contract);
					$scope.addcontract = false;

				
				} else {
					

				}
			})
			.error(function() {
				log.log('network error');
			})

	}


	$scope.changeCurrentContract = function() {


		if ($.trim($scope.changeName) == "" || $.trim($scope.changeBankName) == "" || $.trim($scope.changeBank) == "" || $.trim($scope.changeCard) == "") {

			$scope.changeContractMsg = "输入内容不能为空";
			return;

		}

		if ($.trim($scope.changeMonery) == "" && $scope.changePayType == 0) {

			$scope.changeContractMsg = "输入内容不能为空";
			return;

		}


		var testStr = /^[0-9]*[1-9][0-9]*$/;
		var contractMon = $.trim($scope.changeMonery);



		if (testStr.test(contractMon) == false && $scope.changePayType == 0) {

			$scope.changeContractMsg = "佣金为正整数";
			return;

		}


		if(parseInt(contractMon)>100 && $scope.changePayType == 0) {

			$scope.changeContractMsg = "佣金为百分比，需小于100";
			return;

		}



		var testString = /^\d+$/;

		var cardNumber=$.trim($scope.changeCard);

		if (testString.test(cardNumber) == false) {

			$scope.changeContractMsg = "卡号为整数";
			return;

		}






		$scope.changeContractMsg = "";


		var url = '/api/contract';



		var params = {
			"id": $scope.currentContract.id,
			"name": $scope.changeName,
			"commission": parseInt($scope.changeMonery),
			"bank_name": $scope.changeBank,
			"bank_account_id": $scope.changeCard,
			"bank_account_name": $scope.changeBankName
		};

		log.log(params);

		$http.put(url, params)
			.success(function(resp) {
				log.log(resp);
				if (resp.errcode == 0) {
					//$scope.currentContract=resp.result;

					$scope.contracts[$scope.currentIndex] = resp.result.contract;

					$scope.changeContract = false;

				} else {


				}
			})
			.error(function() {
				log.log('network error');
			})


	}



	function init() {

		var url = '/api/contract';

		$http.get(url)
			.success(function(resp) {
				log.log(resp);
				if (resp.errcode == 0) {

					$scope.contracts = resp.result.contracts;



				} else {


				}
			})
			.error(function() {
				log.log('network error');
			})

	}

	$(".menu4").find("dd").eq(2).addClass("active");

	init();



}]);