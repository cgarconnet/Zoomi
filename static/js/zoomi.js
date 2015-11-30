$(document).ready(function () {

		$(document).on("click", ".entrycheckmark", function(){
			// this is the checkbox as input. So it's parent is required to be checked
			// completed css will put a line-through as text-decoration
			// si checked alors il n'est plus à faire
			$(this).toggleClass("todo");
			$(this).toggleClass("completed");

		});
});


    function EntryComplete(id)
    {
    //	var points = $("input").val();
        $.ajax({
            url: "/entries/update/"+id+"/",
            type: "POST",
            data: {
            	'value': 1},
            success: function(response) {
            },

        });
    }

    function EntryImpediment(id)
    {
    //	var points = $("input").val();
        $.ajax({
            dataType: "json",
            url: "/entries/update/"+id+"/",
            type: "POST",
            data: {
            	'field' : 'impediment',
            	'impediment': 1},
            success: function(response) {
            },

        });
    }

// Sortable listview
// we will have to save it
/*
  $(document).bind('pageinit', function() {
    $( "#sortable" ).sortable();
    $( "#sortable" ).disableSelection();
    <!-- Refresh list to the end of sort to have a correct display -->
    $( "#sortable" ).bind( "sortstop", function(event, ui) {
      $('#sortable').listview('refresh');
    });
  });
  */