$(document).ready(function () {

		$(document).on("click", ".entrycheckmark", function(){
			// this is the checkbox as input. So it's parent is required to be checked
			// completed css will put a line-through as text-decoration
			// si checked alors il n'est plus à faire
			$(this).toggleClass("todo");
			$(this).toggleClass("completed");

		});
});