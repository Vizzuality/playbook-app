$(document).ready(function () {
  var mdPath = window.location.pathname;
    if (mdPath.startsWith('/view-md/')) {
        $.ajax({
            url: mdPath,
            type: 'GET',
            success: function(data) {
                if (data.status === "redirect") {
                    window.location.href = data.url;
                } else {
                    $('#playbook-container').html(data);
                }
            },
            error: function() {
                console.log('Error loading content');
            }
        });
    }
  $("#menu-links, .search-results").on("click", "a", function (e) {
    e.preventDefault();
    var url = $(this).attr("href");
    $("#playbook-container").load(url, function () {
      window.history.pushState({ path: url }, "", url);
    });
  });

  $("#login, #logout").on("click", function () {
    const url = $(this).data("url");
    window.location.href = url;
  });

  $('#search-field').on('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      const searchQuery = $(this).val();

      $.ajax({
        url: '/search',
        data: { query: searchQuery },
        success: function (data) {
          $('#playbook-container').html(data);
        }
      });
    }
  });

  // Handle browser's back button
  window.onpopstate = function (event) {
    if (event.state && event.state.path) {
      $("#playbook-container").load(event.state.path);
    }
  };
  $("#playbook-container").on("click", "a.search-result-link", function (e) {
    e.preventDefault();
    $("#playbook-container").load($(this).attr("href"));
  });
});
function loadContent(url) {
  $.ajax({
      url: url,
      type: 'GET',
      success: function(response) {
          $('#playbook-container').html(response);
      },
      error: function() {
          console.error('Error loading content');
      }
  });
}