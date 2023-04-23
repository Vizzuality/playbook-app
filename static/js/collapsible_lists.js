document.addEventListener("DOMContentLoaded", function () {
  initCollapsibles();
});

document.addEventListener("collapsiblesInitialized", function () {
  uncollapseActiveFolder();
});

function initCollapsibles() {
  console.log("Initializing collapsibles");
  var elems = document.querySelectorAll(".collapsible");
  var instances = M.Collapsible.init(elems, { accordion: false });

  // Dispatch a custom event when collapsibles are initialized
  var event = new Event("collapsiblesInitialized");
  document.dispatchEvent(event);
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




// function uncollapseActiveFolder() {
//   var urlParams = new URLSearchParams(window.location.search);
//   var activeFolderName = urlParams.get("folder");
//   if (!activeFolderName) {
//     return;
//   }

//   console.log("activeFolderName:", activeFolderName);

//   var links = Array.from(document.querySelectorAll(".collapsible a, .collapsible div.collapsible-header"));

//   var activeLink = links.find(function (element) {
//     return element.textContent.includes(activeFolderName);
//   });

//   if (activeLink) {
//     var parentLi = activeLink.closest("li");
//     parentLi.classList.add("active");
//     openParentCollapsibles(parentLi);
//   }
// }

// uncollapseActiveFolder();

function uncollapseActiveFolder() {
  var urlParams = new URLSearchParams(window.location.search);
  var activeFolderName = urlParams.get("folder");
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
