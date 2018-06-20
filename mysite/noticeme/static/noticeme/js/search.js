$(document).ready(function(){
    $('.collapse').on('shown.bs.collapse', function(e){
        console.dir($(this).parent().closest(".panel-default").find(".glyphicon-plus-sign").eq(0))
        $(e.target).parent().closest(".panel-default").find(".glyphicon-plus-sign").eq(0).removeClass("glyphicon-plus-sign").addClass("glyphicon-minus-sign");
        e.stopPropagation();
    }).on('hidden.bs.collapse', function(e){   
        console.dir( $(this).parent().closest(".panel-default").find(".glyphicon-minus-sign").eq(0)) 
        $(e.target).parent().closest(".panel-default").find(".glyphicon-minus-sign").eq(0).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
        e.stopPropagation();
    });
        
})