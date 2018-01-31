$( document ).ready(function() {
    $("#times").hide();
    $("#checked").hide();

    $( "#path" ).autocomplete({
       source: function( request, response ) {
        $.ajax({
          crossDomain: true,
          url: "http://localhost:8000/ajax/" + $("#path").val(),
          dataType: "json",
          data: {

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
});
