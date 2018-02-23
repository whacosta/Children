(function($) {
  "use strict";
  
  var core = {
    init: function(){
      // Closes the panel
      $('.panel-heading .panel-action > .btn-close').on('click', core.panelClose);
      // Minimizes the panel
      $('.panel-heading .panel-action > .btn-min').on('click', core.panelMin);
      // Expands the panel
      $('.panel-heading .panel-action > .btn-expand').on('click', core.panelExpand);

      // Checking if bootstrap popover isn't initialized
      if( !$('[data-toggle="popover"]').data('bs.popover') ){
        // Popover contextual variants
        core.popoverVariants('success');
        core.popoverVariants('info');
        core.popoverVariants('warning');
        core.popoverVariants('danger');
      }

      // Full height panel
      if( $('.panel-full-height').length > 0 ){
        $('.panel-full-height').css('height',$(document).height() - $('.content-wrapper').offset().top+'px' );
      }
    },
    panelClose: function(){
      $(this).closest('.panel').remove();
    },
    panelMin: function(){
      $(this).toggleClass('btn-min btn-plus').closest('.panel').find('.panel-body').slideToggle();
    },
    panelExpand: function(){
      $(this).toggleClass('btn-expand btn-compress').closest('.panel').toggleClass('panel-fixed');

      if( $(this).closest('.panel-fixed') ){
        $('head').append('<style type="text/css" data-type="temp-style">.panel-fixed{position: fixed; top: 0; right: 0; bottom: 0; left: 0; margin-bottom: 0 !important; z-index: 1100;}.panel-fixed .panel-body{max-height: '+$(window).height()+'px'+';overflow: auto;}</style>');
      }else{
        $('head style[data-type="temp-style"]').remove();
      }
    },
    popoverVariants: function(variant){
      $('[data-theme="popover-'+variant+'"]').popover({
        template: '<div class="popover"><div class="arrow"></div><h3 class="popover-title bg-'+variant+'"></h3><div class="popover-content"></div></div>'
      })
    }
  };

  core.init();
})(jQuery);