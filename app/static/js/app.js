// Rafraichissement des données toutes les 30sec
$( document ).ready(function() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){
            $('#row').empty()
            $.each( api_resp, function( key, value ) {
                if ( value.enLigne == "1") {
                   rig_card = "rig_card_on"
                }
                else {
                   rig_card = "rig_card_off"
                }
                $('#row').append(
                      '<div class="'+ rig_card +'">' +
                      '<strong>'+ value.NomRig +'</strong><br>' +
                      'GPUs: <strong>'+ value.nbGpu +' '+ value.typeGpu +'</strong><br>' +
                      'Uptime: <strong>'+ value.uptime +'</strong><br>' +
                      'Miner uptime: <strong>'+ value.mineTime +'</strong><br>' +
                      'Hashrate: <strong>'+ value.HashTotal +' '+ value.hashUnit +'</strong><br>' +
                      'Puissance: <strong>'+ value.totalpw +'W</strong><br>' +
                  '</div>'
                );
            });
        }
   );
});

setInterval(function(){
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){
            $('#row').empty()
            var rig_car = ""
            $.each( api_resp, function( key, value ) {
                if ( value.enLigne == "1") {
                   rig_card = "rig_card_on"
                }
                else {
                   rig_card = "rig_card_off"
                }
                $('#row').append(
                      '<div class="'+ rig_card +'">' +
                      '<strong>'+ value.NomRig +'</strong><br>' +
                      'GPUs: <strong>'+ value.nbGpu +' '+ value.typeGpu +'</strong><br>' +
                      'Uptime: <strong>'+ value.uptime +'</strong><br>' +
                      'Miner uptime: <strong>'+ value.mineTime +'</strong><br>' +
                      'Hashrate: <strong>'+ value.HashTotal +' '+ value.hashUnit +'</strong><br>' +
                      'Puissance: <strong>'+ value.totalpw +'W</strong><br>' +
                  '</div>'
                );
            });
        }
   );
}, 30000); //30 secondes
