function bindEmailCaptchaClick(){
     $("#captcha-btn").click(function (event){
        event.preventDefault();
        var $this = $(this);
        var email = $("input[name='email']").val();
        // alert(email);
        $.ajax(
            {
                url:"captcha/email?email="+email,
                method:"GET",
                success: function(result){
                    var code = result['code'];
                    // alert(result)
                    if(code == 200){
                        var countdown = 5;
                        $this.off("click")
                        var timer = setInterval(function (){
                            $this.text(countdown);
                            countdown -= 1;
                            if(countdown <= 0){
                                clearInterval(timer);
                                $this.text("获取验证码")
                                bindEmailCaptchaClick();
                            }
                        }, 1000)
                        // alert("邮箱验证码发送成功！");
                    }else{
                        alert("邮箱验证码发送出错！");
                    }
                },
                fail: function(error){

                    console.log(error);
                }
            }
        )
    });
}

$(function(){
    bindEmailCaptchaClick();
    });
// alert("register")