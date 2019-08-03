// Rafraichissement des données toutes les 30sec
$( document ).ready(function() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){
            $('#row').empty()
            var rig_card = ""
            var nb_rig = Object.keys(api_resp).length;
            var tt_pw = parseFloat(0)
            var tt_gpu = parseInt(0)
            var hl_rig = parseInt(0)
            uptime_rig = "En ligne"

            $.each( api_resp, function( key, value ) {

                if ( value.enLigne == "1") {
                    rig_card = "rig_card_on"
                    uptime_rig = "En ligne"
                } else {
                    rig_card = "rig_card_off"
                    hl_rig += parseInt(1)
                    uptime_rig = "Hors ligne"
                }

                $('#row').append(
                      '<div class="col-sx-3 col-md-2">' +
                          '<div class="'+ rig_card +' col-lg-12">' +
                              '<strong>'+ value.NomRig +'</strong><br>' +
                              'GPUs: <strong>'+ value.nbGpu +' '+ value.typeGpu +'</strong><br>' +
                              uptime_rig +': <strong>'+ value.uptime.substring(0,10) +'</strong><br>' +
                              'Miner up: <strong>'+ value.mineTime +'</strong><br>' +
                              'Hashrate: <strong>'+ value.HashTotal +' '+ value.hashUnit +'</strong><br>' +
                              'Consommation: <strong>'+ value.totalpw +'W</strong><br>' +
                          '</div>' +
                      '</div>'
                );

                tt_pw += parseFloat(value.totalpw)
                tt_gpu += parseInt(value.nbGpu)

            });
            $('#tt_rig').text(nb_rig);
            $('#tt_pw').text(tt_pw.toFixed(2) + 'W');
            $('#tt_gpu').text(tt_gpu);
            $('#hl_rig').text(hl_rig);
        }
   );
});

setInterval(function(){
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){
            $('#row').empty()
            var rig_card = ""
            var nb_rig = Object.keys(api_resp).length;
            var tt_pw = parseFloat(0)
            var tt_gpu = parseInt(0)
            var hl_rig = parseInt(0)
            var uptime_rig = "En ligne"

            $.each( api_resp, function( key, value ) {
                if ( value.enLigne == "1") {
                    rig_card = "rig_card_on"
                    uptime_rig = "En ligne"
                } else {
                    rig_card = "rig_card_off"
                    hl_rig += parseInt(1)
                    uptime_rig = "Hors ligne"
                }

                $('#row').append(
                      '<div class="col-sx-3 col-md-2">' +
                          '<div class="'+ rig_card +' col-lg-12">' +
                              '<strong>'+ value.NomRig +'</strong><br>' +
                              'GPUs: <strong>'+ value.nbGpu +' '+ value.typeGpu +'</strong><br>' +
                              uptime_rig +': <strong>'+ value.uptime.substring(0,10) +'</strong><br>' +
                              'Miner up: <strong>'+ value.mineTime +'</strong><br>' +
                              'Hashrate: <strong>'+ value.HashTotal +' '+ value.hashUnit +'</strong><br>' +
                              'Consommation: <strong>'+ value.totalpw +'W</strong><br>' +
                          '</div>' +
                      '</div>'
                );

                tt_pw += parseFloat(value.totalpw)
                tt_gpu += parseInt(value.nbGpu)

            });
            $('#tt_rig').text(nb_rig);
            $('#tt_pw').text(tt_pw.toFixed(2) + 'W');
            $('#tt_gpu').text(tt_gpu);
            $('#hl_rig').text(hl_rig);
        }
   );
}, 30000); //30 secondes


var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}