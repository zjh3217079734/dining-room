$(function () {
    $("#kws").keyup(function () {
        var xhr = createXhr();
        var url = "/search?kws="+this.value;
        xhr.open("get",url,true);
        xhr.onreadystatechange=function(){
            if(xhr.readyState==4&&xhr.status==200){
                var arr = JSON.parse(xhr.responseText);
                if(arr.length > 0){
                    $("#show").html("");
                    $("#show").css("display","block");
                    $.each(arr,function (i,obj) {
                        var $a=$("<a>"+obj+"</a>");
                        $("#show").append($a);
                    })
                }else{
                    $("#show").css("diaplay","none");
                };
            };
        };
        xhr.send(null);
    });
});

