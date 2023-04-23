function removeNonAlphanumeric(str) {
  return str.replace(/[^a-zA-Z0-9]/g, "");
}

function scrollToHeading(hash) {
  const anchorText = removeNonAlphanumeric(
    decodeURIComponent(hash.substring(1)).toLowerCase()
  );
  const headings = $("h1, h2, h3, h4, h5, h6");
  const targetHeading = headings.toArray().find(
    (heading) =>
      removeNonAlphanumeric($(heading).text().toLowerCase()) ===
      anchorText
  );

  if (targetHeading) {
    targetHeading.scrollIntoView({
      behavior: "smooth",
      block: "start",
      inline: "nearest",
    });
  }
}

function init() {
  if (window.location.hash) {
    const hash = window.location.hash;
    console.log("Hash:", hash);
    scrollToHeading(hash);
  }
}

if (document.readyState === "loading") {
  $(document).ready(init);
} else {
  init();
}

$(document).on("click", function (event) {
  const target = $(event.target).closest('a[href^="#"]');

  if (target.length) {
    event.preventDefault();
    const hash = target.attr("href");

    if (hash) {
      scrollToHeading(hash);
      window.history.pushState(null, "", hash); // Update the URL to include the hash
    }
  }
});
