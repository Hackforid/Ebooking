angular.module('myhotelApp.directives', []).directive('pageInfo', function($parse) {
  return {
    scope: {
      currentPage: '=key',
      itemPerPage: '=itemkey',
      pageCount: '=itemcount',
      myclick: '&'
    },
    link: function(scope, element, attris) {
      var urlCheck = $parse(scope.myclick);

      function setPage() {
        var count = 10000;
        if (scope.pageCount < scope.itemPerPage) {
          count = scope.currentPage;
        }
        var pageindex = scope.currentPage;
        var linkList = [];
        if (pageindex == 1) {
          linkList[linkList.length] = "<span  href='javascript:void(0)' class='disabled' >&lt; 上一页</span>";
        } else {
          linkList[linkList.length] = "<a  href='javascript:void(0)' >&lt; 上一页</a>";
        }

        function setPageList() {
          if (pageindex == i) {
            linkList[linkList.length] = "<a  href='javascript:void(0)' class='current'>" + i + "</a>";
          } else {
            var tempi = (i-1);
            if(tempi != count){
               linkList[linkList.length] = "<a  href='javascript:void(0)'>" + i + "</a>";
            }
          }
        }
        if (count <= 3) {
          for (var i = 1; i <= count; i++) {
            setPageList();
          }
        } else {
          if (pageindex < 3) {
            for (var i = 1; i <= 3; i++) {
              setPageList();
            }
            linkList[linkList.length] = "<span>...</span>";
          } else {
            for (var i = pageindex - 1; i <= pageindex + 1; i++) {
              setPageList();
            }
            linkList[linkList.length] = "<span>...</span>";
          }
        }
        if (pageindex == count) {
          linkList[linkList.length] = "<span  href='javascript:void(0)' class='disabled'>下一页  &gt;</span>";
        } else {
          linkList[linkList.length] = "<a  href='javascript:void(0)' >下一页  &gt;</a>";
        }

        $("#pageNumber").html(linkList.join(""));

        //事件点击
        var pageClick = function() {
          var aLink = $("#pageNumber").find("a");
          if (aLink.length == 0) {
            return;
          }
          var initPage = pageindex; //初始的页码
          aLink[0].onclick = function() { //点击上一页
            if (initPage == 1) {
              return;
            }
            initPage--;
            scope.currentPage = initPage;
            scope.$apply(function() {
              urlCheck({
                currentPage: initPage
              });
            });
            return;
          }
          for (var i = 1; i < aLink.length - 1; i++) { //点击页码
            aLink[i].onclick = function() {
              initPage = parseInt(this.innerHTML);
              scope.currentPage = initPage;
              scope.$apply(function() {
                /*event.stopPropagation();
                event.preventDefault();*/
                urlCheck({
                  currentPage: initPage
                });
              });
              return;
            }
          }
          aLink[aLink.length - 1].onclick = function() { //点击下一页
            if (scope.pageCount < scope.itemPerPage) {
              return;
            }
            initPage++;
            scope.currentPage = initPage;
            scope.$apply(function() {
              urlCheck({
                currentPage: initPage
              });
            });
            return;
          }
        }()
      }
      scope.$watch('itemPerPage', function(newValue, oldValue) {
        if (newValue == oldValue) {
          return;
        }
        scope.currentPage = 1;
        urlCheck({
          currentPage: scope.currentPage
        });
        setPage();
      });
      scope.$watch('currentPage', function(newValue, oldValue) {
        setPage();
        $(window).scrollTop(0);
      });
      scope.$watch('pageCount', function(newValue, oldValue) {
        if (newValue == oldValue) {
          return;
        }
        setPage();
      });
    }
  };
})