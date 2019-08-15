// Hidden message after 4 sec
window.setTimeout(function() {
    $(".save-conf").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);
