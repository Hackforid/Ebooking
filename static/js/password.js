(function(){

    var passwordApp = angular.module('passwordApp',[]);

    passwordApp.controller('passwordController', ['$scope', '$http', function($scope, $http) {

        function init () {
            $scope.old_password_tips = false;
            $scope.password_tips = false;
            $scope.password_tips2 = false;
            $scope.re_password_tips = false;
            $scope.re_password_tips2 = false;

            $scope.old_password = '';
            $scope.password = '';
            $scope.re_password = '';
        }
        init();

        $scope.resetPasswordTips = function() {
            $scope.password_tips = false;
            $scope.password_tips2 = false;
        };

        $scope.resetRePasswordTips = function() {
            $scope.re_password_tips = false;
            $scope.re_password_tips2 = false;
        };

        $scope.submit = function() {
            var good = true;
            if(!$scope.old_password) {
                $scope.old_password_tips = true;
                good = false;
            }
            if(!$scope.password) {
                $scope.password_tips = true;
                good = false;
            } else if($scope.password.length < 6 || $scope.password.length > 20) {
                $scope.password_tips = true;
                good = false;
            }

            if(($scope.password) && $scope.password == $scope.old_password) {
                $scope.password_tips2 = true;
                good = false;
            }
            if(!$scope.re_password) {
                $scope.re_password_tips = true;
            } else if($scope.password != $scope.re_password) {
                $scope.re_password_tips2 = true;
                good = false;
            }
            if (!good) {
                return;
            }
            var submit = {};
            submit['old_password'] = hex_md5($scope.old_password);
            submit['password'] = hex_md5($scope.password);
            submit['re_password'] = hex_md5($scope.re_password);
            $http.put("/api/password", submit)
                .success(function (response) {
                    if (response.errcode==0) {
                        alert('修改成功, 请重新登陆');
                        window.location="/login/";
                    } else {
                        alert(response.errmsg);
                    }
                })
                .error(function () {
                    alert('网络错误')
                });
        }
    }])
})();