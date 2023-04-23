$(document).ready(function () {
  initCollapsibles();
});

$(document).on("collapsiblesInitialized", function () {
  uncollapseActiveFolder();
});

function updateChevron(element) {
  var chevron = $(element).find(".collapsible-header i");
  if (chevron.length) {
    if ($(element).hasClass("active")) {
      chevron.text("expand_more");
    } else {
      chevron.text("chevron_right");
    }
  }
}

function updateAllChevrons() {
  $(".collapsible li").each(function () {
    updateChevron(this);
  });
}

function initCollapsibles() {
  var elems = $(".collapsible");
  var instances = M.Collapsible.init(elems.get(), { accordion: false });

  $(".collapsible .collapsible-header").on("click", function (event) {
    setTimeout(updateAllChevrons, 100);
  });

  var event = jQuery.Event("collapsiblesInitialized");
  $(document).trigger(event);
}

function openParentCollapsibles(element) {
  let parentCollapsible = $(element).closest(".collapsible");
  if (!parentCollapsible.length) {
    return;
  }

  let parentLi = parentCollapsible.closest("li");
  if (!parentLi.length) {
    return;
  }

  let index = parentLi.parent().children().index(parentLi);
  let collapsibleInstance = M.Collapsible.getInstance(
    parentLi.closest(".collapsible").get(0)
  );

  collapsibleInstance.open(index);
  openParentCollapsibles(parentLi.closest(".collapsible"));
}

function uncollapseActiveFolder() {
  var urlParams = new URLSearchParams(window.location.search);
  var activeFolderName = urlParams.get("folder");
  updateAllChevrons();
  if (!activeFolderName) {
    return;
  }

  var links = $(".collapsible a[data-folder], .collapsible div.collapsible-header[data-folder]").toArray();

  var activeLink = links.find(function (element) {
    var elementFolder = $(element).attr("data-folder");
    return elementFolder === activeFolderName;
  });

  if (activeLink) {
    var parentLi = $(activeLink).closest("li");
    parentLi.addClass("active");
    openParentCollapsibles(parentLi);
  }
}
