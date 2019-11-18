// Display statistics in list

function rig_stats() {
    var id_rig = $(".wrapper").attr("id");

    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/' + id_rig,
        }).done(function(api_rig_stats){

            var stats = api_rig_stats;
            var nb_gpu = Object.keys(api_rig_stats).length;
            var tt_pw = parseFloat(0);
            var tt_hash = parseInt(0);
            var uptime = ""

            $('#rigs').empty();
            $.each( stats, function( key, value ) {

                $('#rigs').append(
                    '' +
                        '<tr>' +
                            '<td><strong>GPU' + key + '</strong></td>' +
                            '<td>' + value.model + '</td>' +
                            '<td>' + value.hash +'</td>' +
                            '<td>' + value.mem_freq + ' MHz</td>' +
                            '<td>' + value.core_freq + ' MHz</td>' +
                            '<td>' + value.pw + ' W</td>' +
                        '</tr>' +
                    ''
                );

                tt_hash += parseFloat(value.hash)
                tt_pw += parseFloat(value.pw)
            });

            $('#nb_gpu').text(nb_gpu);
            $('#tt_hash').text(tt_hash.toFixed(2));
            $('#tt_pw').text(tt_pw.toFixed(2));
            $('#uptime').text(uptime);
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