
(function( $ ){	
	
	$.fn.calm = function(startOnInit) {
		function Calm($el, startOnInit){
			var $el = $el;
			var timeout;
			var opts = {
			  lines: 11, 
			  length: 6, 
			  width: 3, 
			  radius: 5, 
			  rotate: 0, 
			  color: '#fff', 
			  speed: 1, 
			  trail: 50, 
			  shadow: false, 
			  hwaccel: true, 
			  className: 'spinner',
			  zIndex: 2e9, // The z-index (defaults to 2000000000)
			};
			this.start = function(){
				$el.addClass('stayActive');
				timeout = setTimeout(function(){
					var position = $el.position();
					var position = $el.position();
					var spinner = new Spinner(opts).spin();
					$(spinner.el).insertAfter($el).css({
						'position' : 'absolute',
						'top' : position.top + $el.outerHeight() / 2,
						'left': position.left+ $el.outerWidth() / 2
					});
				}, 1500);
			}
			
			this.stop = function(){
				clearTimeout(timeout);
				$el.removeClass('stayActive');
			}
			
			$el.click(this.start);
			
			if(startOnInit){
				this.start();
			}
		}
		return this.each(function() {
			var $this = $(this);
			if( !$this.data('calm') ){
				var c = new Calm($this, startOnInit);
				$this.data('calm', c);
			}
		});
	};
	
	$.fn.flash = function() {
		var $header = $('#header_one');
		var header_position = $('#header_one').position();
		return this.each(function() {
			var $this = $(this);
			$this.click(function(){
				$this.clearQueue().slideUp()
			});
			$this.css({'top':header_position.top, 'left':header_position.left, 'display': 'none'});
			$this.delay(300).slideDown().delay(3000).slideUp();
		});
	};
	
	// vcenter to footer
	$.fn.vcenter = function() {
		return this.each(function() {
			var $this = $(this);
			var h = $('#footer').offset().top - $this.offset().top - 44;
			$this.css({'height': h});
		});
	}
	
	
})(jQuery);

/*
$(function(){
	$('#flash').flash();
	$('.vcenter').vcenter();	
});
*/