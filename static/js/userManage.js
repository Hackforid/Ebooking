(function() {

    var userManageApp = angular.module('userManageApp', []);

    userManageApp.controller('userInfoController', ['$scope', '$http', '$location', function($scope, $http, $location) {

        for(var i=0;i<userList.length; i++) {
            user = userList[i];
            user.auths={};
            user.auth_all=false;
            auth = user.authority;
            for(var j=0;j<=10;j++) {
                user.auths[j] = false;
            }
            for(var j=0;j<=10;j++) {
                if((auth & (1<<j))>0) {
                    user.auths[j] = true;
                }
            }
            if(auth == 2047 || auth == 2046) {
                user.auth_all=true;
            }
        }
        $scope.users = angular.copy(userList);

        $scope.showSelect=true;
        $scope.selectUser = angular.copy(userList[0]);
        $scope.tmpUser = {};
        $scope.isShow=true;
        if($scope.selectUser.authority%2==1) {
            $scope.isShow=false;
        }
        for (var i=0; i<$scope.users.length; i++) {
            $scope.tmpUser[$scope.users[i].id] = angular.copy($scope.users[i]);
        }

        $scope.showSelectUser = function(id) {
            $scope.showSelect = true;
            $scope.showAdd = false;
            $scope.selectUser = $scope.tmpUser[id];
            if($scope.selectUser.authority%2==1) {
                $scope.isShow=false;
            } else {
                $scope.isShow=true;
            }
        };

        $scope.selectAllAuth = function() {
            for(var i=1;i<=10;i++) {
                if(!$scope.selectUser.auth_all) {
                    $scope.selectUser.auths[i] = true;
                } else {
                    $scope.selectUser.auths[i] = false;
                }
            }
        };

        $scope.changeAuth = function (id) {
            if(id<1 || id>10) {
                $scope.selectUser.auths[id] = !$scope.selectUser.auths[id];
                return;
            }
            $scope.selectUser.authority ^= (1<<id);
            if($scope.selectUser.authority == 2047 || $scope.selectUser.authority == 2046) {
                $scope.selectUser.auth_all = true;
            } else {
                $scope.selectUser.auth_all = false;
            }
        };

        $scope.submitUpdate = function() {
            submit = {};
            submit['merchant_id'] = $scope.selectUser.merchant_id;
            submit['username'] = $scope.selectUser.username;
            submit['password'] = $scope.selectUser.password;
            submit['department'] = $scope.selectUser.department;
            submit['mobile'] = $scope.selectUser.mobile;
            submit['email'] = $scope.selectUser.email;
            submit['authority']=0;
            for(var i=0;i<=10;i++) {
                if($scope.selectUser.auths[i]) {
                    submit['authority'] += (1<<i);
                }
            }
            submit['valid_begin_date'] = $scope.selectUser.valid_begin_date;
            submit['valid_end_date'] = $scope.selectUser.valid_end_date;
            if($scope.selectUser.is_valid=='1') {
                submit['is_valid'] = 1;
            } else {
                submit['is_valid'] = 0;
            }

            $http.put("/userManage/", submit)
                .success(function(response) {
                    if (response.errcode==0) {
                        for(var i=0;i<$scope.users.length;i++) {
                            if($scope.users[i].id == $scope.selectUser.id) {
                                $scope.users[i] = angular.copy($scope.selectUser);
                                break;
                            }
                        }
                        $scope.tmpUser[$scope.selectUser.id] = $scope.selectUser;
                        alert("修改成功");
                        $scope.selectUser.password=null;
                    } else {
                        if (response.errcode==301) {
                            alert('修改成功，请重新登陆');
                            window.location = response.errmsg;
                        } else {
                            alert(response.errmsg);
                        }
                    }
                })
                .error(function() {
                    alert("网络异常");
                });
        };

        $scope.cancelUpdate = function() {
            for(var i=0; i<$scope.users.length; i++) {
                if($scope.users[i].id == $scope.selectUser.id) {
                    $scope.tmpUser[$scope.users[i].id] = angular.copy($scope.users[i]);
                    $scope.selectUser = $scope.tmpUser[$scope.users[i].id];
                    break;
                }
            }
        };


        $scope.showAdd = false;
        $scope.addUser = {};

        $scope.showAddUser = function() {
            $scope.showSelect = false;
            $scope.showAdd = true;
        };

        $scope.submitAdd = function() {

        };
        $scope.cancelAdd = function() {
            $scope.addUser = {};
        };
    }]);
})();
