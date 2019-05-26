function ShowHint(){
    let hintArea = document.getElementById("hint");
    hintArea.style.display = "block";
}

function Skip(){
    let answerArea = document.getElementById("answer-wrapper");
    let customArea = document.getElementById("custom-answer-wrapper");

    customArea.style.display = "block";
    answerArea.style.display = "block";
}