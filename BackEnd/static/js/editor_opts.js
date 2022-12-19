if (document.getElementById("optim")!=null) {
    CodeMirror.fromTextArea(document.getElementById("optim"),{
        lineNumbers : true,
        theme : "cobalt",
        mode: "go",
        readOnly: false,
        matchBrackets: true,
    });
    }
    