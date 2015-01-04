(function() {

    var phoneChecker = function(mobile) {
        var re = /^1\d{10}$/;
        if (re.test(mobile)) {
            return true;
        }
        return false;
    };

    var userManageApp = angular.module('userManageApp', []);

    userManageApp.controller('userInfoController', ['$scope', '$http', '$location', function($scope, $http, $location) {

        function initSelectUser(data) {
            for(var i=0;i<data.length; i++) {
                var user = data[i];
                user.auths={};
                user.auth_all=false;
                auth = user.authority;
                for(var j=0;j<10;j++) {
                    user.auths[j] = false;
                }
                for(var j=0;j<10;j++) {
                    if((auth & (1<<j))>0) {
                        user.auths[j] = true;
                    }
                }
                if(auth == 1023 || auth == 1022) {
                    user.auth_all=true;
                }
            }
            $scope.users = angular.copy(userList);
            $scope.selectUser = angular.copy(userList[0]);
            $scope.tmpUser = {};
            $scope.selected = {};
            $scope.isShow=true;
            $scope.selectBadMobile=false;
            $scope.selectBadDepartment=false;
            $scope.selectBadPassword=false;
            if($scope.selectUser.authority%2==1) {
                $scope.isShow=false;
            }
            for (var i=0; i<$scope.users.length; i++) {
                $scope.tmpUser[$scope.users[i].id] = angular.copy($scope.users[i]);
                $scope.selected[$scope.users[i].id] = '';
            }
        }
        initSelectUser(userList);

        $scope.showSelect=true;
        $scope.showAdd = false;
        $scope.selected[$scope.selectUser.id] = 'active';
        $scope.selected[0]='';

        $scope.showSelectUser = function(id) {
            $scope.showSelect = true;
            $scope.showAdd = false;
            $scope.selectUser = $scope.tmpUser[id];
            if($scope.selectUser.authority%2==1) {
                $scope.isShow=false;
            } else {
                $scope.isShow=true;
            }

            for(var i=0; i<$scope.users.length; i++) {
                $scope.selected[$scope.users[i].id] = '';
            }
            $scope.selected[$scope.selectUser.id] = 'active';
            $scope.selected[0]='';
        };

        $scope.submitUpdate = function() {
            var good=true;
            if(!phoneChecker($scope.selectUser.mobile)) {
                $scope.selectBadMobile = true;
                good=false;
            }
            if(!$scope.selectUser.department) {
                $scope.selectBadDepartment = true;
                good=false;
            }
            if(($scope.selectUser.password) && ($scope.selectUser.password.length <6 || $scope.selectUser.password.length >20)) {
                $scope.selectBadPassword = true;
                good = false;
            }
            if(!good) {
                return;
            }
            var submit = {};
            submit['merchant_id'] = $scope.selectUser.merchant_id;
            submit['username'] = $scope.selectUser.username;
            submit['password'] = $scope.selectUser.password;
            submit['department'] = $scope.selectUser.department;
            submit['mobile'] = $scope.selectUser.mobile;
            submit['email'] = $scope.selectUser.email;
            submit['authority']=0;
            for(var i=0;i<10;i++) {
                if($scope.selectUser.auths[i]) {
                    submit['authority'] += (1<<i);
                }
            }
            if($scope.selectUser.is_valid=='1') {
                submit['is_valid'] = 1;
            } else {
                submit['is_valid'] = 0;
            }

            $http.put("/api/userManage/", submit)
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

        function initAddUser() {
            $scope.addUser = {};
            $scope.addUser.merchant_id = $scope.users[0].merchant_id;
            $scope.addUser.auths = {};
            $scope.addUser.is_valid = 1;
            for(var i=1;i<10;i++) {
                $scope.addUser.auths[i] = false;
            }
            $scope.addUser.auths[0] = false;
            $scope.addUser.auth_all = false;

            $scope.addBadUsername = false;
            $scope.addBadPassword = false;
            $scope.addBadDepartment = false;
            $scope.addBadMobile = false;
        }
        initAddUser();

        $scope.showAddUser = function() {
            $scope.showSelect = false;
            $scope.showAdd = true;
            for(var i=0; i<$scope.users.length; i++) {
                $scope.selected[$scope.users[i].id] = '';
            }
            $scope.selected[0]='active';
        };

        $scope.submitAdd = function() {
            var good=true;
            if(!$scope.addUser.username || $scope.addUser.username.length <2 || $scope.addUser.username > 20) {
                $scope.addBadUsername = true;
                good = false;
            }
            if(!$scope.addUser.password || !$scope.addUser.re_password || $scope.addUser.password != $scope.addUser.re_password) {
                $scope.addBadPassword = true;
                good = false;
            }
            if(($scope.addUser.password) && ($scope.addUser.password.length <6 || $scope.addUser.password.length >20)) {
                $scope.addBadPassword = true;
                good = false;
            }
            if(!$scope.addUser.department) {
                $scope.addBadDepartment = true;
                good=false;
            }
            if(!phoneChecker($scope.addUser.mobile)) {
                $scope.addBadMobile = true;
                good=false;
            }
            if(!good) {
                return;
            }
            var submit = {};
            submit['merchant_id'] = $scope.addUser.merchant_id;
            submit['username'] = $scope.addUser.username;
            submit['password'] = $scope.addUser.password;
            submit['re_password'] = $scope.addUser.re_password;
            submit['department'] = $scope.addUser.department;
            submit['mobile'] = $scope.addUser.mobile;
            submit['authority'] = 0;
            for(var i=1; i<10; i++) {
                if ($scope.addUser.auths[i]) {
                    submit['authority'] += (1<<i);
                }
            }
            if($scope.addUser.is_valid=='1') {
                submit['is_valid'] = 1;
            } else {
                submit['is_valid'] = 0;
            }
            $http.post("/api/userManage/", submit)
                .success(function(response) {
                    if (response.errcode==0) {
                        alert('添加成功');
                        $http.get("/api/userManage")
                            .success(function(response){
                                if(response.errcode==0) {
                                    initSelectUser(response.result);
                                } else {
                                    window.location = "/userManage";
                                }
                            }).error(window.location = "/userManage");
                        initAddUser();
                    } else {
                        alert(response.errmsg);
                    }
                }).error('网络错误');
        };
        $scope.cancelAdd = function() {
            initAddUser();
        };


        $scope.selectAllAuth = function(user) {
            for(var i=1;i<10;i++) {
                if(!user.auth_all) {
                    user.auths[i] = true;
                } else {
                    user.auths[i] = false;
                }
            }
        };

        $scope.changeAuth = function (user, id) {
            if(id<1 || id>9) {
                user.auths[id] = !user.auths[id];
                return;
            }
            user.authority ^= (1<<id);
            if(user.authority == 1023 || user.authority == 1022) {
                user.auth_all = true;
            } else {
                user.auth_all = false;
            }
        };

    }]);
})();
