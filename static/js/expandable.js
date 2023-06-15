$(document).ready(function () {
  var mdPath = window.location.pathname;
  if (mdPath.startsWith("/view-md/")) {
    $.ajax({
      url: mdPath,
      type: "GET",
      success: function (data) {
        if (data.status === "redirect") {
          window.location.href = data.url;
        } else {
          $("#playbook-container").html(data);
        }
      },
      error: function () {
        console.log("Error loading content");
      },
    });
  }
  $("#menu-links, .search-results").on("click", "a", function (e) {
    e.preventDefault();
    var url = $(this).attr("href");
    $("#playbook-container").load(url, function () {
      window.history.pushState({ path: url }, "", url);
      $(window).scrollTop(0);
    });
  });
  // Attach click event to buttons with aria-controls attribute
  $("[aria-controls]").on("click", function () {
    const button = $(this);
    const targetId = button.attr("aria-controls").replace(" ", "-");
    const target = $(`#${targetId}`);
    const targetUl = target.children("ul"); // Find the direct child ul element
    const isExpanded = button.attr("aria-expanded") === "true";

    // Close other menus and reset their chevrons
    $("[aria-controls]")
      .not(this)
      .each(function () {
        const otherButton = $(this);
        const otherTargetId = otherButton.attr("aria-controls");
        const otherTarget = $(`#${otherTargetId}`);
        const otherTargetUl = otherTarget.children("ul"); // Find the direct child ul element

        if (!button.parents("li").has(otherButton).length) {
          otherButton.attr("aria-expanded", false);
          otherButton
            .find("svg")
            .removeClass("rotate-90 text-gray-500")
            .addClass("text-gray-400");
          otherTargetUl.slideUp().addClass("collapsed-menu");
        }
      });

    // Collapse sibling elements
    button
      .closest("li")
      .siblings()
      .each(function () {
        const siblingButton = $(this).find("[aria-controls]").first();
        const siblingTargetId = siblingButton.attr("aria-controls");
        const siblingTarget = $(`#${siblingTargetId}`);
        const siblingTargetUl = siblingTarget.children("ul"); // Find the direct child ul element

        siblingButton.attr("aria-expanded", false);
        siblingButton
          .find("svg")
          .removeClass("rotate-90 text-gray-500")
          .addClass("text-gray-400");
        siblingTargetUl.slideUp().addClass("collapsed-menu");
      });

    // Toggle expanded state
    button.attr("aria-expanded", !isExpanded);

    // Toggle chevron icon
    if (!isExpanded) {
      button
        .find("svg")
        .addClass("rotate-90 text-gray-500")
        .removeClass("text-gray-400");
      targetUl.removeClass("collapsed-menu").removeAttr("style");
    } else {
      button
        .find("svg")
        .removeClass("rotate-90 text-gray-500")
        .addClass("text-gray-400");
      targetUl.addClass("collapsed-menu");
    }
  });
});
