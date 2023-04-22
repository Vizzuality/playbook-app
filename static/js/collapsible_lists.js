
function initCollapsibles() {
    console.log("Initializing collapsibles");
    var elems = document.querySelectorAll(".collapsible");
    var instances = M.Collapsible.init(elems, {accordion: false});
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
  let collapsibleInstance = M.Collapsible.getInstance(parentLi.closest(".collapsible"));

  collapsibleInstance.open(index);
  openParentCollapsibles(parentLi);
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
  let collapsibleInstance = M.Collapsible.getInstance(parentLi.closest(".collapsible"));

  collapsibleInstance.open(index);
  openParentCollapsibles(parentLi);
}

function uncollapseActiveFolder() {
  {% if active_folder %}
    var activeFolderPath = "{{ active_folder }}";
    console.log("activeFolderPath:", activeFolderPath);

    var lastFolder = activeFolderPath.split('/').slice(-1)[0];
    var decodedLastFolder = decodeURIComponent(lastFolder);
    console.log("decodedLastFolder:", decodedLastFolder);

    var links = Array.from(document.querySelectorAll('.collapsible a')).filter(function(a) {
      return a.href.includes(decodedLastFolder);
    });

    if (links.length > 0) {
      var link = links[0];
      var parentLi = link.closest("li");

      if (link.href) {
        parentLi.classList.add("active");
      } else {
        openParentCollapsibles(parentLi);
      }
    }
  {% endif %}
}

document.addEventListener("DOMContentLoaded", function() {
  initCollapsibles();
  uncollapseActiveFolder();
});




document.addEventListener("DOMContentLoaded", function() {
  initCollapsibles();
  uncollapseActiveFolder();
});



