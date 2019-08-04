// Rafraichissement des données toutes les 30sec

var rig_card = "";
var uptime_rig = "En ligne";
var show_nbgpu = "show_block";
var show_uptime = "show_block";
var show_minetime = "show_block";
var show_hash = "show_block";
var show_pw = "show_block";

$( document ).ready(function() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){
            $('#row').empty()

            var stats = api_resp.stats;
            var cfgBlock = api_resp.cfg;
            var nb_rig = Object.keys(stats).length;
            var tt_pw = parseFloat(0);
            var tt_gpu = parseInt(0);
            var hl_rig = parseInt(0);

            if(cfgBlock[0].cfg_nbGpu == 0){
                show_nbgpu = "hidden_block";
            }
            if(cfgBlock[0].cfg_hashTotal == 0){
                show_hash = "hidden_block";
            }
            if(cfgBlock[0].cfg_totalpw == 0){
                show_pw = "hidden_block";
            }
            if(cfgBlock[0].cfg_uptime == 0){
                show_uptime = "hidden_block";
            }
            if(cfgBlock[0].cfg_mineTime == 0){
                show_minetime = "hidden_block";
            }

            $.each( stats, function( key, value ) {
                if ( value.enLigne == "1") {
                    rig_card = "rig_card_on";
                    uptime_rig = "En ligne";
                } else {
                    rig_card = "rig_card_off";
                    hl_rig += parseInt(1);
                    uptime_rig = "Hors ligne";
                }

                $('#row').append(
                      '<div class="col-sx-3 col-md-2">' +
                          '<div class="'+ rig_card +' col-lg-12">' +
                              '<strong>'+ value.NomRig +'</strong><br>' +
                              '<span class="'+show_nbgpu+'">GPUs: <strong>'+ value.nbGpu +' '+ value.typeGpu +'</strong><br></span>' +
                              '<span class="'+show_uptime+'">'+uptime_rig +': <strong>'+ value.uptime.substring(0,10) +'</strong><br></span>' +
                              '<span class="'+show_minetime+'">Miner up: <strong>'+ value.mineTime +'</strong><br></span>' +
                              '<span class="'+show_hash+'">Hashrate: <strong>'+ value.HashTotal +' '+ value.hashUnit +'</strong></span><br>' +
                              '<span class="'+show_pw+'">Consommation: <strong>'+ value.totalpw +'W</strong><br></span>' +
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

            var stats = api_resp.stats;
            var cfgBlock = api_resp.cfg;
            var nb_rig = Object.keys(stats).length;
            var tt_pw = parseFloat(0);
            var tt_gpu = parseInt(0);
            var hl_rig = parseInt(0);

            if(cfgBlock[0].cfg_nbGpu == 0){
                show_nbgpu = "hidden_block";
            }
            if(cfgBlock[0].cfg_hashTotal == 0){
                show_hash = "hidden_block";
            }
            if(cfgBlock[0].cfg_totalpw == 0){
                show_pw = "hidden_block";
            }
            if(cfgBlock[0].cfg_uptime == 0){
                show_uptime = "hidden_block";
            }
            if(cfgBlock[0].cfg_mineTime == 0){
                show_minetime = "hidden_block";
            }

            $.each( stats, function( key, value ) {
                if ( value.enLigne == "1") {
                    rig_card = "rig_card_on";
                    uptime_rig = "En ligne";
                } else {
                    rig_card = "rig_card_off";
                    hl_rig += parseInt(1);
                    uptime_rig = "Hors ligne";
                }

                $('#row').append(
                      '<div class="col-sx-3 col-md-2">' +
                          '<div class="'+ rig_card +' col-lg-12">' +
                              '<strong>'+ value.NomRig +'</strong><br>' +
                              '<span class="'+show_nbgpu+'">GPUs: <strong>'+ value.nbGpu +' '+ value.typeGpu +'</strong><br></span>' +
                              '<span class="'+show_uptime+'">'+uptime_rig +': <strong>'+ value.uptime.substring(0,10) +'</strong><br></span>' +
                              '<span class="'+show_minetime+'">Miner up: <strong>'+ value.mineTime +'</strong><br></span>' +
                              '<span class="'+show_hash+'">Hashrate: <strong>'+ value.HashTotal +' '+ value.hashUnit +'</strong></span><br>' +
                              '<span class="'+show_pw+'">Consommation: <strong>'+ value.totalpw +'W</strong><br></span>' +
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

