$(document).on('pageinit', function(){
// with JQueryMobile, use this instead of classical ready function
// source here: http://www.gajotres.net/document-onpageinit-vs-document-ready/
//$("#id_name").focus();

});


$(document).ready(function () {

/* move to EntryComple(id) sucessful Ajax load */
		$(document).on("click", ".entrycheckmark", function(){
			// this is the checkbox as input. So it's parent is required to be checked
			// completed css will put a line-through as text-decoration
			// si checked alors il n'est plus à faire
			$(this).toggleClass("todo");
			$(this).toggleClass("completed");
            $(this).parent().parent().addClass("hide_entry");
            $('#todo_list').listview("refresh");

            $(this).parent().parent().slideUp("slow", function(){
            });

            setTimeout(function() {

            },30);

		});


// /* changing the top menu active button selection */
//         $(document).on("click", ".top_menu", function(){
//             // this is the checkbox as input. So it's parent is required to be checked
//             // completed css will put a line-through as text-decoration
//             // si checked alors il n'est plus à faire
//             $( ".top_menu" ).removeClass( "ui-btn-active" );
//             $(this).addClass("ui-btn-active");

//         });
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
// do the toggleClass only when load is sucessfull
//				$(this).toggleClass("todo");
//				$(this).toggleClass("completed");

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
    $( "#todo_list" ).sortable();
    $( "#todo_list" ).disableSelection();
    <!-- Refresh list to the end of sort to have a correct display -->
    $( "#todo_list" ).bind( "sortstop", function(event, ui) {
      $('#todo_list').listview('refresh');
    });
  });
  
*/


