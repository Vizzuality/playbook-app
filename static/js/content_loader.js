$(document).ready(function () {
    initCollapsibles();
  
    // Load the default content or the content specified in the URL
    let contentUrl = "default_content"; // Replace with the actual default content URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("url")) {
      contentUrl = urlParams.get("url");
    }
    loadContent(contentUrl);
  });
  
  function loadContent(url) {
    $.get(`/view-md/${url}`, function (data) {
      $("#content").html(data);
    });
  }