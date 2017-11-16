$.mobile.autoInitializePage = false;
var socket;
var keyboard;
var cursor = 0;
var windowIndex = [[0,2], [3,5], [5,7]];
var startTime;

var keyCss = {
  "height": "30px",
  "line-height": "30px",
  "width": "30%",
  "float": "left",
  "border-style": "solid",
  "border-width": "1px",
  "text-align": "center"
};

var wordCss = {
  "height": "40px",
  "width": "19%",
  "float": "left",
  "border-style": "solid",
  "border-width": "1px",
  "text-align": "center",
  "word-break": "break-all"
};

function setKeyVisible() {
  $('#keycontainer').children().each(function(index) {
    if (windowIndex[cursor][0] <= index && index <= windowIndex[cursor][1]) {
      $('#keycontainer').children().eq(index).show();
    } else {
      $('#keycontainer').children().eq(index).hide();
    }
  });
}

function setKeyboard() {
  $("#keycontainer").empty();
  cursor = 0;

  keyboard.forEach(function(key, index){
    var keyView = $.trim(Array.from(key.toUpperCase()).join(' '))
    var keyDiv = $('<div>').append(keyView);

    keyDiv.css(keyCss);
    keyDiv.click(function(event){
      if (startTime == undefined) {
        startTime = performance.now();
      }
      $("#input").append(' ' + $.trim($(this).text().replace(/\s+/g, '')));
      socket.emit("request", {data: $.trim($("#input").text().toLowerCase())});
      return false;
    });

    $('#keycontainer').append(keyDiv);
  });

  setKeyVisible();
}

function setSuggest(wordList) {
  $("#wordcontainer").empty();
  wordList.forEach(function(key, index){
    var wordDiv = $('<div>').append(key);

    wordDiv.css(wordCss);
    if (key != '') {
      wordDiv.click(function(event){
        if (startTime == undefined) {
	  startTime = performance.now();
        }
        $("#selected").find('span').remove();
        $("#selected").append(' '+$.trim($(this).text()));
        if ($.trim($("#selected").text()) == $.trim($("#target").text())) {
	  setTarget();
        }
        $("#input").empty();
        socket.emit("request", {data: ''});
        return false;
      });
    }
    $("#wordcontainer").append(wordDiv);
  });
}

function getRandomInt() {
  var max = mackenzies.length - 1;
  return Math.floor(Math.random() * max);
}

function setTarget() {
  var minute = ((performance.now() - startTime) / 1000) / 60;
  var numWord = $("#target").text().replace(/\s+/g, '').length / 5;
  $("#wpm").text("WPM: " + (numWord / minute));
  startTime = undefined;
  $("#target").text(mackenzies[getRandomInt()].toLowerCase());
  $("#selected").empty();
}

$(document).ready(function(){
  socket = io.connect("http://" + document.domain + ":" + location.port + "/mynamespace");
  socket.on('response', function(msg){
    keyboard = msg.data.letter.split(",");
    setKeyboard();

    var wordList = msg.data.word.split(",");
    setSuggest(wordList);

    var nowInput = $.trim($("#input").text());
    $("#selected").find('span').remove();
    if (nowInput != '') {
      var nowInputList = nowInput.split(' ');
      var newNowInput = $.trim(wordList[0].slice(0, nowInputList.length));
      var preDiv = $('<span>').append(' ' + newNowInput);
      preDiv.css({
        "color": "gray"
      });
      $("#selected").append(preDiv);
    }
  });

  $("#target").text(mackenzies[getRandomInt()].toLowerCase());

  $('#keycontainer').on('swiperight', function(event){
    if (cursor == 0) {
      return;
    }
    cursor--;
    setKeyVisible();
  });

  $('#keycontainer').on('swipeleft', function(event){
    if (cursor == 2) {
      return;
    }
    if (startTime == undefined) {
      startTime = performance.now();
    }
    cursor++;
    setKeyVisible();
  });

  $('#inputspace').on('swipeup', function(event){
    var preInput = $.trim($("#input").text());
    if (preInput == '') {
      var preSelected = $.trim($("#selected").text());
      var preSelectedList = preSelected.split(' ');
      preSelectedList.pop();
      var select = preSelectedList.join(' ');
      $("#selected").text($.trim(select));
      socket.emit("request", {data: ''});
    } else {
      var preInputList = preInput.split(' ');
      preInputList.pop();
      var input = preInputList.join(' ');
      $("#input").text($.trim(input));
      socket.emit("request", {data: $.trim($("#input").text().toLowerCase())});
    }
  });
});
