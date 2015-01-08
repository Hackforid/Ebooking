angular.module('myApp.directives', []).directive('pageInfo', function() {
  return {

    link: function(scope, element, attris) {

      function setPage() {
        //console.log("这里是setpage");
        var count = Math.ceil((scope.total) / (scope.itemPerPage));
        var pageindex = scope.currentPage;
        var linkList = [];
        //总页数少于10 全部显示 大于10 显示前3 后3 中间3 其余....
        if (pageindex == 1) {
          linkList[linkList.length] = "<span  href='#' class='disabled' >&lt; 上一页</span>";
        } else {
          linkList[linkList.length] = "<a  href='#' >&lt; 上一页</a>";
        }

        function setPageList() {
            if (pageindex == i) {
              linkList[linkList.length] = "<a  href='#' class='current'>" + i + "</a>";
            } else {
              linkList[linkList.length] = "<a  href='#'>" + i + "</a>";
            }
          }
          //总页数小于10
        if (count <= 10) {
          for (var i = 1; i <= count; i++) {
            setPageList();
          }
        }
        //总页数大于10页
        else {
          if (pageindex <= 4) {
            for (var i = 1; i <= 5; i++) {
              setPageList();
            }
            linkList[linkList.length] = "...<a  href='#'>" + count + "</a>";
          } else if (pageindex >= count - 3) {
            linkList[linkList.length] = "<a href='#'>1</a>...";
            for (var i = count - 4; i <= count; i++) {
              setPageList();
            }
          } else { //当前页在中间部分
            linkList[linkList.length] = "<a href='#'>1</a>...";
            for (var i = pageindex - 2; i <= pageindex + 2; i++) {
              setPageList();
            }
            linkList[linkList.length] = "...<a  href='#'>" + count + "</a>";
          }
        }
        if (pageindex == count) {
          linkList[linkList.length] = "<span  href='#' class='disabled'>下一页  &gt;</span>";
        } else {
          linkList[linkList.length] = "<a  href='#' >下一页  &gt;</a>";
        }


        $("#" + scope.paginationId).html(linkList.join(""));

        //事件点击
        var pageClick = function() {
          var aLink = $("#" + scope.paginationId).find("a");
          var initPage = pageindex; //初始的页码
          aLink[0].onclick = function() { //点击上一页
            if (initPage == 1) {
              return;
            }
            initPage--;
            scope.currentPage = initPage;

            scope.$apply(function() {
              scope.urlCheck(initPage);
            });

            setPage();
            return;
          }
          for (var i = 1; i < aLink.length - 1; i++) { //点击页码
            aLink[i].onclick = function() {
              initPage = parseInt(this.innerHTML);

              scope.currentPage = initPage;

              // console.log("这里是当前页点击");

              scope.$apply(function() {
                scope.urlCheck(initPage);
              });

              setPage();
              return;
            }
          }
          aLink[aLink.length - 1].onclick = function() { //点击下一页
            if (initPage == count) {
              return;
            }
            initPage++;
            scope.currentPage = initPage;

            scope.$apply(function() {
              scope.urlCheck(initPage);
            });
            setPage();
            return;
          }
        }()


      }

      setPage();

      scope.$watch('itemPerPage', function() {
        //console.log("这里是itemPerPage变化时候产生的watch");
        scope.currentPage = 1;
        scope.urlCheck(scope.currentPage);

      });

      scope.$watch('finalUrl', function(newValue, oldValue) {
        //console.log("这里是url变化时候产生的watch");
        //console.log(scope.finalUrl);


        if (newValue == oldValue) {
         // setPage();
          return;
        }
        scope.searchResult();

      });

      scope.$watch('pageCount', function() {
        //console.log("这里是pageCount变化时候产生的watch");
        scope.currentPage = 1;
        setPage();
      });



    }
  };
})