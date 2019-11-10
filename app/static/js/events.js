// Hidden message after 4 sec
window.setTimeout(function() {
    $(".save-conf").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);

function events_list() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_events',
        }).done(function(api_resp){

            var events_json = api_resp;
            var hl_rig = parseInt(0);
            var id_event = 0;

            $('#events').empty();
            $.each( events_json, function( key, value ) {
                if ( value.online == "1") {
                    online_class = "table-success";
                    rig_status = "En ligne";
                } else {
                    online_class = "table-danger";
                    hl_rig += parseInt(1);
                    rig_status = "Hors-ligne";
                }

                // display table
                $('#events').append(
                    '' +
                        '<tr class="'+online_class+'" style="cursor:pointer" onclick="alert(\'ok\')">' +
                            '<td><strong>' + value.id +'</strong></td>' +
                            '<td><strong>' + value.nom_rig +'</strong></td>' +
                            '<td>' + rig_status + '</td>' +
                            '<td>' + value.create_at + '</td>' +
                        '</tr>' +
                    ''
                );


            });
        }
   );
};

var launch_events;

$( document ).ready(function() {
    launch_events = events_list();
    reload_events();
});

function reload_events() {
  reload_events = setInterval(events_list, 20000);
}
