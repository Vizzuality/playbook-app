$(document).ready(function () {
  $("#menu-links").on("click", "a", function (e) {
    e.preventDefault(); // Prevent default navigation behavior

    // Load the content of the clicked link into the playbook-container div
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
});
