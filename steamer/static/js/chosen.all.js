/*
 * Lets save space, and add a search box to the inputs, also
 * remove the overflow:hidden from the grand parents of the 
 * input boxes to fix the grappelli layout so that it can 
 * display the .chosen plugin widget.
 */

//The flatpages editor
tinyMCE.init({ theme : "advanced", 
               mode:"exact",
               theme_advanced_styles: "Normal=normalp;Fancy=fancy", 
               elements: "id_content"});



$(document).ready(function(){ 
    $('select:not([name="action"],[name="cfg_dir"])').chosen();
    $('select').each(function(){
        $(this).parent().parent().css("overflow","visible")
        $(this).parent().parent().parent().css("overflow","visible")
    });
    //As the chosen plugin mucksup the admin's .filter_choice onchange event
    //we regiter it again.
    $('select.filter_choice').change( function(){window.location.href = $(this).val()})

})



