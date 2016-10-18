var log = function(){
    console.log(arguments)
}


// ajax 判断用户名是否可用
var checkUsername = function(){
    $("#id-input-username").on("blur", function(){
        var username = $("#id-input-username").val()
        var message = ''
        if(username.length < 6){
            message = '用户名太短,至少6个字符'
        } else if (username.length >= 15) {
            message = '用户名太长,至多15个字符'
        } else {
            var form = {
                username : username
            }
            var response = function(r) {
                message = r.message
                $("#id-check-username").html(message)
            }
            api.usernameCheck(form, response)

        }
        $("#id-check-username").html(message)
    })
}


// 判断前后输入密码是否一致
var checkPassword = function(){
    $("#id-input-password").on("blur", function(){
        var passwordFirst = $("#id-input-password").val()
        var message = ''
        if(passwordFirst.length <= 5){
            message = '密码太短,至少6个字符'
        } else if (passwordFirst.length >= 18) {
            message = '密码太长,至多18个字符'
        } else {
            message = '该密码可以使用'
        }
        $("#id-check-password").html(message)
    })
    $("#id-input-password2").on("blur", function(){
        var passwordSecond = $("#id-input-password2").val()
        var passwordFirst = $("#id-input-password").val()
        var message = ''
        if(passwordSecond.length == 0){
            message = '密码不能为空'
        } else if(passwordFirst == passwordSecond) {
            message = '前后一致,可以注册啦'
        } else {
            message = '请确保前后输入的两次密码相同'
        }
        $("#id-check-password2").html(message)
    })
}

var setup = function(){
    // tab click
    $(".tab >a").on("click", function(){
        var self = $(this);
        $(".active").removeClass("active");
        self.addClass("active");
    });
    // tab action
    var tabAction = function(position, showLogin){
        $(".tab-block").animate({
            "left" : position
        }, "fast");
        $("#id-div-login").toggle(showLogin);
        $("#id-div-signup").toggle(!showLogin);
    };

    $("#id-a-signup").on("click", function(){
        var position = "0px";
        var showLogin = false;
        tabAction(position, showLogin);
    })

    $("#id-a-login").on("click", function(){
        var position = "65px";
        var showLogin = true;
        tabAction(position, showLogin);
    });


};

//form
var formFromKeys = function(keys, prefix){
    var form = {};
    for(var i = 0; i < keys.length; i++){
        var key = keys[i];
        var tagid = prefix + key;
        var value = $("#" + tagid).val();
        log('value', value, 'tagid', tagid)
        if(value.length < 1){
            break;
        }
        form[key] = value;
    }
    return form;
}

var loginForm = function(){
    var keys = [
        'username',
        'password',
    ];
    var loginPrefix = 'id-input-login-';
    var form = formFromKeys(keys, loginPrefix);
    return form;
}

var registerForm = function(){
    var keys = [
        'username',
        'password'
    ];
    var registerPrefix = 'id-input-';
    var form = formFromKeys(keys, registerPrefix);
    return form;
};

// actions
var register = function(){
    var form = registerForm()
    log(form, 'form')
    var response = function(r){
        if(r.success){
            var data = r.data;
            window.location.href = data.next;
        } else {
            alertify.error(r.message);
        }
    };
    api.userRegister(form, response);
};

var login = function(){
    var form = loginForm()
    var response = function(r){
        if(r.success){
            var data = r.data;
            window.location.href = data.next;
        } else {
            alertify.error(r.message);
        }
    };
    api.userLogin(form, response);
}

var bindActions = function(){
    $("#id-button-register").on("click", function(){
        register();
    });

    $("#id-button-login").on("click", function(){
        login();
    })
}


var _main = function(){
    checkUsername()
    checkPassword()
    setup()
    bindActions()
    //select signup
    $("#id-a-login").click();
}

$(document).ready(function(){
    _main()
})