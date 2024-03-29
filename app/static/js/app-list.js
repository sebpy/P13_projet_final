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
            var tt_hash = parseInt(0);
            var hl_rig = parseInt(0);
            var availability = load;

            $('#rigs').empty();
            $.each( stats, function( key, value ) {
                if ( value.online == "1") {
                    online_class = "table-success";
                } else {
                    online_class = "table-danger";
                    hl_rig += parseInt(1);
                }

                // display table
                $('#rigs').append(
                    '' +
                        '<tr class="'+online_class+'" style="cursor:pointer" onclick="javascript:location.href=\'/detail/' + value.id_rig + '\'">' +
                            '<td><strong>' + value.nom_rig +'</strong></td>' +
                            '<td>' + value.nb_gpu + ' ' + value.gpu_type + '</td>' +
                            '<td>' + value.uptime + '</td>' +
                            '<td>' + value.total_hash +' '+ value.hash_unit +'</td>' +
                            '<td>' + value.total_pw + 'W</td>' +
                        '</tr>' +
                    ''
                );

                tt_pw += parseFloat(value.total_pw)
                tt_hash += parseFloat(value.total_hash)
                //tt_gpu += parseInt(value.nb_gpu)

            });

            $('#tt_rig').text(nb_rig);
            $('#tt_pw').text(tt_pw.toFixed(2) + 'W');
            if (!$(stats).length){
                $('#tt_hash').text(0.00);
            } else {
                $('#tt_hash').text(tt_hash.toFixed(2)+' '+stats[0].hash_unit);
            }
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
