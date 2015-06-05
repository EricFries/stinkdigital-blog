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

function deleteComment(){
	$('.comment-delete-form').on('submit', function(e){
		e.preventDefault();
		e.stopPropagation();
		var commentId = $(this).find('.form-group').children().first().val();

		$.ajax({
			url: '/comment/delete/',
			type: 'POST',
			data: {id: commentId},
			success: function(json){
				var deletedCommentID = String(json.id);
				$("#" + deletedCommentID).slideUp();
				$("#comment-delete-form" + deletedCommentID).slideUp();
			}
		});
	});
}

// $(this).find('.form-group').children().first().val()

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
			 success: function(json) {
             // clear fields
            $('#comment-name').val("");
            $('#comment-email').val("");
            $('#comment-content').val("");
            // add new comment
            $("#comment-group").append("<div class='comment' id='" + json.id + "''><ul><li> On " + json.date + " " + "<a href='mailto:" + json.email +"'>" + json.name + "</a> said, " + json.content + "</li></ul></div");
            debugger
            // update comment count
            if (json.count === 1){
            	$("#comment-count").html(json.count + " Comment");
          		}
        		else {
        			$("#comment-count").html(json.count + " Comments");
          		}
        },
		});
	});
}



