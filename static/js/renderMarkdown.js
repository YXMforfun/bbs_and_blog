var renderMarkDown = function() {
	marked.setOptions({
		renderer : new marked.Renderer(),
		gfm : true,
		tables : true,
		breaks : true,
		pedantic : true,
	});
	$('.markdown-body').each(function(){
		var tag = $(this);
		var raw = tag.text();
		tag.html(marked(raw));
	})
	$('pre > code').each(function () {
		var tag = $(this);
		var target = this;

		var code = tag.text();
		tag.empty();
		initCodeMirror(code, target);
	});
	console.log(marked('I am using __markdown__.'))
}
var initCodeMirror = function(code, target) {
    var options = {
        value : code,
        lineNumbers : true,
        readOnly : true,
        theme : "material",
        height : "auto",
    };
    var mode = "python";
    var editor = CodeMirror(target, options);
    editor.setSize("100%", "100%");
}
