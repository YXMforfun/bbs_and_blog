var api = {}

api.ajax = function(url, method, form, callback) {
    var request = {
        url : url,
        type : method,
        data : form,
        success : function(response) {
            var r = JSON.parse(response)
            callback(r)
        },
        error : function(err) {
            var r = {
                'success' : false,
                message : '网络错误'
            }
            callback(r)
        }

    }
    $.ajax(request)
}

api.get = function(url, response) {
    api.ajax(url, 'get', {}, response)
}

api.post = function(url, form, response) {
    api.ajax(url, 'post', form, response)
}

//weibo API
api.weiboAdd = function(form, response) {
    var url='/api/weibo/add'
    api.post(url, form, response)
}

api.weiboDelete = function(weiboId, response){
    var url = '/api/weibo/delete/' + weiboId
    api.get(url, response)
}

api.weiboUpdate = function(weiboId, form, response){
    var url = '/api/weibo/update/' + weiboId
    api.post(url, form, response)
}

//weiboComment API
api.weiboComment = function(weiboId, response) {
    var url = '/api/weibo/' + weiboId + '/comment'
    api.get(url, response)
}

api.weiboCommentAdd = function(form, response){
    var url = '/api/weibo/comment/add'
    api.post(url, form, response)
}


api.weiboCommentGet = function(commentId, response){
    var url = '/api/weibo/comment/' + commentId
    api.get(url, response)
}

api.weiboCommentUpdate = function(commentId, form, response){
    var url = '/api/weibo/comment/update/' + commentId
    api.post(url, form, response)
}

api.weiboCommentDelete = function(commentId, response){
    var url = '/api/weibo/comment/delete/' + commentId
    api.get(url, response)
}


// user API
api.usernameCheck = function(form, response){
    var url = '/api/user/check/username'
    api.post(url, form, response)
}

api.userGet = function(userId, response){
    var url = '/api/user/' + userId
    api.get(url, response)
}

api.userRegister = function(form, response){
    var url = '/api/user/register'
    api.post(url, form, response)
}

api.userLogin = function(form, response){
    var url = '/api/user/login'
    api.post(url, form, response)
}