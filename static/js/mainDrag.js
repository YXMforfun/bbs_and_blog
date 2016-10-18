var log = function() {
    console.log(arguments);
}
var showSiteNav = function(){
    var switchSite= $("#switch-site-nav")
    var pos = [-395, -355, -315,- 270,  -230];
    var start = $("#site-nav a.active").index();
    switchSite.css({ top : pos[start]})
    $("#site-nav a").hover(
        function(){
            var index = $(this).index();
            switchSite.stop().animate({ top : pos[index]}, 'normal', 'swing')
        },
        function(){
            switchSite.animate({ top : pos[start]}, 'normal', 'swing')
        })
}

var addActive = function(){
    var location = String(window.location);
    $("#site-nav a").each(function(){
        if($(this)[0].href == location){
            $(this).addClass("active");
        }
    })

}

var mainDrag = {
    config : function() {
        this.selector = {
            mainElement : "#main",
            bgImg : "#bg-image img",
            col : "#main .col",
            scrollBar : ".scrollbar",
            navCol : "#nav-col"
        };
        this.mainElement = $(this.selector.mainElement);
        this.bgImg = $(this.selector.bgImg);
        this.col = $(this.selector.col);
        this.scrollBar = $(this.selector.scrollBar);
        this.navCol = $(this.selector.navCol);
        this.numCols = this.col.length;
        this.colWidth = this.col.eq(0).innerWidth() + 1;
        this.maxCols = this.getMaxVisibleCols() ;
        this.step = this.stepMax = 5;
        this.isDragging = false;
        this.currentIndex = 0;
        this.dragAxis;
        this.tempElem;
        this.ms;
        this.downX;
        this.downY;
        this.startX;
        this.startY;
        this.mainOffset;
        this.distanceX;
        this.distanceY;
        this.scrollOnLimit = false;
        this.isAnimating;
        this.getMaxDragLeft = {}
        this.getMaxDragRight = {}
        this.left;
        this.intDelta = 0;
        this.currentWheel = null;
    },
    setup : function(){
        mainDrag.config();
        mainDrag.bindWindowSize();
        mainDrag.mainElement.width(mainDrag.numCols * mainDrag.colWidth)
        mainDrag.scrollBar.fadeOut();
        $(document).on("mousedown", mainDrag.mouseDown);
        $(document).on("mouseup", mainDrag.mouseUp);
        $(document).on("keydown", mainDrag.keyDown);
        mainDrag.col.on("mousewheel", mainDrag.mouseWheel);
    },
    mouseDown : function(event) {
        if($(event.target).is('input') || $(event.target).is('textarea')){
            return;
        }
        var targetParent = $(event.target).parents("#main");
        if(targetParent.length > 0){
            $(document).on("mousemove", mainDrag.mouseMove);
            mainDrag.mainElement.addClass('dragging');
        }
    },
    mouseMove : function(event) {
        mainDrag.unbindMove(event);
        if(!mainDrag.isDragging){
            mainDrag.checkDrag(event);
        } else {
            if(mainDrag.dragAxis == 'x'){
                mainDrag.dragFromX(event);
            } else if(mainDrag.dragAxis == 'y'){
                mainDrag.dragFromY(event);
            }
        }
        mainDrag.downX = event.pageX;
        mainDrag.downY = event.pageY;
    },
    mouseUp : function(event){
        $(document).off("mousemove", mainDrag.mouseMove);
        mainDrag.scrollBar.fadeTo('medium', 0);
        mainDrag.mainElement.removeClass('dragging');
        if(mainDrag.isDragging){
            mainDrag.isDragging = false;
            if(mainDrag.dragAxis == 'x'){
                var currentIndex = mainDrag.getComputedIndex();
                var nextElement = mainDrag.col.eq(currentIndex);
                mainDrag.animateMain(-nextElement.position().left);
            } else {
                window.setTimeout(function() {
                    $('a').off('click', mainDrag.unbindMove);
                }, 60);
            }
        }
    },
    unbindMove : function(event){
        event.preventDefault();
    },
    bindWindowSize : function(event) {
        $(window).on("resize", function(event) {
            mainDrag.maxCols = mainDrag.getMaxVisibleCols();
            mainDrag.intDelta = 0;
            mainDrag.col.css('top', 0);
        })
    },
    checkDrag : function(event) {
        var timeOut=300;
        var d = new Date();
        var currentMs = d.getTime();
        if(mainDrag.step<= 0 && mainDrag.ms != null){
            mainDrag.step = mainDrag.stepMax;
            if( (currentMs - mainDrag.ms) < timeOut){
                mainDrag.isDragging = true;
                $('a').on("click", mainDrag.unbindMove);
                mainDrag.setAxis(event, mainDrag.startX, mainDrag.startY);
            }
        }
        if(mainDrag.step == mainDrag.stepMax){
            mainDrag.ms = currentMs;
            mainDrag.startX = event.pageX;
            mainDrag.startY = event.pageY;
        }
        mainDrag.step--;
    },
    setAxis : function(event, startX, startY) {
         var currentX = event.pageX;
         var currentY = event.pageY;
         var dx = currentX - startX;
         var dy = currentY - startY;
         if (Math.abs(dx) > Math.abs(dy)){
             mainDrag.dragAxis = 'x';
             mainDrag.tempElem = mainDrag.mainElement;
         } else {
             mainDrag.dragAxis = 'y';
             mainDrag.tempElem = $(event.target).closest('.col');
             mainDrag.setScroll(mainDrag.tempElem);
         }
    },
    dragFromY : function(event) {
        mainDrag.distanceY = mainDrag.tempElem.position().top + event.pageY - mainDrag.downY;
        var distanceY = mainDrag.distanceY
        var scrollH = mainDrag.tempElem.find(".scroll").height();
        var windowH = $(window).height();
        if(scrollH <= windowH){
            mainDrag.scrollOnLimit = true;
        } else {
            mainDrag.scrollOnLimit = false;
            if(distanceY <= 0 && distanceY > (windowH - scrollH)){
                mainDrag.tempElem[0].style.top = distanceY + 'px';
                mainDrag.tempElem.data('top', distanceY);
                mainDrag.updateScrollPosition(mainDrag.tempElem);
            }
        }
    },
    dragFromX : function(event) {
        mainDrag.distanceX = mainDrag.tempElem.position().left + event.pageX - mainDrag.downX;
        var distanceX = mainDrag.distanceX;
        var windowWidth = $(window).width() + 'x' + $(window).height();
        if(distanceX >= 0 && distanceX <= mainDrag.getDragRight(windowWidth)){
            if(!(mainDrag.bgImg.hasClass('left'))){
                mainDrag.bgImg.addClass('left').removeClass('right');
            }
            mainDrag.tempElem[0].style.left = distanceX + 'px';
        } else if (distanceX < 0 && distanceX > -mainDrag.getDragLeft(windowWidth)){
            if(!(mainDrag.bgImg).hasClass('right')){
                mainDrag.bgImg.addClass('right').removeClass('left');
            }
            mainDrag.tempElem[0].style.left = distanceX + 'px';
        }
    },
    getDragLeft : function(windowWidth) {
        if(!(mainDrag.getMaxDragLeft[windowWidth] === undefined)){
            return mainDrag.getMaxDragLeft[windowWidth];
        }
        var imgWidth = mainDrag.bgImg.width();
        var winWidth = $(window).width();
        var mainElemWidth = mainDrag.mainElement.width();
        var navColWidth = mainDrag.navCol.width();
        var left = mainElemWidth + imgWidth + navColWidth - winWidth;
        return mainDrag.getMaxDragLeft[winWidth] = left;
    },
    getDragRight : function(windowWidth) {
        if(!(mainDrag.getMaxDragRight[windowWidth] === undefined)){
            return mainDrag.getMaxDragRight[windowWidth];
        }
        var imgWidth = mainDrag.bgImg.width();
        var right = imgWidth;
        return mainDrag.getMaxDragRight[windowWidth] = right;
    },
    getMaxVisibleCols : function() {
        var colWidth = mainDrag.colWidth;
        var visibleWindow = mainDrag.getVisibleArea().x;
        var max = Math.floor(visibleWindow/colWidth) ;
        return max;
    },
    getVisibleArea : function() {
        return {
            'x' : $(window).width() - mainDrag.navCol.innerWidth(),
            'y' : $(window).height()
        }
    },
    getComputedIndex : function() {
        mainDrag.left = mainDrag.mainElement.position().left;
        var left = mainDrag.left;
        var colWidth = mainDrag.colWidth;
        var limitIndex = mainDrag.numCols - mainDrag.maxCols;
        var limitOffset = limitIndex * colWidth;
        if(left >= 0){
            mainDrag.currentIndex = 0;
        } else if ((-left) >= limitOffset){
            mainDrag.currentIndex = limitIndex;
        } else {
            mainDrag.currentIndex = Math.floor((-left)/colWidth)
        }
        return mainDrag.currentIndex;
    },
    animateMain : function(offset) {
        mainDrag.isAnimating = true;
        mainDrag.mainElement.stop().animate({
            left : offset
        }, 600 , 'swing', function(){
            mainDrag.isAnimating = false;
            mainDrag.slideTrackAnimate();
            $('a').off('click', mainDrag.unbindMove);
        });
    },
    slideTrackAnimate : function() {
        var left = $('li', slideTrack.container).eq(mainDrag.currentIndex).position().left;
        slideTrack.track.css({
            'left' : left
        });
        slideTrack.left = left;
        slideTrack.isDragging = false;
    },
    setScroll : function(col) {
        var scrollH = $(".scroll", col).height();
        var windowH = $(window).height();
        var scrollValue = 100 * windowH / scrollH;
        if(scrollValue < 100) {
            mainDrag.scrollBar.fadeTo('medium', 0.5).css('left', $(col).offset().left - 193 + $(col).width() - 15);
            $(".scrollbar-track", mainDrag.scrollBar).height(scrollValue + "%")
            mainDrag.updateScrollPosition(col);
        } else {
            mainDrag.scrollBar.hide();
        }
    },
    updateScrollPosition: function(col){
        if(!mainDrag.scrollOnLimit){
            var top = $(col).position().top;
            var scrollH = $(".scroll", col).height();
            var scrollTop = Math.abs(100 * top / scrollH);
            $(".scrollbar-track").css('top', scrollTop + '%');
        }
    },
    keyDown: function(event){
        if($(event.target).is('input')){
            return;
        }
        var keyCode = event.which;
        var arrow = {
            left : 37,
            up : 38,
            right : 39,
            down : 40
        }
        switch(keyCode){
            case arrow.right:
            mainDrag.navTo('next');
            break;
            case arrow.left:
            mainDrag.navTo('prev');
            break;
        }
    },
    navTo: function(sign){
        var limitIndex = mainDrag.numCols - mainDrag.maxCols;
        if (sign == 'next' && mainDrag.currentIndex >= limitIndex) {
            return;
        }
        var nextElement = mainDrag.col.eq(mainDrag.currentIndex)[sign]();
        if (nextElement.length != 0) {
            var left = nextElement.position().left;
            mainDrag.animateMain(-left);
            mainDrag.currentIndex = sign == 'next' ? (mainDrag.currentIndex + 1) : (mainDrag.currentIndex - 1);
        }
        if (sign == 'prev') {
            if (!mainDrag.bgImg.hasClass('left')) {
                mainDrag.bgImg.addClass('left').removeClass('right');
            }
        } else if (sign == 'next') {
            if (!mainDrag.bgImg.hasClass('right')) {
                mainDrag.bgImg.addClass('right').removeClass('left');
            }
        }
    },
    mouseWheel : function(event, delta) {
        if (mainDrag.currentWheel != mainDrag.col.index(this)){
            mainDrag.intDelta = $(this).data('intDelta') || 0;
        }
        var scrollH = $(this).find('.scroll').height();
        var windowH = $(window).height();
        var top = $(this).position().top;
        if(delta > 0 && mainDrag.intDelta <= 0){
            mainDrag.intDelta++;
        } else if (top != -(scrollH - windowH)){
            mainDrag.intDelta--;
        }
        if ($(this).data('top') != null ) {
            mainDrag.intDelta = Math.round($(this).data('top') / 20);
            $(this).data('top', null );
        }
        if (scrollH > windowH && (mainDrag.intDelta <= 0 && (top >= -(scrollH - windowH) || top < 0))) {
            var newTop = 20 * mainDrag.intDelta;
            if (newTop < -(scrollH - windowH)) {
                newTop = -(scrollH - windowH);
            }
            $(this).css('top', newTop);
            mainDrag.updateScrollPosition($(this));
        }
        mainDrag.currentWheell = $('.col').index(this);
        $(this).data('intDelta', mainDrag.intDelta);
    }
}

