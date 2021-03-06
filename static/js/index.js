    $( ".todo" ).draggable();
    $( ".ui-tabs-panel" ).droppable({
    	drop: function( event, ui ) {
    		// http://jsfiddle.net/tilwinjoy/6PL8H/
    		// http://stackoverflow.com/questions/3816636/example-combing-jquery-drag-and-drop-and-tabs
			// Remove the item from first list
			// Add the item to the second list
			alert($(this))
			// $( this )
         	//	.addClass( "ui-state-highlight" )
          	//	.find( "p" )
            //	.html( "Dropped!" );
      }
    });


$(function() {
    $( "#list-items" ).sortable({
      placeholder: "ui-state-highlight",
      stop: function (event, ui) {
 		localStorage.setItem("list-items", $("#list-items").html());
      }
    });
    $( "#list-items" ).disableSelection();
});

$(function() {
    $( "#list-items-week" ).sortable({
      placeholder: "ui-state-highlight",
      stop: function (event, ui) {
 		localStorage.setItem("list-items-week", $("#list-items-week").html());
      }
    });
    $( "#list-items-week" ).disableSelection();
});

$(function() {
    $( "#list-items-future" ).sortable({
      placeholder: "ui-state-highlight",
      stop: function (event, ui) {
 		localStorage.setItem("list-items-future", $("#list-items-future").html());
      }
    });
    $( "#list-items-future" ).disableSelection();
});

$(document).ready(function () {
    // YOUR CODE HERE!
    // $("#xxx") for a Id
    // $(".xxx") for a Class

    // Before we load what's in LocalStorage
    // Then we show them on the page
	$("#list-items").html(localStorage.getItem("list-items"));
	$("#list-items-week").html(localStorage.getItem("list-items-week"));
	$("#list-items-future").html(localStorage.getItem("list-items-future"));


    $(".add-items").submit(function(event){
		event.preventDefault(); // submit will submit the form and load again the page, this is why without this code, the Hi will only falsh and desiappear because a new page is loaded
		var item = $("#todo-list-item").val();

		if (item) {
			// Now let's save it local storage
			$("#list-items").append("<li class='todo'><input class='checkbox' type='checkbox'/><a class='impediment state_off'>(B)</a> - " + item + "<a class='remove'>x</a><hr></li>");
			//Now we can save the updated list in LocalStorage
			localStorage.setItem("list-items", $("#list-items").html());	
			$("#todo-list-item").val("");
		}

    });

    $(".add-items-week").submit(function(event){
		event.preventDefault(); // submit will submit the form and load again the page, this is why without this code, the Hi will only falsh and desiappear because a new page is loaded
		var item = $("#todo-list-item-week").val();

		if (item) {
			// Now let's save it local storage
			$("#list-items-week").append("<li class='todo'><input class='checkbox' type='checkbox'/><a class='impediment state_off'>(B)</a>" + item + "<a class='remove'>xx</a><hr></li>");
			//Now we can save the updated list in LocalStorage
			localStorage.setItem("list-items-week", $("#list-items-week").html());	
			$("#todo-list-item-week").val("");
		}

    });

    $(".add-items-future").submit(function(event){
		event.preventDefault(); // submit will submit the form and load again the page, this is why without this code, the Hi will only falsh and desiappear because a new page is loaded
		var item = $("#todo-list-item-future").val();

		if (item) {
			// Now let's save it local storage
			$("#list-items-future").append("<li class='todo'><input class='checkbox' type='checkbox'/>" + item + "<a class='remove'>x</a><hr></li>");
			//Now we can save the updated list in LocalStorage
			localStorage.setItem("list-items-future", $("#list-items-future").html());	
			$("#todo-list-item-future").val("");
		}

    });

		$(document).on("change", ".checkbox", function(){
			// this is the checkbox as input. So it's parent is required to be checked
			// completed css will put a line-through as text-decoration
			// si checked alors il n'est plus à faire
			$(this).parent().toggleClass("todo");
			$(this).parent().toggleClass("completed");


		
			// we also change the checked in the DOM, so we can save this value in LocalStorage 
			if ($(this).attr("checked")) {
				$(this).removeAttr("checked");
			} else {
				$(this).attr("checked","checked");
			// This code to highlight in red works but should  flash in the future
			// Would need also to do not hightlight in red the (B) items, so only select the item that have ".state_off"
		    $(this).parent().prevAll(".todo").addClass('before');
		    setTimeout(function(){
		      $('.before').removeClass('before');}, 1000);

			}
			//Now we can save the updated list in LocalStorage
			localStorage.setItem("list-items", $("#list-items").html());	
			localStorage.setItem("list-items-week", $("#list-items-week").html());	
			localStorage.setItem("list-items-future", $("#list-items-future").html());	
		});

		$(document).on("click", ".impediment", function(){
			$(this).toggleClass("state_off");
			$(this).toggleClass("state_on");

			//Now we can save the updated list in LocalStorage
			localStorage.setItem("list-items", $("#list-items").html());
			localStorage.setItem("list-items-week", $("#list-items-week").html());
			localStorage.setItem("list-items-future", $("#list-items-future").html());
		});


		$(document).on("click", ".remove", function(){
			$(this).parent().slideUp("slow", function(){
				localStorage.setItem("list-items", $("#list-items").html());
				localStorage.setItem("list-items-week", $("#list-items-week").html());
				localStorage.setItem("list-items-future", $("#list-items-future").html());	
			});

		});

});
