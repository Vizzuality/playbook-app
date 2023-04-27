$(document).ready(function () {
  $("#menu-links").on("click", "a", function (e) {
    e.preventDefault();
    $("#playbook-container").load($(this).attr("href"));
  });
  $("#login").on("click", function () {
    const url = $(this).data("url");
    window.location.href = url;
  });

  $("#logout").on("click", function () {
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
  $("#playbook-container").on("click", "a.search-result-link", function (e) {
    e.preventDefault();
    $("#playbook-container").load($(this).attr("href"));
  });
});
