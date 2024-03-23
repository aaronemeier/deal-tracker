$('document').ready(function () {

    $('#notification').click(function (){
        $('#notification').fadeOut(500);
    });

    setTimeout(function() {
        $('#notification').click();
    }, 5000);

    $(".card-img").each(function (){
        let maxWidth = 200;
        let maxHeight = 200;
        let ratio = 0;

        let width = $(this).width();
        let height = $(this).height();

        if(width > maxWidth){
            ratio = maxWidth / width;
            $(this).width(maxWidth);
            $(this).height(height * ratio);
        }

        width = $(this).width();
        height = $(this).height();
        if(height > maxHeight){
            ratio = maxHeight / height;
            $(this).height(maxHeight);
            $(this).width(width * ratio);
        }
    });
});
