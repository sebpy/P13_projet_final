$( document ).ready(function() {
    //setInterval(function(){
        $.ajax({
            type:"GET",
            url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){
            $.each( api_resp, function( key, value ) {
              $('#nom_rig').text(value.NomRig),
              $('#hash_rig').text(""+value.HashTotal+""),
              $('#pw_rig').text(value.totalpw);
            });
        });
    //}, 60000); // Ici chaque minute
});




