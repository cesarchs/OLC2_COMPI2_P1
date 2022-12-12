if (document.getElementById("console")!=null) {
CodeMirror.fromTextArea(document.getElementById("console"),{
    lineNumbers : true,
    theme : "cobalt",
    mode: "go",
    readOnly: false,
    matchBrackets: true,
});
}
