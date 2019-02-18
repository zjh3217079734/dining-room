
function createXhr(){
  //判断浏览器对xhr的支持性
  if(window.XMLHttpRequest){
    return new XMLHttpRequest();
  }else{
    return new ActiveXObject("Microsoft.XMLHTTP");
  }
}

