$(document).on('pageinit', function(){
// with JQueryMobile, use this instead of classical ready function
// source here: http://www.gajotres.net/document-onpageinit-vs-document-ready/
//$("#id_name").focus();

});

// $(document).on('pageshow', function(event, data) {
// $('[data-url="/"]').not(".ui-page-active").remove();
// // $('[data-url=/transferred]').not(".ui-page-active").remove();
// });

// $(document).on('pageshow', function(event, data) {
// $('[data-role=page]').not(".ui-page-active").remove();
// });

// $('#page1').on('pagehide',function(event){
// $('#page1').remove();
// });


$(document).ready(function () {


// Force scrolling to the top, otherwise, the focus on the crete form make the page going to the down
    $(this).scrollTop(0);



    // $('#editModal').on('show.bs.modal', function (event) {
      
    //   $("#editModalContent").load($(this).attr('data-to-load'));

    //   $(this).attr('data-to-load') button = $(event.relatedTarget) // Button that triggered the modal
    //   var recipient = button.data('whatever') // Extract info from data-* attributes
    //   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    //   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    //   var modal = $(this)
    //   modal.find('.modal-title').text('New message to ')
    //   modal.find('.modal-body input').val(recipient)
    // })


        $(document).on("click", ".options", function(){
//  click on the gear
            $("#edit_entry").load($(this).attr('data-to-load'));
            setTimeout( function() {
                $("#edit_entry").popup("open");
            }
                , 50);
// ???          $(this).parent().toggleClass("state_on");
        })


// Code for the modal
$('#editModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    $("#editModalContent").load(button.data('toload'));
})

//         $(document).on("click", ".editor", function(){
// //  click on the gear
//             $("#editModalContent").load($(this).attr('data-to-load'));
//             conqolz.log($(this).attr('data-to-load'));
// // ???          $(this).parent().toggleClass("state_on");
//         })




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


