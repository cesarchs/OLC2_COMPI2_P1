
if (document.getElementById("default")!=null) {
CodeMirror.fromTextArea(document.getElementById("default"),{
    lineNumbers : true,
    theme : "abcdef",
    mode: "python",
    matchBrackets: true,
    
});
}


