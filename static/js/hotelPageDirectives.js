angular.module('myhotelApp.directives', []).directive('pageInfo', function() {
  return {

    link: function(scope, element, attris) {

      function setPage() {
        //console.log("这里是setpage");       
       /* console.log("bug");
        console.log(scope.pageCount);*/

        var count = 10000;   

         if(scope.pageCount<scope.itemPerPage){
              count=scope.currentPage;
        }


        var pageindex = scope.currentPage;
        var linkList = [];
       
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

           
        if (count <= 3) {
          for (var i = 1; i <= count; i++) {
            setPageList();
          }
        }
       
        else {                                     
          if (pageindex < 3) {
            for (var i = 1; i <= 3; i++) {
              setPageList();
            }
            linkList[linkList.length] = "<span>...</span>";
          }  else { //当前页在中间部分
            //linkList[linkList.length] = "";
            for (var i = pageindex - 1; i <= pageindex + 1; i++) {
              setPageList();
            }
            linkList[linkList.length] = "<span>...</span>";
          }
        
       
           }
        if (pageindex == count) {
          linkList[linkList.length] = "<span  href='#' class='disabled'>下一页  &gt;</span>";
        } else {
          linkList[linkList.length] = "<a  href='#' >下一页  &gt;</a>";
        }

        

        $("#" + scope.paginationId).html(linkList.join(""));


        /*if (pageindex == count) {
         
           var aLink = $("#" + scope.paginationId).find("a");
           console.log(aLink);
           $(aLink[(aLink.length-1)]).next("span").remove();
           $(aLink[(aLink.length-1)]).remove();
         
        } */



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

               console.log("这里是当前页点击");

              scope.$apply(function() {
                scope.urlCheck(initPage);
              });

              setPage();
              return;
            }
          }
          aLink[aLink.length - 1].onclick = function() { //点击下一页

             if(scope.pageCount<scope.itemPerPage){
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
        setPage();

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


      scope.$watch('pageCount', function(newValue, oldValue) {
      
        //console.log(scope.finalUrl);

        if (newValue == oldValue) {
       
          return;
        }

        console.log("这里产生的watch");
        setPage();

      });






       

    }
  };
})