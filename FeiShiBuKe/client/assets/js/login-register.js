function checkna(){
	na = form1.uname.value;

	if( na.length <1 || na.length >12)
	{
		divname.innerHTML='<font class="tips_false">长度是1~12个字符</font>';
	}else{
		divname.innerHTML='<font class="tips_true">输入正确</font>';
	}
}
//验证密码 
function checkpsd1(){    
	psd1=form1.upwd.value;  
	var flagZM=false ;
	var flagSZ=false ; 
	var flagQT=false ;
	if(psd1.length<6 || psd1.length>12){   
		divpassword1.innerHTML='<font class="tips_false">长度错误</font>';
	}else
		{   
		  for(i=0;i < psd1.length;i++)   
			{    
				if((psd1.charAt(i) >= 'A' && psd1.charAt(i)<='Z') || (psd1.charAt(i)>='a' && psd1.charAt(i)<='z')) 
				{   
					flagZM=true;
				}
				else if(psd1.charAt(i)>='0' && psd1.charAt(i)<='9')    
				{ 
					flagSZ=true;
				}else    
				{ 
					flagQT=true;
				}   
			}   
			if(!flagZM||!flagSZ||flagQT){
			divpassword1.innerHTML='<font class="tips_false">密码必须是字母数字的组合</font>'; 
			}else{
			divpassword1.innerHTML='<font class="tips_true">输入正确</font>';					 
			}  				 
		}
}
//验证确认密码 
function checkpsd2(){ 
		if(form1.upwd.value!=form1.upwd1.value) { 
		    divpassword2.innerHTML='<font class="tips_false">您两次输入的密码不一样</font>';
		} else { 
		     divpassword2.innerHTML='<font class="tips_true">输入正确</font>';
		}
}

//验证用户名
