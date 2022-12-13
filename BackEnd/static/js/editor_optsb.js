if (document.getElementById("optimb")!=null) {
    CodeMirror.fromTextArea(document.getElementById("optimb"),{
        lineNumbers : true,
        theme : "cobalt",
        mode: "go",
        readOnly: false,
        matchBrackets: true,
    });
    }
    