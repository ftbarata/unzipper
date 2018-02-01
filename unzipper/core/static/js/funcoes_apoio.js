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

});
