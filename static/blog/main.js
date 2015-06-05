$(document).ready(function(){

	var csrftoken = $.cookie('csrftoken');

	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	createComment();
	deleteComment();
});


//Listener is delegated to parent because of dynamcially generated delete forms
function deleteComment(){
	$('#comment-group').on('click', '.comment-delete-form', function(e){
		e.preventDefault();
		e.stopPropagation();
		var commentId = $(this).find('.form-group').children().first().val();

		$.ajax({
			url: '/comment/delete/',
			type: 'POST',
			data: {id: commentId},
			success: function(json){
				var deletedCommentID = String(json.id);
				$("#" + deletedCommentID).remove();
				$("#comment-delete-form" + deletedCommentID).slideUp();
				updateCommentCount(json.count);
			}
		});
	});
}

function createComment(){
		$('#comment-submit').on('click', function(e){
			e.preventDefault();
			e.stopPropagation();
			$.ajax({
				url: '/comment/create/',
				type : 'POST',
				data: {post_id: $("#post_id").val(),
					name: $('#comment-name').val(),
					email: $('#comment-email').val(), 
					content: $('#comment-content').val()
				},
			 success: function(data) {
             // clear fields
            $('#comment-name').val("");
            $('#comment-email').val("");
            $('#comment-content').val("");
            // add new comment
            $("#comment-group").append(data);

            updateCommentCount($(".comment").length);
        },
		});
	});
}

function updateCommentCount(count){
	if (count === 1){
		$("#comment-count").html(count + " Comment:");
  		}
	else {
		$("#comment-count").html(count + " Comments:");
  		}
}