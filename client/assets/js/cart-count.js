/*----------------------------
        购物车加减小计
------------------------------ */
// var price = 0.00
// function jia() {
//     var i = parselnt(document.getElementsByTagName("qtybutton").valueOf().value - 1);
//     if (i <= 0); {
//         i = 0
//     }
//     document.getElementsByTagName("qtybutton").value = i;
//     price = 60.00 * i;
//     document.getElementById("xiaoji").value = price
// }

/*----------------------------
    // 表单数据json获取测试
    ------------------------------ */
// function getJson() {
//     $("#caidan").each(function () {
//         var getid = [];
//         var getnum = [];
//         getid.join(value.getElementsByName("good_info_id"));
//         getnum.join(document.getElementsByName("qtybutton"));
//
//     });
//
//     for (var i = 0; i < getid.length; i++) {
//         var dic = {
//             getid:getnum,
//         };
//     }
//
//
//     return dic
// }


$("#quzhifu").click(function () {
    var goosinfo=[];
    for(var i=0;i<$('#count');i++){
       var params={
            "goods_id" : $("#good").val(),
           "goods_num" : $("#qtybutton").val()
        }
        goodsinfo.join(params)
    }
    return goosinfo
})