var slideTrack = {
    config : function(){
        this.selector = {
            container: "#cols-nav",
            track : "#cols-nav-track",
            slide : "#main"
        }
        this.container = $(this.selector.container);
        this.track = $(this.selector.track);
        this.slide = $(this.selector.slide);
        this.trackWidth = this.track.width();
        this.containerWidth = this.container.width()
        this.relation = mainDrag.colWidth/6;
        this.isDragging = false;
        this.currentX;
        this.left = 0;
        this.isMoving = false;
    },
    setup : function(){
        slideTrack.config();
        $("#main .col").each(function(index){
            $('ul', slideTrack.container).append(slideTrack.liTemplate(index));
        });
        var width = ($('li', this.container).width() + 2) * $('li', this.container).length
        slideTrack.container.css({'width' : width});
        slideTrack.updateTrack();
        $(window).on("resize", function(event){
            slideTrack.updateTrack();
        });
        slideTrack.track.on("mousedown", slideTrack.unbindMove);
        $(document).on("mousedown", slideTrack.mouseDown);
        $(document).on("mouseup", slideTrack.mouseUp);
    },
    liTemplate : function(index){
        var result = index + 1;
        var t = `
        <li class="nav-col-item ir">${ result }</li>
        `
        return t;
    },
    unbindMove : function(event){
        event.preventDefault();
    },
    mouseDown : function(event){
        if(slideTrack.isDragging){
            return;
        }
        if($(event.target).is(slideTrack.selector.track)){
            slideTrack.currentX = event.pageX;
            $(document).on("mousemove", slideTrack.mouseMove);
        }
    },
    mouseMove : function(event){
        var left = slideTrack.left + event.pageX -slideTrack.currentX || 0;
        if(!slideTrack.isDragging){
            slideTrack.isDragging = true;
        }
        if(left >= 0) {
            slideTrack.track.css({'left': left});
            slideTrack.slide.css({'left': (-left) * slideTrack.relation});
            slideTrack.left = left;
        } else {
            return;
        }
        slideTrack.currentX = event.pageX;
    },
    mouseUp : function(event){
        if(slideTrack.isDragging){
            $(document).off("mousemove", slideTrack.mouseMove);
            var currentIndex = mainDrag.getComputedIndex();
            var nextElement = mainDrag.col.eq(currentIndex);
            mainDrag.animateMain(-nextElement.position().left);
        }
    },
    updateTrack : function(){
        slideTrack.track.css('width', mainDrag.getMaxVisibleCols() * 6 - 2);
    }

}

var pageDrag = function(){
    addActive();
    showSiteNav();
    mainDrag.setup();
    slideTrack.setup();
}
