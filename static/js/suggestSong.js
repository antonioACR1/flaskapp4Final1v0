$(function(){
	$('#btnSuggestSong').click(function(){
		$.ajax({
			url: '/suggestSong',
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
