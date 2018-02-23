(function($){
  'use strict';

  var dashboard = {
		// Device check
		device: 				'ontouchstart' in document.documentElement,
		$navbarTop: 		$('.navbar-top'),
		$sidebarExtra: 	$('.sidebar-extra'),
		$content: 			$('.content'),
		$sidebar: 			$('.sidebar'),
		$sidebarFixed: 	$('.sidebar-fixed'),
		$sidebarNav: 		$('.sidebar-nav'),

		init: function(){
	    // Prevents dropdown links
	    $('[data-click="prevent"]').on('click', dashboard.preventDef);

	    // Navbar
	    // Dropdown fix for IOS (adding backdrop)
	    dashboard.$navbarTop.find('.dropdown').on('show.bs.dropdown hide.bs.dropdown', dashboard.navbarDropdownIOS);

		// Button which opens/closes the sidebar
		dashboard.$navbarTop.find('.sidebar-toggle').on('click', dashboard.sidebarToggle);

		// Navbar form button
		dashboard.$navbarTop.find('.navbar-form .btn').on('click', dashboard.navbarFormBtn);

		// Sidebar extra
		// Prevents notifications dropdown and sidebar extra from closing on self click
		dashboard.$sidebarExtra.on('click', dashboard.stopProp);

		// Custom scrollbar for notifications, messages, tasks dropdowns
		//Function Arguments: selector, color
	  	dashboard.slimscrollInit('.list-dropdown-notifications', '#777');
	  	dashboard.slimscrollInit('.list-dropdown-messages', '#777');
	  	// dashboard.slimscrollInit('.list-dropdown-tasks', '#777');

	    // Inits sidebar extra tabs
			//dashboard.$sidebarExtra.find('.nav-tabs a').on('click', dashboard.tabInit);

			// Custom scrollbar for .sidebar-extra
			//dashboard.slimscrollInit('.sidebar-extra-scroller', '#fff');

	    // Custom switches
	    //dashboard.bootstrapSwitchInit('.sidebar-extra .bs-switch');

	    // Makes text succinct
	    //dashboard.succinctInit('#sidebar-timeline', 60);
	    //dashboard.succinctInit('#sidebar-mail', 22);

	    // Sidebar
			// Sidebar dropdown functionality
		dashboard.$sidebarNav.find('.dropdown > a').on('click', dashboard.sidebarDropdown);

			// Fixed sidebar
		if( $('.sidebar').hasClass('sidebar-fixed') && $('.sidebar-fixed').is(':visible') ){
			// Custom scrollbar
			dashboard.slimscrollInit('.sidebar-fixed-scroller', '#fff');
		}
		// When sidebar is fixed and toggled to small, this function shows the sidebar in default large width when you hover it.
		dashboard.$sidebarFixed.on('mouseenter mouseleave', dashboard.sidebarSmFixedMouseOver);

		// Shows sidebar active link
		dashboard.sidebarActiveLinkInit();

		// Page height configuration
		dashboard.pageHeight();
		},

		stopProp: function(e){
		  e.stopPropagation();
		},
		 preventDef: function(e){
		   e.preventDefault();
		    e.returnValue = false;
	    },
		slimscrollInit: function(el, color){
	    if(!dashboard.device){
	    	if( !$(el).height().length > 0 ){
		      $(el).closest('.dropdown-menu').css({
		        'display': 'block',
		        'visibility': 'hidden'
		      });
		    }

		    $(el).slimScroll({
		    	width: $(el).width(),
		      height: $(el).height(),
		      allowPageScroll: true,
		      wheelStep: 24,
		      color: color
		    });

		    if( !$(el).height().length > 0 ){
		      $(el).closest('.dropdown-menu').removeAttr('style');
		    }
	    }
	  },
	  bootstrapSwitchInit: function(el){
	    $(el).bootstrapSwitch('onColor', 'info');
	  },
	  succinctInit: function(el, size){
	    $(el+' .text-ellipsis').succinct({
	      size: size
	    });
	  },
		tabInit: function(e){
	    e.preventDefault();
	    $(this).tab('show');
		},
		navbarDropdownIOS: function(e){
			if( /iPhone|iPad|iPod/i.test(navigator.userAgent) ){
				// Checking for Apple devices
				if( e.type == 'show' ){
					$('body').append('<div class="dropdown-backdrop"></div>');
		    	$('.dropdown-backdrop').css('cursor', 'pointer');
				}else if( e.type == 'hide' ){
		    	$('.dropdown-backdrop').remove();
				}
			}
		},
		navbarFormBtn: function(){
			if( $(this).closest('form').find('.form-control').is(':visible') && $(this).closest('form').find('.form-control').css('position') != 'absolute' ){
				$(this).attr('type', 'submit');
			}else{
				$(this).attr('type', 'button');
				$(this).closest('form').toggleClass('open');
			}
		},
		sidebarToggle: function(){
			if( dashboard.$sidebar.css('float') == 'none' && dashboard.$sidebar.css('position') != 'fixed' ){
				// Sliding up/down sidebar for mobile view
				if( dashboard.$sidebar.css('display') == 'none' ){
					dashboard.$sidebar.slideDown(300);

					dashboard.$sidebar.css('min-height', 'inherit');
				}else{
					dashboard.$sidebar.slideUp(300, function(){
						$(this).removeAttr('style');

						dashboard.pageHeight();
					});
				}
			}else{
				$('body').toggleClass('has-sidebar-sm');

				dashboard.pageHeight();
			}
		},
		sidebarDropdown: function(){
	    if( !$('body').hasClass('has-sidebar-sm') && !dashboard.$sidebar.hasClass('sidebar-hover') || dashboard.$sidebar.css('float') == 'none' ){
	    	// Opens dropdowns
	    	dashboard.sidebarDropdownClick( $(this) );
	    }

	    if( $('body').hasClass('has-sidebar-sm') && $(this).parent('.dropdown').parent().closest('.dropdown').length > 0 ){
	    	// Small sidebar
	    	// Opens inner level dropdowns
	    	dashboard.sidebarDropdownClick( $(this) );
	    }

	    if( !$('body').hasClass('has-sidebar-sm') && dashboard.$sidebar.hasClass('sidebar-hover') && $(this).parent('.dropdown').parent().closest('.dropdown').length > 0 ){
	    	// Hover sidebar
	    	// Opens inner level dropdowns
	    	dashboard.sidebarDropdownClick( $(this) );
	    }
		},
		sidebarDropdownClick: function( $this ){
			var $dropdown = $this.parent();
	    var $innerMenu = $this.next();

			if( !$dropdown.hasClass('open') ){
				$dropdown.siblings().find('.inner-nav').slideUp(300, function(){
					$this.removeAttr('style');
				});
				
				$innerMenu.slideDown(300, function(){
					$dropdown.addClass('open').siblings().removeClass('open');
					$innerMenu.removeAttr('style');

					// if( !dashboard.$sidebar.hasClass('sidebar-fixed') && !$('body').hasClass('has-sidebar-sm') || dashboard.$sidebar.css('float') == 'none' ){
					// 	// Page scroll
					// 	$('html, body').animate({
				 //    	scrollTop: $dropdown.offset().top - dashboard.$navbarTop.height()
				 //    }, 500);
					// }

					if( dashboard.$sidebar.css('float') != 'none' ){
						//	Mobile view when sidebar is hidden
						// As sidebar height is changing when dropdown is open, we set sidebar min-height to inherit and run pageHeight().
						dashboard.$sidebar.css('min-height', 'inherit');
						dashboard.pageHeight();
					}
				});
	    }else{
	    	$innerMenu.slideUp(300, function(){
	    		$dropdown.removeClass('open');
	    		$innerMenu.removeAttr('style');

	    		if( dashboard.$sidebar.css('float') != 'none' ){
	    			//	Mobile view when sidebar is hidden
	    			// As sidebar height is changing when dropdown is closed, we set sidebar min-height to inherit and run pageHeight().
		    		dashboard.$sidebar.css('min-height', 'inherit');
		    		dashboard.pageHeight();
	    		}
	    	});
	    }

	    if( $this.closest('.sidebar-nav').hasClass('sidebar-nav-h') ){
				$this.closest('.sidebar-nav').siblings('.sidebar-nav').find('li.open').removeClass('open');
			}
		},
		sidebarSmFixedMouseOver: function(e){
			if( dashboard.$sidebar.hasClass('sidebar-fixed') && dashboard.$sidebarFixed.is(':visible') ){
				if( e.type == 'mouseenter' && dashboard.$sidebarFixed.css('position') == 'fixed' ){
					if( $('body').hasClass('has-sidebar-sm') ){
						$('body').removeClass('has-sidebar-sm').addClass('has-sidebar-fixed');
					}
				}else if( e.type == 'mouseleave' && $('body').hasClass('has-sidebar-fixed') ){
					$('body').addClass('has-sidebar-sm').removeClass('has-sidebar-fixed');
				}
			}
		},

		sidebarActiveLinkInit: function(){
			var url;
		  var fileName;

		  url = window.location.pathname;
		  url = url.split('/');
		  fileName = url[url.length -1];

		  dashboard.$sidebarNav.find('a').each(function(){
		    var aHref = $(this).attr('href');

		    if( aHref == fileName ){
		      $(this).parent().addClass('active').parents('.dropdown').addClass('open active');
		    }
		  });
		},
		pageHeight: function(){
	    if( dashboard.$sidebar.outerHeight() > $(window).height() ){
	    	dashboard.$sidebar.css('min-height', dashboard.$sidebar.outerHeight());
	    	dashboard.$content.css('min-height', dashboard.$sidebar.outerHeight());
	    }else{
	    	dashboard.$sidebar.css('min-height', $(window).height());
	    	dashboard.$content.css('min-height', $(window).height());
	    }
		}
	};
  
  dashboard.init();
})(jQuery);