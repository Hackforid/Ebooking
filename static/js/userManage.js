(function() {

    var userManageApp = angular.module('userManageApp', []);

    userManageApp.controller('userInfoController', ['$scope', '$http', function($scope, $http) {

        for(i=0;i<userList.length; i++) {
            user = userList[i];
            user.auths={};
            user.auth_all=false;
            auth = user.authority;
            for(j=0;j<10;j++) {
                user.auths[j] = false;
            }
            for(j=0;j<10;j++) {
                if((auth & (1<<j))>0) {
                    user.auths[j] = true;
                }
            }
            if(auth == 1023) {
                user.auth_all=true;
            }
        }
        $scope.users = angular.copy(userList);

        $scope.showSelect=true;
        $scope.selectUser = angular.copy(userList[0]);
        $scope.tmpUser = {};
        for (i=0; i<$scope.users.length; i++) {
            $scope.tmpUser[$scope.users[i].id] = angular.copy($scope.users[i]);
        }

        $scope.showSelectUser = function(id) {
            $scope.showSelect = true;
            $scope.showAdd = false;
            $scope.selectUser = $scope.tmpUser[id];
        };

        $scope.selectAllAuth = function() {
            for(i=0;i<10;i++) {
                if(!$scope.selectUser.auth_all) {
                    $scope.selectUser.auths[i] = true;
                } else {
                    $scope.selectUser.auths[i] = false;
                }
            }
        };

        $scope.submitUpdate = function() {
            submit = {};
            submit['id'] = $scope.selectUser.id;
            submit['merchantId'] = $scope.selectUser.merchantId;
            submit['username'] = $scope.selectUser.username;
            submit['password'] = $scope.selectUser.password;
            submit['department'] = $scope.selectUser.department;
            submit['mobile'] = $scope.selectUser.mobile;
            submit['email'] = $scope.selectUser.email;
            submit['authority']=0;
            for(i=0;i<10;i++) {
                if($scope.selectUser.auths[i]) {
                    submit['authority'] += (1<<i);
                }
            }
            submit['valid_begin_date'] = $scope.selectUser.valid_begin_date;
            submit['valid_end_date'] = $scope.selectUser.valid_end_date;
            submit['is_valid'] = $scope.selectUser.is_valid;
            submit['is_delete'] = $scope.selectUser.is_delete;

            $http.put("/userManage/" + submit.merchantId, submit)
                .success(function(response) {
                    if (response.errcode==0) {
                        for(i=0;i<$scope.users.length;i++) {
                            if($scope.users[i].id == $scope.selectUser.id) {
                                $scope.users[i] = angular.copy($scope.selectUser);
                                break;
                            }
                        }
                        $scope.tmpUser[$scope.selectUser.id] = $scope.selectUser;
                        alert("成功");
                    } else {
                        alert(response.errmsg);
                    }
                })
                .error(function() {
                    alert("网络异常");
                });
        };

        $scope.cancelUpdate = function() {
            for(i=0; i<$scope.users.length; i++) {
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
