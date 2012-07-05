var grab_start=0;
var pub_start=0;
var cur_view="grab"

function change_view(name){
	$("."+cur_view).hide();
	$("."+cur_view+"_menu").removeClass('active');
	cur_view=name
	$("."+cur_view).show();
	$("."+cur_view+"_menu").addClass('active');
}

$(".grab_more").live('click',function(){
    $(".grab_more").html('loading')
    $(".grab_more").attr("disabled", "disabled");
    get_grab();
})
$(".pub_more").live('click',function(){
    $(".pub_more").html('loading')
    $(".pub_more").attr("disabled", "disabled");
    get_pub();
})
function get_grab(){
  params={'start':grab_start}
  $.ajax({
    
		type: 'POST',
		url:'/bt/grab',
		data: JSON.stringify(params),
		contentType: "application/json; charset=utf-8", 
		dataType:"json",
		success: function(response) {
			if(response.result==1){
				data=response.data;
				grab_start=response.end
				var tt,html,sec1,sec3
				var len=0
				if(data)
					len = data.length;
				for (item in data){
					html=""
					tt=data[item]
					//console.log(item)
					grab_time=new Date(tt['grab_time']*1000)
					sec1="No."+(grab_start-(len-item))+" grab at "+grab_time.getDate()+" "+(grab_time.getMonth()+1)+" "+grab_time.getFullYear()+" "+grab_time.getHours()+":"+grab_time.getMinutes()+":"+grab_time.getSeconds()+"<br>"
					sec1+="<a href="+tt.url+" target=_blank>"+tt.title+"</a></br>"
					sec1+="tag:"+tt.tag+" <button class='btn btn-info' onclick=publish('"+tt.url+"')>pub</button></br>"
					for (cc in tt.content.items){
						//console.log(cc)
						sec1+="<b>"+cc+"</b>:"+ tt.content.items[cc]+"</br>"
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
					$('.grab ul.thumbnails').append(html)
				}
			    if(response.is_end){
				$(".grab_more").html('end')
				$(".grab_more").attr("disabled", "disabled");
			    }else{
			    	$(".grab_more").html('more')
			    	$(".grab_more").removeAttr("disabled");   
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


function publish(url){
  params={'url':url}
  $.ajax({

                type: 'POST',
                url:'/bt/pub',
                data: JSON.stringify(params),
                contentType: "application/json; charset=utf-8",
                dataType:"json",
                success: function(response) {
			console.log(response)
			if(response.result==1){
				alert(response.data)
			}else{
				alert(response.error)
			}
		},
                error: function(jqXHR,textStatus,error) {
                        alert(error)
                }

  })

}


function get_pub(){
  params={'start':pub_start}
  console.log("test:"+pub_start)
  $.ajax({

                type: 'GET',
                url:'/bt/pub/'+pub_start,
                data: JSON.stringify(params),
                contentType: "application/json; charset=utf-8",
                dataType:"json",
                success: function(response) {
                        //$(document).trigger("report_submitted_event",response);              
                        if(response.result==1){
                                data=response.data;
                                pub_start=response.end
				console.log("bbb:"+pub_start)
                                var tt,html,sec1
				var len=0
				if(data)
					len= data.length
                                for (item in data){
                                        html=""
                                        tt=data[item]
                                        console.log(item)
                                        console.log(data[item])
					var pub_time=new Date(tt['grab_time']*1000)
					sec3=""
					sec3+="url: <a href='"+tt.publish.url+"' target=_blank>"+tt.publish.url+"</a><br>"
					sec3+="btfile: <a href='"+tt.publish.btfile+"' target=_blank>"+tt.publish.btfile+"</a><br>"
                                        for ( dd in tt.publish.imgs){
                                                sec3+="[img]"+tt.publish.imgs[dd]+"[/img]<br>"
                                        }
                                        for ( dd in tt.publish.imgs){
                                                sec3+="<img src="+tt.publish.imgs[dd]+">"
                                        }
					sec1="No."+(pub_start-(len-item))+" grab at "+pub_time.getDate()+" "+(pub_time.getMonth()+1)+" "+pub_time.getFullYear()+" "+pub_time.getHours()+":"+pub_time.getMinutes()+":"+pub_time.getSeconds()+"<br>"
                                        sec1+="<a href="+tt.url+" target=_blank>"+tt.title+"</a></br>"
                                        sec1+="tag:"+tt.tag+" <button class='btn btn-info' onclick=publish('"+tt.url+"')>pub</button></br>"
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
                                        html+=' <ul class="nav nav-tabs navbar-inner">'
                                        html+='   <li class="active"><a href="#tab_pub_'+(pub_start-item)+'_1" data-toggle="tab">grab</a></li>'
                                        html+='   <li><a href="#tab_pub_'+(pub_start-item)+'_2" data-toggle="tab">origin</a></li>'
                                        html+='   <li><a href="#tab_pub_'+(pub_start-item)+'_3" data-toggle="tab">pub</a></li>'
                                        html+=' </ul>'
                                        html+=' <div class="tab-content">'
                                        html+='   <div class="tab-pane active" id="tab_pub_'+(pub_start-item)+'_1">'
                                        html+='         <p>'+sec1+'</p>'
                                        html+='   </div>'
                                        html+='   <div class="tab-pane" id="tab_pub_'+(pub_start-item)+'_2">'
                                        html+='         <p>'+tt.raw_content+'</p>'
                                        html+='   </div>'
                                        html+='   <div class="tab-pane" id="tab_pub_'+(pub_start-item)+'_3">'
                                        html+='         <p>'+sec3+'</p>'
                                        html+='   </div>'
                                        html+=' </div>'
                                        html+='</div>'
                                        console.log(html)
                                        $('.pub ul.thumbnails').append(html)
                                }
                            if(response.is_end){
                                $(".pub_more").html('end')
                                $(".pub_more").attr("disabled", "disabled");
			    }else{
                                $(".pub_more").html('more')
                                $(".pub_more").removeAttr("disabled");
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
