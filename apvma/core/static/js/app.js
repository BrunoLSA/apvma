$('form').submit(function (e) {

  e.preventDefault();

  $.post({
    url: '/api/reservations/',
    data: {
      user: $('#user').val(),
      date: $('#date').val(),
      spot: $('#spot').val(),
    },

    success: function (content) {

      // get values from JSON response
      var newEvent = content.spot;
      var cellId = '#day_' + parseInt(content.date.substr(8, 2));

      // update calendar
      var currentHtml = $(cellId).html();
      var newHtml = currentHtml.replace('&nbsp;', newEvent);
      $(cellId).html(newHtml);

      // update form
      var parts = content.date.split('-');
      var year = parts[0];
      var month = parseInt(parts[1]);
      var day = parseInt(parts[2]);
      var optionValue = year + '-' + month + '-' + day;
      $('option[value=' + optionValue + ']').remove();  // remove date
      $('#spot').val('');  // clean text input

    },

    error: function (content) {
      console.log(content);
    },
  });
});

// © 2018 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About