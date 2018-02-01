$( document ).ready(function() {
    $("#times").hide();
    $("#checked").hide();

    $( "#path" ).autocomplete({
       source: function( request, response ) {
        $.ajax({
          crossDomain: true,
          type: "POST",
          url: "http://localhost:8000/ajax/checkpath",
          dataType: "json",
          data: {
            inputpath:$("#path").val()
          },
          success: function( data ) {

            if (data == "False"){
                $("#times").show();
                $("#checked").hide();
            }
            if (data == "True"){
                $("#times").hide();
                $("#checked").show();
            }
          }
        })
      },
      minLength: 2,
    })

//$("#btn-submit").click((function() {
//    var progressbar = $( "#progressbar" ),
//      progressLabel = $( ".progress-label" );
//
//    progressbar.progressbar({
//      value: false,
//      change: function() {
//        progressLabel.text( progressbar.progressbar( "value" ) + "%" );
//      },
//      complete: function() {
//        progressLabel.text( "Concluído." );
//      }
//    });
//
//    function progress() {
//      var val = progressbar.progressbar( "value" ) || 0;
//
//      progressbar.progressbar( "value", val + 2 );
//
//      if ( val < 99 ) {
//        setTimeout( progress, 80 );
//      }
//    }
//
//    setTimeout( progress, 2000 );
//  }))

});
