var log = function(){
    console.log(arguments)
}


var weiboTemplate = function(weibo) {
    var w = weibo
    var t = `
            <div class="weibo-container border-top weibo-wrapper">
                <div class="weibo-cell">
                    <div class="user-avatar">
                        <img src=${ w.avatar }>
                    </div>
                    <div class="weibo-body">
                        <div class="weibo-username">
                            <strong>${ w.author }</strong>
                        </div>
                        <div class="weibo-content-body">${ w.weibo }</div>
                        <div class="weibo-time fl-l">发布于&nbsp;:&nbsp;${ w.create_time }</div>
                        <div class="weibo-comment-info">
                            <span>现有评论</span>
                            <span class="weibo-comment-num">${ w.comment }</span>
                        </div>
                    </div>
                    <div class="weibo-bottom">
                        <button class="btn-weibo-delete" data-id="${ w.id }">删&nbsp;&nbsp;除</button>
                        <button class="btn-weibo-comment-expand">展开评论</button>
                    </div>
                </div>
                <div class="height-40"></div>
                <div class="weibo-comment-cell hide">
                    <div class="weibo-edit-form">
                        <div class="height-50"></div>
                        <textarea name="comment-add" class="comment-add left mid" placeholder="发表评论，评论长度不应小于1"></textarea>
                        <button class="btn-weibo-comment-add" data-id="${ w.id }">发表评论</button>
                    </div>
                </div>
                <div class="height-40"></div>
            </div>
    `

    return t
}

var weiboCommentTemplate = function(weiboComment){
    var c = weiboComment
    var t = `
    <div class="height-40"></div>
    <div class="weibo-comment">
        <div class="weibo-main-comment">
            <div class="user-avatar">
                <img src=${ c.avatar }>
            </div>
            <div class="weibo-body">
                <div class="weibo-username">
                    <strong>${ c.author }</strong>
                    <span>&nbsp;评论</span>
                </div>
                <div class="weibo-content-body comment">${ c.comment }</div>
                <div class="weibo-time fl-l comment-create-time">发布于&nbsp;:&nbsp;${ c.create_time }</div>
                <div class="weibo-time fl-r comment-update-time">更新于&nbsp;:&nbsp;${ c.update_time }</div>
            </div>
            <div class="weibo-bottom">
                <button class="btn-weibo-comment-delete" data-id="${ c.id }">删除</button>
                <button class="btn-weibo-comment-edit">更新</button>
            </div>
        </div>
        <div class="weibo-comment-update-cell weibo-edit-form hide">
            <div class="height-40"></div>
            <textarea name="comment-update" class="comment-update left mid" placeholder="更新评论，评论长度不应小于1"></textarea>
            <button class="btn-comment-update" data-id="${ c.id }">确认更新</button>
        </div>
    </div>
    `

    return t
}

var bindEventWeiboAdd = function() {
    $(".btn-weibo-add").on('click', function(){
        log('click')
        var weiboEditForm = $(this).closest('.weibo-edit-form')
        var textarea = weiboEditForm.find(".textarea-weibo")
        var body = textarea.val()
        log('body', body)
        var form = {
            body : body
        }
        var response = function(r){
            if(r.success) {
                var w = r.data
                $(".weibo-list").prepend(weiboTemplate(w))
                textarea.val("")
                alertify.success(r.message)
            }
            else {
                alertify.error(r.message)
            }
        }
        api.weiboAdd(form, response)
    })
}



var bindEventWeiboDelete = function(){
    $(".weibo-list").on('click', '.btn-weibo-delete', function(){
        var weiboId = $(this).data('id')
        var weiboContanier = $(this).closest('.weibo-container')

        api.weiboDelete(weiboId, function(r){
            if(r.success){
                $(weiboContanier).slideUp()
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
            }
        })
    })
}

var bindEventWeiboCommentToggle = function(){
    $(".weibo-list").on('click',".btn-weibo-comment-expand", function(){
        var weiboCell = $(this).closest('.weibo-cell')
        var weiboCommentCell = weiboCell.siblings('.weibo-comment-cell')
        weiboCommentCell.slideToggle()
    })
}

var bindEventWeiboCommentUpdateToggle = function(){
    $(".weibo-list").on('click', ".btn-weibo-comment-edit", function(){
        var weiboMainComment = $(this).closest('.weibo-main-comment')
        var commentUpdateCell = weiboMainComment.siblings('.weibo-comment-update-cell')
        log(commentUpdateCell)
        commentUpdateCell.slideToggle()
    })
}


var bindEventWeiboCommentAdd = function(){
    $(".weibo-list").on('click', ".btn-weibo-comment-add",function(){
        var weiboId = $(this).data('id')
        var weiboEditForm = $(this).closest('.weibo-edit-form')
        var textarea = weiboEditForm.find('textarea.comment-add')
        var body = textarea.val()
        var form = {
            weibo_id : weiboId,
            body : body
        }
        var response = function(r){
            if(r.success) {
                var weiboCommentCell = weiboEditForm.closest('.weibo-comment-cell')
                var c = r.data
                weiboCommentCell.prepend(weiboCommentTemplate(c))
                var weiboContanier = weiboCommentCell.closest('.weibo-container')
                var weiboCommentInfo = weiboContanier.find('.weibo-comment-info')
                var num = weiboCommentInfo.find('span.weibo-comment-num')
                num.text((parseInt(num.text())+1))
                textarea.val("")
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
            }
        }
        api.weiboCommentAdd(form, response)
    })
}

var bindEventWeiboCommentUpdate = function(){
    $(".weibo-list").on('click', "button.btn-comment-update", function(){
        var weiboCommentId = $(this).data('id')
        var updateCell = $(this).parent()
        var textarea = updateCell.find(".comment-update")
        var body = textarea.val()
        var form = {
            body : body
        }
        var response = function(r) {
            if(r.success) {
                var c = r.data
                var weiboMainComment = updateCell.siblings(".weibo-main-comment")
                var comment = weiboMainComment.find(".comment")
                var updateTime = weiboMainComment.find(".comment-update-time")
                comment.text(c.comment)
                updateTime.text(c.update_time)
                textarea.val("")
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
            }

        }

        api.weiboCommentUpdate(weiboCommentId, form, response)
    })
}

var bindEventWeiboCommentDelete = function(){
    $(".weibo-list").on('click', ".btn-weibo-comment-delete", function(){
        var weiboCommentId = $(this).data('id')
        var weiboComment = $(this).closest('.weibo-comment')
        var weiboContanier = $(this).closest('.weibo-container')
        api.weiboCommentDelete(weiboCommentId, function(r){
            if(r.success) {
                $(weiboComment).siblings(".height-40").slideUp()
                $(weiboComment).slideUp()
                var num = weiboContanier.find('span.weibo-comment-num')
                num.text((parseInt(num.text())-1))
                alertify.success(r.message)
            }else {
                alertify.error(r.message)
            }
        })
    })
}

var _list = function(){
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboCommentToggle()
    bindEventWeiboCommentAdd()
    bindEventWeiboCommentDelete()
    bindEventWeiboCommentUpdateToggle()
    bindEventWeiboCommentUpdate()
}


$(document).ready(function(){
    _list()
})