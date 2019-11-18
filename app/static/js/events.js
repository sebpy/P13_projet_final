let last_tt_event = 0;

function events_list() {
    $.ajax({
        type:"GET",
        url: $SCRIPT_ROOT + '/_events',
        }).done(function(api_resp){

            var audio = new Audio('/static/sound/notification.mp3');
            var events_json = api_resp;
            var hl_rig = parseInt(0);
            var id_event = 0;
            var events_items = api_resp.events_items;
            var total_active_event = api_resp.total_active_event;

            $('#events').empty();
            $.each( events_items, function( key, value ) {

                if ( value.event == "1") {
                    online_class = "table-success";
                    rig_status = "En ligne";
                }
                else if ( value.event == "0") {
                    online_class = "table-danger";
                    hl_rig += parseInt(1);
                    rig_status = "Hors-ligne";
                }

                // display table
                $('#events').append(
                    '' +
                        '<tr class="'+ online_class +'">' +
                            '<td><strong>' + value.id +'</strong></td>' +
                            '<td><strong>' + value.nom_rig +'</strong></td>' +
                            '<td>' + rig_status + '</td>' +
                            '<td>' + value.create_at + '</td>' +
                        '</tr>' +
                    ''
                );
            });
            $('#tt_events').text(total_active_event);

            if (total_active_event > last_tt_event) {
                audio.play();
                last_tt_event = total_active_event;
            }
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
