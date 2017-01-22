$(function () {
  $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});

  $("#notifications").click(function () {
    if ($(".popover").is(":visible")) {
      $("#notifications").popover('hide');
    }
    else {
      $("#notifications").popover('show');
      $.ajax({
        url: '/notifications/last/',
        beforeSend: function () {
          $(".popover-content").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
          $("#notifications").attr('data', '');
		  $("#notifications").removeClass("badge1");
        },
        success: function (data) {
          $(".popover-content").html(data);
        }
      });
    }
    return false;
  });

  function check_notifications() {
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data != "0") {
			if (data >=100) {
		  $("#notifications").addClass("badge1");
          $("#notifications").attr('data', '99+');
			}
			else {
          $("#notifications").addClass("badge1");	
          $("#notifications").attr('data', data);
			}
        }
        else {
		  $("#notifications").removeClass("badge1");
          $("#notifications").attr('data', '');
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, 30000);
      }
    });
  };
  check_notifications();
});
