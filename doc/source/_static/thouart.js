// jQuery Cookie Plugin https://github.com/carhartl/jquery-cookie
(function(g){g.cookie=function(h,b,a){if(1<arguments.length&&(!/Object/.test(Object.prototype.toString.call(b))||null===b||void 0===b)){a=g.extend({},a);if(null===b||void 0===b)a.a=-1;if("number"===typeof a.a){var d=a.a,c=a.a=new Date;c.setDate(c.getDate()+d)}b=""+b;return document.cookie=[encodeURIComponent(h),"=",a.b?b:encodeURIComponent(b),a.a?"; expires="+a.a.toUTCString():"",a.path?"; path="+a.path:"",a.domain?"; domain="+a.domain:"",a.c?"; secure":""].join("")}for(var a=b||{},d=a.b?function(a){return a}:
decodeURIComponent,c=document.cookie.split("; "),e=0,f;f=c[e]&&c[e].split("=");e++)if(d(f[0])===h)return d(f[1]||"");return null}})(jQuery);

function sb_toggle(i){
        if (i == true && $.cookie("f") == "1") {
                $(".sphinxsidebarwrapper").fadeOut(100); $("div.bodywrapper").animate({marginLeft: "20px"}, '400'); $.cookie("f", "1");
        } else if(i == false){
                if ( $.cookie("f") == null){
                    $(".sphinxsidebarwrapper").fadeOut(100); $("div.bodywrapper").animate({marginLeft: "20px"}, '400'); $.cookie("f", "1");
                } else{
                    $(".sphinxsidebarwrapper").fadeIn(); $("div.bodywrapper").animate({marginLeft: "230px"}); $.cookie("f", null);
                }
        }
}
$(document).ready( function(){ sb_toggle(true); $(".fold").click( function(){sb_toggle(false)})});
