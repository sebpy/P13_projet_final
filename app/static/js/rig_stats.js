// Display statistics in list

var id_rig = $(".wrapper").attr("id");
function rig_stats() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/' + id_rig,
        }).done(function(api_rig_stats){

            var stats = api_rig_stats.stats_rig;
            var rig = api_rig_stats;
            var nb_gpu = Object.keys(stats).length;
            var tt_pw = parseFloat(0);
            var tt_hash = parseInt(0);
            var uptime = rig.uptime
            var rig_name = rig.rig_name
            var active_envent = rig.event
            var hash_unit = rig.hash_unit

            $('#rigs').empty();
            $.each( stats, function( key, value ) {

                $('#rigs').append(
                    '' +
                        '<tr>' +
                            '<td><strong>GPU' + key + '</strong></td>' +
                            '<td>' + value.model + '</td>' +
                            '<td>' + value.hash + ' ' + hash_unit +'</td>' +
                            '<td>' + value.mem_freq + ' MHz</td>' +
                            '<td>' + value.core_freq + ' MHz</td>' +
                            '<td>' + value.pw + ' W</td>' +
                            '<td>' + value.fan + ' %</td>' +
                            '<td>' + value.temp + ' °</td>' +
                        '</tr>' +
                    ''
                );

                tt_hash += parseFloat(value.hash)
                tt_pw += parseFloat(value.pw)
            });

            $('#nb_gpu').text(nb_gpu);
            $('#tt_hash').text(tt_hash.toFixed(2) + ' ' + hash_unit);
            $('#tt_pw').text(tt_pw.toFixed(2) + ' W');
            $('#uptime').text(uptime);
            $('#active_events').text(active_envent);
            $('#rig_name').text(rig_name);
       }
   );
};

var launch_stats;

$( document ).ready(function() {
    launch_stats = rig_stats();
    reload_stats();
});

function reload_stats() {
  launch_stats = setInterval(rig_stats, 30000);
}

