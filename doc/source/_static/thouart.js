(function(a){a.fn.bPopup=function(i,k){function u(){c.css({left:b.scrollLeft()+g,position:"absolute",top:b.scrollTop()+e,"z-index":o.zIndex}).appendTo(o.appendTo).hide(function(){a.isFunction(o.onOpen)&&o.onOpen.call(c);if(o.loadUrl!=null){o.contentContainer=o.contentContainer==null?c:a(o.contentContainer);switch(o.content){case "iframe":a('<iframe width="100%" height="100%"></iframe>').attr("src",o.loadUrl).appendTo(o.contentContainer);break;default:o.contentContainer.load(o.loadUrl)}}}).fadeIn(o.fadeSpeed, function(){a.isFunction(k)&&k()});v()}function j(){o.modal&&a("#bModal").fadeOut(o.fadeSpeed,function(){a("#bModal").remove()});c.fadeOut(o.fadeSpeed,function(){o.loadUrl!=null&&o.content!="xlink"&&o.contentContainer.empty()});o.scrollBar||a("html").css("overflow","auto");a("."+o.closeClass).die("click");a("#bModal").die("click");b.unbind("keydown.bPopup");f.unbind(".bPopup");c.data("bPopup",null);a.isFunction(o.onClose)&&setTimeout(function(){o.onClose.call(c)},o.fadeSpeed);return false}function w(){if(m|| x){var d=[b.height(),b.width()];return{"background-color":o.modalColor,height:d[0],left:l(),opacity:0,position:"absolute",top:0,width:d[1],"z-index":o.zIndex-1}}else return{"background-color":o.modalColor,height:"100%",left:0,opacity:0,position:"fixed",top:0,width:"100%","z-index":o.zIndex-1}}function v(){a("."+o.closeClass).live("click",j);o.modalClose&&a("#bModal").live("click",j).css("cursor","pointer");if(o.follow[0]||o.follow[1])f.bind("scroll.bPopup",function(){c.stop().animate({left:o.follow[1]? b.scrollLeft()+g:g,top:o.follow[0]?b.scrollTop()+e:e},o.followSpeed);}).bind("resize.bPopup",function(){if(o.modal&&m){var d=[b.height(),b.width()];n.css({height:d[0],width:d[1],left:l()})}h=p(c,o.amsl);if(o.follow[0])e=q?b.scrollTop()+o.position[0]:b.scrollTop()+h[0];if(o.follow[1])g=r?b.scrollLeft()+o.position[1]:b.scrollLeft()+h[1];c.stop().animate({left:g,top:e},o.followSpeed)});o.escClose&&b.bind("keydown.bPopup",function(d){d.which==27&&j()})}function l(){return f.width()<a("body").width()? 0:(a("body").width()-f.width())/2}function p(d,y){var s=(f.height()-d.outerHeight(true))/2-y,z=(f.width()-d.outerWidth(true))/2+l();return[s<20?20:s,z]}if(a.isFunction(i)){k=i;i=null}o=a.extend({},a.fn.bPopup.defaults,i);o.scrollBar||a("html").css("overflow","hidden");var c=a(this),n=a('<div id="bModal"></div>'),b=a(document),f=a(window),h=p(c,o.amsl),q=o.position[0]!="auto",r=o.position[1]!="auto",e=q?o.position[0]:h[0],g=r?o.position[1]:h[1],t=navigator.userAgent.toLowerCase(),x=t.indexOf("iphone")!= -1,m=/msie 6/i.test(t)&&typeof window.XMLHttpRequest!="object";this.close=function(){o=c.data("bPopup");j()};return this.each(function(){if(!c.data("bPopup")){o.modal&&n.css(w()).appendTo(o.appendTo).animate({opacity:o.opacity},o.fadeSpeed);c.data("bPopup",o);u()}})};a.fn.bPopup.defaults={amsl:50,appendTo:"body",closeClass:"bClose",content:"ajax",contentContainer:null,escClose:true,fadeSpeed:250,follow:[true,true],followSpeed:500,loadUrl:null,modal:true,modalClose:true,modalColor:"#000",onClose:null, onOpen:null,opacity:0.7,position:["auto","auto"],scrollBar:true,zIndex:9999}})(jQuery);
//reStructuredText image directive doesn't set id.
$(document).ready( function(){ $("img.popuplarge").each( function(idx){ this.setAttribute('id', 'imgl'+idx ) })})
$(document).ready(function(){ $(".popup").each( function(idx){ $(this).bind('click', function(){ $("img#imgl"+idx).bPopup(); return false }) } )});
