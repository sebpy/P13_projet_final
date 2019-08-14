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
            var load = api_resp.availability;
            var nb_rig = Object.keys(stats).length;
            var tt_pw = parseFloat(0);
            var tt_gpu = parseInt(0);
            var hl_rig = parseInt(0);
            var availability = load;


            if(cfgBlock[0].cfg_nb_gpu == 0){
                show_nbgpu = "hidden_block";
            }
            if(cfgBlock[0].cfg_total_hash == 0){
                show_hash = "hidden_block";
            }
            if(cfgBlock[0].cfg_total_pw == 0){
                show_pw = "hidden_block";
            }
            if(cfgBlock[0].cfg_uptime == 0){
                show_uptime = "hidden_block";
            }
            if(cfgBlock[0].cfg_mineTime == 0){
                show_minetime = "hidden_block";
            }

            $.each( stats, function( key, value ) {
                if ( value.online == "1") {
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
                              '<strong>'+ value.nom_rig +'</strong><br>' +
                              '<span class="'+show_nbgpu+'">GPUs: <strong>'+ value.nb_gpu +' '+ value.type_gpu +'</strong><br></span>' +
                              '<span class="'+show_uptime+'">'+uptime_rig +': <strong>'+ value.uptime.substring(0,10) +'</strong><br></span>' +
                              '<span class="'+show_minetime+'">Miner up: <strong>'+ value.mine_time +'</strong><br></span>' +
                              '<span class="'+show_hash+'">Hashrate: <strong>'+ value.total_hash +' '+ value.hash_unit +'</strong></span><br>' +
                              '<span class="'+show_pw+'">Consommation: <strong>'+ value.total_pw +'W</strong><br></span>' +
                          '</div>' +
                      '</div>'
                );


                tt_pw += parseFloat(value.total_pw)
                tt_gpu += parseInt(value.nb_gpu)

            });

            $('#tt_rig').text(nb_rig);
            $('#tt_pw').text(tt_pw.toFixed(2) + 'W');
            $('#tt_gpu').text(tt_gpu);
            $('#hl_rig').text(hl_rig);
            $('#availability').text(availability + '%');

            if(hl_rig > 0){
                $( '#hl_rig' ).removeClass( "badge-success" ).addClass( "badge-danger" );
            }
            else {
                $( '#hl_rig' ).removeClass( "badge-danger" ).addClass( "badge-success" );
            }

            if(availability.toFixed(2) < 70) {
                $( '.average' ).removeClass( "badge-success" ).addClass( "badge-danger" );
            }
            else if(availability.toFixed(2) >= 70 && availability.toFixed(2) < 90) {
                $( '.average' ).removeClass( "badge-danger" ).addClass( "badge-warning" );
            }
            else {
                $( '.average' ).removeClass( "badge-warning" ).addClass( "badge-success" );
            }

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
            var load = api_resp.availability;
            var nb_rig = Object.keys(stats).length;
            var tt_pw = parseFloat(0);
            var tt_gpu = parseInt(0);
            var hl_rig = parseInt(0);
            var availability = load;

            if(cfgBlock[0].cfg_nb_gpu == 0){
                show_nbgpu = "hidden_block";
            }
            if(cfgBlock[0].cfg_total_hash == 0){
                show_hash = "hidden_block";
            }
            if(cfgBlock[0].cfg_total_pw == 0){
                show_pw = "hidden_block";
            }
            if(cfgBlock[0].cfg_uptime == 0){
                show_uptime = "hidden_block";
            }
            if(cfgBlock[0].cfg_mineTime == 0){
                show_minetime = "hidden_block";
            }

            $.each( stats, function( key, value ) {
                if ( value.online == "1") {
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
                              '<strong>'+ value.nom_rig +'</strong><br>' +
                              '<span class="'+show_nbgpu+'">GPUs: <strong>'+ value.nb_gpu +' '+ value.type_gpu +'</strong><br></span>' +
                              '<span class="'+show_uptime+'">'+uptime_rig +': <strong>'+ value.uptime.substring(0,10) +'</strong><br></span>' +
                              '<span class="'+show_minetime+'">Miner up: <strong>'+ value.mine_time +'</strong><br></span>' +
                              '<span class="'+show_hash+'">Hashrate: <strong>'+ value.total_hash +' '+ value.hash_unit +'</strong></span><br>' +
                              '<span class="'+show_pw+'">Consommation: <strong>'+ value.total_pw +'W</strong><br></span>' +
                          '</div>' +
                      '</div>'
                );


                tt_pw += parseFloat(value.total_pw)
                tt_gpu += parseInt(value.nb_gpu)

            });

            $('#tt_rig').text(nb_rig);
            $('#tt_pw').text(tt_pw.toFixed(2) + 'W');
            $('#tt_gpu').text(tt_gpu);
            $('#hl_rig').text(hl_rig);
            $('#availability').text(availability + '%');

            if(hl_rig > 0){
                $( '#hl_rig' ).removeClass( "badge-success" ).addClass( "badge-danger" );
            }
            else {
                $( '#hl_rig' ).removeClass( "badge-danger" ).addClass( "badge-success" );
            }

            if(availability.toFixed(2) < 70) {
                $( '.average' ).removeClass( "badge-success" ).addClass( "badge-danger" );
            }
            else if(availability.toFixed(2) >= 70 && availability.toFixed(2) < 90) {
                $( '.average' ).removeClass( "badge-danger" ).addClass( "badge-warning" );
            }
            else {
                $( '.average' ).removeClass( "badge-warning" ).addClass( "badge-success" );
            }

        }
   );
}, 30000); //30 secondes

// Hidden message after 4 sec
window.setTimeout(function() {
    $(".save-conf").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);
