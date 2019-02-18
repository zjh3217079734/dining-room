
$(function(){
  $("#btnLog").click(function(){
      var params = {
      "username":$("#username").val(),
      "password":$("#password").val(),
    }
    $.post('/login',params,function(data){
      alert(data);
    });
  });
});


$(function(){
  $("#btnReg").click(function(){
      var params = {
      "username":$("#uname").val(),
      "password":$("#upwd").val(),
      "phone":$("#uphone").val()
    }
    $.post('/register',params,function(data){
      alert(data);
    });
  });
});


function checkUname(){
    var ret = true;
    var xhr = createXhr();
    var uname = $("#uname").val();
    var url = "/register/checkuname?uname="+uname;
    xhr.open('get',url,false);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4&&xhr.status==200){
            if(xhr.responseText=="1"){
                $("#uname-show").html("用户名称已存在");
                 ret = false;
            }else{
                $("#uname-show").html("通过");
            }
        }
    }
    xhr.send(null);
    return ret;
};
function registerUser(){
    if(checkUname()){
        var xhr = createXhr();
        xhr.open("post",'/register',true);
        xhr.onreadystatechange=function(){
            if(xhr.readyState==4&&xhr.status==200){
                alert(xhr.responseText);
            }
        }
        xhr.setRequestHeader('Content-Type',"application/x-www-form-urlencoded");
        var uname=$("#uname").val();
        var upwd = $("#upwd").val();
        var phone=$("#uphone").val();
        var params="username="+uname+"&password="+upwd+"&phone="+phone;
        xhr.send(params);
    }else{
        alert("用户名称已存在,不能注册");
    }
}

$(function(){
    $("#uname").blur(function(){
        checkUname();
    });
    $("#btnReg").click(function(){
        registerUser();
    });
});
