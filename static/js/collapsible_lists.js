document.addEventListener("DOMContentLoaded", function () {
  setTimeout(initCollapsibles, 100);
});

document.addEventListener("collapsiblesInitialized", function () {
  setTimeout(uncollapseActiveFolder, 100);
});

function initCollapsibles() {
  console.log("Initializing collapsibles");
  var elems = document.querySelectorAll(".collapsible");
  
  elems.forEach(function (elem) {
    M.Collapsible.init(elem, {
      accordion: false,
      onOpenEnd: function () {
        updateAllChevrons();
      },
      onCloseEnd: function () {
        updateAllChevrons();
      }
    });
  });

  // Add event listeners to update the chevron when collapsible is opened or closed
  var headers = document.querySelectorAll(".collapsible .collapsible-header");
  headers.forEach(function (header) {
    header.addEventListener("click", function (event) {
      setTimeout(updateAllChevrons, 100);
    });
  });

  // Dispatch a custom event when collapsibles are initialized
  var event = new Event("collapsiblesInitialized");
  document.dispatchEvent(event);
}



function updateChevron(element) {
  var chevron = element.querySelector(".collapsible-header i");
  if (chevron) {
    if (element.classList.contains("active")) {
      chevron.textContent = "expand_more";
    } else {
      chevron.textContent = "chevron_right";
    }
  }
}

function updateAllChevrons() {
  var collapsibleHeaders = document.querySelectorAll(".collapsible li");
  collapsibleHeaders.forEach(function (element) {
    updateChevron(element);
  });
}

function openParentCollapsibles(element) {
  let parentCollapsible = element.closest(".collapsible");
  if (!parentCollapsible) {
    return;
  }

  let parentLi = parentCollapsible.closest("li");
  if (!parentLi) {
    return;
  }

  let index = Array.from(parentLi.parentNode.children).indexOf(parentLi);
  let collapsibleInstance = M.Collapsible.getInstance(
    parentLi.closest(".collapsible")
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

  console.log("activeFolderName:", activeFolderName);

  var links = Array.from(document.querySelectorAll(".collapsible a[data-folder], .collapsible div.collapsible-header[data-folder]"));

  var activeLink = links.find(function (element) {
    var elementFolder = element.getAttribute("data-folder");
    return elementFolder === activeFolderName;
  });

  if (activeLink) {
    var parentLi = activeLink.closest("li");
    parentLi.classList.add("active");
    openParentCollapsibles(parentLi);
  }
}
