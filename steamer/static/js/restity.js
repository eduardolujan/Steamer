//This is for using with stringify:  $('form').serializeObject()
(function( $ ){
    $.fn.serializeObject = function() {
            var o = {}; var a = this.serializeArray();
            $.each(a, function() {
                if (o[this.name] !== undefined) {
                    if (!o[this.name].push) {
                        o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';
                }
            });
        return o;
    };
})(jQuery);

//A shortcut on .ajax()
(function( $ ){
    $.restifyForm = function(form, method, callback, badRequest) {
        if (arguments.length > 3){
            var badRequest = function(){} 
            var callback = function(){} 
        }else if (arguments.length > 4){
            var badRequest = function(){} 
        }
        $.ajax({
            type: method,
            url: form.attr('action'),
            processData:false,
            contentType:'application/json', data: JSON.stringify(form.serializeObject()),
            statusCode: { 200: callback, 201: callback, 204: callback, 400: badRequest },
            dataType: "json"
        });
    };
})(jQuery);

