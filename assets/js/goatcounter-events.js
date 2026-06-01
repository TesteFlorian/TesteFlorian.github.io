(function() {
  "use strict";

  if (window.goatcounterLinkTracking) {
    return;
  }
  window.goatcounterLinkTracking = true;

  var trackedFile = /\.(csv|docx?|pdf|pptx?|qmd|rda|rds|tiff?|tsv|xlsx?|zip)$/i;

  function onReady(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
    } else {
      callback();
    }
  }

  function slugify(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/^https?:\/\//, "")
      .replace(/[?#].*$/, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 96) || "link";
  }

  function compact(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function currentPage() {
    return window.location.pathname || "/";
  }

  function linkLabel(link, url) {
    return compact(
      link.getAttribute("aria-label") ||
      link.getAttribute("title") ||
      link.textContent ||
      url.pathname ||
      url.href
    );
  }

  function fileEvent(link, url) {
    var match = url.pathname.match(trackedFile);

    if (!match && !link.hasAttribute("download")) {
      return null;
    }

    var filename = url.pathname.split("/").filter(Boolean).pop() || "download";
    var basename = filename.replace(/\.[^.]+$/, "");
    var extension = match ? match[1].toLowerCase().replace(/^tiff$/, "tif") : "file";

    return {
      path: "download-" + extension + "-" + slugify(basename),
      title: compact("Download: " + filename + " from " + currentPage()).slice(0, 180)
    };
  }

  function contactEvent(url) {
    if (url.protocol === "mailto:") {
      return {
        path: "contact-email",
        title: compact("Email link from " + currentPage()).slice(0, 180)
      };
    }

    if (url.protocol === "tel:") {
      return {
        path: "contact-phone",
        title: compact("Phone link from " + currentPage()).slice(0, 180)
      };
    }

    return null;
  }

  function outboundEvent(link, url) {
    if (!/^https?:$/.test(url.protocol) || url.hostname === window.location.hostname) {
      return null;
    }

    var host = url.hostname.replace(/^www\./, "");
    var pathParts = url.pathname.split("/").filter(Boolean).slice(0, 2).join("-");
    var eventName = "outbound-" + slugify(host + (pathParts ? "-" + pathParts : ""));

    return {
      path: eventName,
      title: compact("Outbound: " + host + " - " + linkLabel(link, url) + " from " + currentPage()).slice(0, 180)
    };
  }

  function eventFor(link) {
    var href = link.getAttribute("href");
    var url;

    if (!href || link.hasAttribute("data-goatcounter-click") || link.hasAttribute("data-goatcounter-ignore")) {
      return null;
    }

    try {
      url = new URL(href, window.location.href);
    } catch (error) {
      return null;
    }

    return fileEvent(link, url) || contactEvent(url) || outboundEvent(link, url);
  }

  function annotateLinks() {
    var links = document.querySelectorAll("a[href]");

    for (var i = 0; i < links.length; i += 1) {
      var link = links[i];
      var event = eventFor(link);

      if (!event) {
        continue;
      }

      link.setAttribute("data-goatcounter-click", event.path);
      link.setAttribute("data-goatcounter-title", event.title);
      link.setAttribute("data-goatcounter-referrer", currentPage());
      link.setAttribute("data-goatcounter-no-session", "1");
    }
  }

  onReady(annotateLinks);
}());
