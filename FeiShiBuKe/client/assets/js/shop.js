var pk = 1;
$(window).scroll(function () {
    var htmlHeight = $(document).height();
    var clientHeight = $(window).height();
    var scrollTop = $(document).scrollTop();
    var he = scrollTop + clientHeight;
    if (he == htmlHeight) {
        pk = pk +1; //每次和后端交互，page+1。
        addMore();
    }
    if (scrollTop <=0){
        refresh();
    }
});

function addMore() {
    $.ajax({
        type:"GET",
        url:"/shops?page="+pk,
        dataType:"html",
        success:function (data) {
            $("#div2").empty();
            var div = document.createElement("div");
            document.body.appendChild(div);
            div.innerHTML = data;
        }
    })
}
function refresh() {
    $.ajax({
        type:"GET",
        url:"/shops",
        dataType:"html",
        success:function () {
            window.location.reload();
        }
    })

}
