var grab_start=0;
function get_grab(){
  params={'start':grab_start}
  $.ajax({
    
		type: 'POST',
		url:'/bt/grab',
		data: JSON.stringify(params),
		contentType: "application/json; charset=utf-8", 
		dataType:"json",
		success: function(response) {
		        //$(document).trigger("report_submitted_event",response);				
			if(response.result==1){
				alert('aaaa')
				data=response.data;
				grab_start=response.end
				var tt,html,sec1
				for (item in data){
					html=""
					tt=data[item]
					console.log(item)
					console.log(data[item])
					sec1=""
					sec1+="<a href="+tt.url+" target=_blank>"+tt.title+"</a></br>"
					sec1+="tag:"+tt.tag+" text</br>"
					for (cc in tt.content.items){
						//console.log(cc)
						sec1+=cc+":"+ tt.content.items[cc]+"</br>"
					}
					sec1+="btfile:<a href='/btfiles/"+tt.btfile+"'>"+tt.btfile+"</a></br>"
					sec1+="images:"+tt.images.length+"</br>"
					for ( cc in tt.images){
						sec1+="<img src=/btimgs/"+tt.images[cc][1]+">"
					}

					html='<div class="tabbable">'
					html+='	<ul class="nav nav-tabs navbar-inner">'
					html+='	  <li class="active"><a href="#tab'+(grab_start-item)+'_1" data-toggle="tab">grab</a></li>'
					html+='	  <li><a href="#tab'+(grab_start-item)+'_2" data-toggle="tab">origin</a></li>'
					html+='	</ul>'
					html+='	<div class="tab-content">'
					html+='	  <div class="tab-pane active" id="tab'+(grab_start-item)+'_1">'
					html+='		<p>'+sec1+'</p>'
					html+='	  </div>'
					html+='	  <div class="tab-pane" id="tab'+(grab_start-item)+'_2">'
					html+='		<p>'+tt.raw_content+'</p>'
					html+='	  </div>'
					html+='	</div>'
					html+='</div>'
					console.log(html)
					/*
					html+="<li class='span5'>"
					html+="<div class=thumbnail>"
					html+="<a href="+tt.url+" target=_blank>"+tt.title+"</a></br>"
					html+="tag:"+tt.tag+" text</br>"
					for (cc in tt.content.items){
						console.log(cc)
						html+=cc+":"+ tt.content.items[cc]+"</br>"
					}
					html+="btfile:"+tt.btfile+"</br>"
					html+="images:"+tt.images.length+"</br>"
					html+="</div>"
					html+="</li>"
					*/
					$('.grab ul.thumbnails').append(html)
				}
			}
			else{
				alert(response.error)
			}

		},
		error: function(jqXHR,textStatus,error) {
			alert(error)
		}
		
  })
}





!function ($) {

  "use strict"; // jshint ;_;


 /* TAB CLASS DEFINITION
  * ==================== */

  var Tab = function ( element ) {
    this.element = $(element)
  }

  Tab.prototype = {

    constructor: Tab

  , show: function () {
      var $this = this.element
        , $ul = $this.closest('ul:not(.dropdown-menu)')
        , selector = $this.attr('data-target')
        , previous
        , $target
        , e

      if (!selector) {
        selector = $this.attr('href')
        selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') //strip for ie7
      }

      if ( $this.parent('li').hasClass('active') ) return

      previous = $ul.find('.active a').last()[0]

      e = $.Event('show', {
        relatedTarget: previous
      })

      $this.trigger(e)

      if (e.isDefaultPrevented()) return

      $target = $(selector)

      this.activate($this.parent('li'), $ul)
      this.activate($target, $target.parent(), function () {
        $this.trigger({
          type: 'shown'
        , relatedTarget: previous
        })
      })
    }

  , activate: function ( element, container, callback) {
      var $active = container.find('> .active')
        , transition = callback
            && $.support.transition
            && $active.hasClass('fade')

      function next() {
        $active
          .removeClass('active')
          .find('> .dropdown-menu > .active')
          .removeClass('active')

        element.addClass('active')

        if (transition) {
          element[0].offsetWidth // reflow for transition
          element.addClass('in')
        } else {
          element.removeClass('fade')
        }

        if ( element.parent('.dropdown-menu') ) {
          element.closest('li.dropdown').addClass('active')
        }

        callback && callback()
      }

      transition ?
        $active.one($.support.transition.end, next) :
        next()

      $active.removeClass('in')
    }
  }


 /* TAB PLUGIN DEFINITION
  * ===================== */

  $.fn.tab = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('tab')
      if (!data) $this.data('tab', (data = new Tab(this)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.tab.Constructor = Tab


 /* TAB DATA-API
  * ============ */

  $(function () {
    $('body').on('click.tab.data-api', '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
      e.preventDefault()
      $(this).tab('show')
    })
  })

}(window.jQuery);
