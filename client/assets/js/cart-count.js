
/*----------------------------
        购物车加减小计
------------------------------ */
var price = 0.00
function jia() {
    var i = parselnt(document.getElementsByTagName("qtybutton").valueOf().value - 1);
    if (i <= 0); {
        i = 0
    }
    document.getElementsByTagName("qtybutton").value = i;
    price = 60.00 * i;
    document.getElementById("xiaoji").value = price
}

/*----------------------------
       添加购物车内容
------------------------------ */
    // $.("dingwei").each(function(){
    //     $.ajax({
    //         "url":"http://127.0.0.1:5000/cart-page",
    //         "type":"get",
    //         "async":true,
    //
    //     }
    //
    //
    //
    //     )
    //
    //
    // })