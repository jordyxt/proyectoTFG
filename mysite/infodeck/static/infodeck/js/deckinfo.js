$(document).ready(function(){ 
  //funcion ajax para mostrar usuarios
    $("#search").submit(function(e){
        e.preventDefault();
		var deckId= $("#deck-search").val();
        $.ajax({
	        url: "http://localhost:8000/noticeme/deckinfo/"+deckId
	    }).then(function(par) {
		   $.each(par, function(i, item) {
               var resultado
                        if (item['attached']=='no'){
                               resultado='it\'s not an attached slide'                 
                        }else{
                            if (item['updated']==false){
                                resultado='it\'s an attached slide  (outdated version)' 
                            }else{
                                resultado='it\'s an attached slide  (updated version)' 
                            }
                        }
						$('#test').append(
							$('<ul>').append(
                                $('<li>').append(i+' : '+resultado),
                                
							)
						)
    			
			});
	    });
    });
});