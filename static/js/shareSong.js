$(function(){
	$('#btnShareSong').click(function(){
		$.ajax({
			url: '/shareSong',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
