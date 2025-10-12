/* ==========================================================================
   jQuery plugin settings and other scripts
   ========================================================================== */

$(document).ready(function(){
  // Sticky footer
  var bumpIt = function() {
      $("body").css("margin-bottom", $(".page__footer").outerHeight(true));
    },
    scheduleBump = (function() {
      var scheduled = false;
      var enqueue =
        window.requestAnimationFrame ||
        function(callback) {
          return window.setTimeout(callback, 16);
        };
      return function() {
        if (scheduled) {
          return;
        }
        scheduled = true;
        enqueue(function() {
          scheduled = false;
          bumpIt();
        });
      };
    })();

  bumpIt();

  $(window).on("resize", scheduleBump);
  // FitVids init
  $("#main").fitVids();

  // init sticky sidebar
  $(".sticky").Stickyfill();

  var $authorWrapper = $(".author__urls-wrapper");
  var $authorToggle = $authorWrapper.find("button");
  var $authorList = $authorWrapper.find(".author__urls");

  var setAuthorVisibility = function(expanded) {
    if ($authorList.length === 0) {
      return;
    }
    var isExpanded = Boolean(expanded);
    if ($authorToggle.length) {
      $authorToggle.attr("aria-expanded", isExpanded);
    }
    if (isExpanded) {
      $authorList.attr("aria-hidden", "false").removeAttr("hidden").show();
    } else {
      $authorList.attr("aria-hidden", "true").attr("hidden", "hidden").hide();
    }
  };

  var stickySideBar = function(){
    var show = $(".author__urls-wrapper button").length === 0 ? $(window).width() > 1024 : !$(".author__urls-wrapper button").is(":visible");
    // console.log("has button: " + $(".author__urls-wrapper button").length === 0);
    // console.log("Window Width: " + windowWidth);
    // console.log("show: " + show);
    //old code was if($(window).width() > 1024)
    if (show) {
      // fix
      Stickyfill.rebuild();
      Stickyfill.init();
      setAuthorVisibility(true);
    } else {
      // unfix
      Stickyfill.stop();
      setAuthorVisibility(false);
    }
  };

  stickySideBar();

  $(window).resize(function(){
    stickySideBar();
  });

  // Follow menu drop down

  if ($authorToggle.length) {
    setAuthorVisibility(!$authorToggle.is(":visible"));

    $authorToggle.on("click", function() {
      var expanded = $authorToggle.attr("aria-expanded") === "true";
      setAuthorVisibility(!expanded);
      $authorToggle.toggleClass("open", !expanded);
    });
  }

  // init smooth scroll
  $("a").smoothScroll({offset: -20});

  // add lightbox class to all image links
  $("a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.png'],a[href$='.gif']").addClass("image-popup");

  // Magnific-Popup options
  $(".image-popup").magnificPopup({
    // disableOn: function() {
    //   if( $(window).width() < 500 ) {
    //     return false;
    //   }
    //   return true;
    // },
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      tError: '<a href="%url%">Image #%curr%</a> could not be loaded.',
    },
    removalDelay: 500, // Delay in milliseconds before popup is removed
    // Class that is added to body when popup is open.
    // make it unique to apply your CSS animations just to this exact popup
    mainClass: 'mfp-zoom-in',
    callbacks: {
      beforeOpen: function() {
        // just a hack that adds mfp-anim class to markup
        this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure mfp-with-anim');
      }
    },
    closeOnContentClick: true,
    midClick: true // allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source.
  });

});
