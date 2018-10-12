$('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like/', {category_id: catid}, function(data){
        $('#like_count').html(data);
        $('#likes').hide();
    });
});
// $('#likes').click(function(){
// $.ajax({
//             type: 'GET',
//             data:{category_id: catid},
//             url:'/rango/like/',
//             dataType: 'html',
//             success: function(data){
//            $('#like_count').html(data);
//             $('#likes').hide();
//         }
// });
// });