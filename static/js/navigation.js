$(document).ready(function () {
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
