// Display statistics in list

function stats_list() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_answer',
        }).done(function(api_resp){

            var stats = api_resp.stats;
            var cfgBlock = api_resp.cfg;
            var load = api_resp.availability;
            var nb_rig = Object.keys(stats).length;
            var tt_pw = parseFloat(0);
            var tt_gpu = parseInt(0);
            var hl_rig = parseInt(0);
            var availability = load;

            $.each( stats, function( key, value ) {
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

            if(parseFloat(availability).toFixed(2) < 70) {
                $( '.average' ).removeClass( "badge-success" ).addClass( "badge-danger" );
            }
            else if(parseFloat(availability).toFixed(2) >= 70 && parseFloat(availability).toFixed(2) < 90) {
                $( '.average' ).removeClass( "badge-danger" ).addClass( "badge-warning" );
            }
            else {
                $( '.average' ).removeClass( "badge-warning" ).addClass( "badge-success" );
            }
        }
   );
};

var launch_stats;

$( document ).ready(function() {
    launch_stats = stats_list();
    reload_stats();
});

function reload_stats() {
  launch_stats = setInterval(stats_list, 30000);
}
