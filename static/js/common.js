//
//此文档的js是登录后模板页公共js部分，静态适用，动态代码可重写
//
//
$(document).ready(function() {

  //$(".menu1").find("a").click(function(){console.log($(this).parent());$(this).parent().addclass("active");alert("1");});

  function waitingQuery() {
    $.ajax({
      url: '/api/order/waiting/?start=0',
      success: function(data) {
        var total = data.result.total;
        //console.log("data");
        // console.log(total);
        if (total > 0) {
          $("#orderPoint").show();
        } else {
          $("#orderPoint").hide();
        }
      }
    });
  }

  waitingQuery();
  setInterval(function() {
    waitingQuery();
  }, 60000);


  //显示或隐藏左上角的用户菜单
  var handle = null;
  $(".admin-info").mouseover(function() {
    handle = setTimeout(function() {
      $(".person-menu").show(0);
    }, 300);
  })
  $(".admin-info").mouseout(function() {
    clearTimeout(handle);
  });

  $(".main-left,.main-mid,.main-right").mouseover(function() {
    $(".person-menu").hide(0);
  });


  $(document).bind('click', function(e) {
    if ($(e.target).eq(0).is($(".person-menu")) || $(e.target).eq(0).is($(".person-menu"))) {
      return;
    }
    $(".person-menu").hide(0);
  });



  //新手引导弹窗
  $("#guide-btn").click(function() {
    $("#guide-div").fadeIn(500);
  });
  $("#guide-div .close").click(function() {
    $(".messageDiv").fadeOut(500);
  });


  //退出登录弹窗提示 
  $("#out-btn").click(function() {
    $("#out-div").fadeIn(500);
  });
  $("#out-div #no-out").click(function() {
    $("#out-div").fadeOut(500);
  });

  $("#out-div #sure-out").click(function() {
    location.href = "/logout";
  });

});