$( document ).ready(function() {
    $("#times").hide();
    $("#checked").hide();
    $("#progress").hide();

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

$("#emails_hyperlink").click(function() {
    $("#progress").show();
  });

$("#salvar_senha").click(function() {
    $("#progress").show();
  });

$("#voltar").click(function() {
    $("#progress").show();
});

});
