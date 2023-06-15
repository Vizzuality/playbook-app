$(document).ready(function () {
  $("#login, #logout").on("click", function () {
    const url = $(this).data("url");
    window.location.href = url;
  });

  $("#search-field").on("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      const searchQuery = $(this).val();

      $.ajax({
        url: "/search",
        data: { query: searchQuery },
        success: function (data) {
          $("#playbook-container").html(data);
          $(window).scrollTop(0);
        },
      });
    }
  });

  $(document).ready(function () {
    if ($("#sidebarContainer").is(":empty")) {
      $.get("/sidebar", function (data) {
        $("#sidebarContainer").html(data);
      });
    }
  });

  // Handle browser's back button
  window.onpopstate = function (event) {
    if (event.state && event.state.path) {
      $("#playbook-container").load(event.state.path);
      $(window).scrollTop(0);
    }
  };
  $("#playbook-container").on("click", "a.search-result-link", function (e) {
    e.preventDefault();
    $("#playbook-container").load($(this).attr("href"));
    $(window).scrollTop(0);
  });
});
function loadContent(url) {
  $.ajax({
    url: url,
    type: "GET",
    success: function (response) {
      $("#playbook-container").html(response);
      $(window).scrollTop(0);
    },
    error: function () {
      console.error("Error loading content");
    },
  });
}
