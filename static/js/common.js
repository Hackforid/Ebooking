//
//此文档的js是登录后模板页公共js部分，静态适用，动态代码可重写
//
//
$(document).ready(function() {

  //$(".menu1").find("a").click(function(){console.log($(this).parent());$(this).parent().addclass("active");alert("1");});

  var nameCheckValue = $.trim($("#userNameCheck").html());
  var nameLength = nameCheckValue.replace(/[\u4e00-\u9fa5]/g, "aa").length;
  if (nameLength > 6) {

    var cordCount = 0;
    var realName = "";
    for (var i = 0; i < 6; i++) {
      var singleCode = nameCheckValue.substring(i, i + 1);

      if (/[\u4e00-\u9fa5]/.test(singleCode)) {

        cordCount = cordCount + 2;
        realName = realName + singleCode;
        if (cordCount > 4) {
          break;
        }

      } else {
        cordCount = cordCount + 1;
        realName = realName + singleCode;
        if (cordCount > 6) {
          break;
        }

      }

    };
    realName = realName + "...";

    console.log(realName);
    $("#userNameCheck").html(realName);

  }



  function waitingQuery() {
    $.ajax({
      url: '/api/order/waiting/?start=0',
      success: function(data) {

        if (data.errcode == 0) {
          var total = data.result.total;
          if (total > 0) {
            $("#orderPoint").show();
          } else {
            $("#orderPoint").hide();
          }
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

  /*qq*/

  $("#qqOnline").click(function() {
    $("#qqContact").show();
    $("#qqOnline").css("background-color", "white");
    $("#qqOnline").css("border-left", "1px solid #ccc");
    $("#qqOnline").css("border-right", "1px solid #ccc");

  });
  $("#qqOnline").mouseleave(function() {
    $("#qqContact").hide();
    $("#qqOnline").css("background-color", "#FAFAFA");
    $("#qqOnline").css("border-left", "none");
    $("#qqOnline").css("border-right", "none");
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