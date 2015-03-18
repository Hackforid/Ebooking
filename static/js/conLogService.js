var appservice = angular.module('myApp.service', []);


var ifIe = function showLog() {
	var b = document.createElement('b');
	b.innerHTML = '<!--[if IE]><i></i><![endif]-->';
	//console.log("ietest");
	return b.getElementsByTagName('i').length === 1;
}();


appservice.service('config', function() {

	return {
		showLog: ifIe
	};

});


appservice.service('log', ['config', function(config) {

	return {
		log: log
	};

	function log(data) {

		if (!config.showLog) {
			console.log(data);
		}

	}

}]);