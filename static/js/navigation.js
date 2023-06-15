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
      console.log(event.state.path);
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

$(document).ready(function () {
  function titleCase(str) {
    return str
      .toLowerCase()
      .split(" ")
      .map(function (word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
      })
      .join(" ");
  }

  var urlPath = window.location.pathname;

  if (urlPath === "/" || urlPath === "/index.html" || urlPath === "") {
    document.title = "Vizzuality Playbook";
  } else {
    var pathParts = urlPath.split("/");
    var titleFromUrl = pathParts[pathParts.length - 1];

    titleFromUrl = decodeURIComponent(titleFromUrl).replace(/[_-]/g, " ");

    if (titleFromUrl) {
      var newTitle = "Vizzuality Playbook - " + titleCase(titleFromUrl);
      var newUrl = window.location.href;

      document.title = newTitle;
      $('meta[name="title"]').attr("content", newTitle);
      $('meta[property="og:title"]').attr("content", newTitle);
      $('meta[property="twitter:title"]').attr("content", newTitle);

      $('meta[property="og:url"]').attr("content", newUrl);
      $('meta[property="twitter:url"]').attr("content", newUrl);
    }
  }
});
