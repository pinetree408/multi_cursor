$.mobile.autoInitializePage = false;
var socket;
var keyboard;
var cursor = 0;
var windowIndex = [[0,2], [3,5], [5,7]];
var startTime;


function setKeyVisible() {
  $('#keycontainer').children().each(function(index) {
    if (windowIndex[cursor][0] <= index && index <= windowIndex[cursor][1]) {
      $('#keycontainer').children().eq(index).show();
    } else {
      $('#keycontainer').children().eq(index).hide();
    }
  });
}

function getKeyboard() {
  var suggestedKey = '';
  $("#keycontainer").children().each(function(index) {
    suggestedKey = suggestedKey + ' ' + $("#keycontainer").children().eq(index).text().replace(/\s+/g, '');
  });
  return $.trim(suggestedKey);
}

function getVisibleKeyboard() {
  var visibleKey = '';
  $('#keycontainer').children().each(function(index) {
    if (windowIndex[cursor][0] <= index && index <= windowIndex[cursor][1]) {
      visibleKey = visibleKey + ' ' + $("#keycontainer").children().eq(index).text().replace(/\s+/g, '');
    }
  });
  return $.trim(visibleKey);
}

function setKeyboard() {
  $("#keycontainer").empty();
  cursor = 0;

  keyboard.forEach(function(key, index){
    var keyView = $.trim(Array.from(key.toUpperCase()).join(' '))
    var keyDiv = $('<div>').append(keyView);

    keyDiv.addClass("key");
    keyDiv.click(function(event){
      if (startTime == undefined) {
        startTime = performance.now();
      }
      $("#input").append(' ' + $.trim($(this).text().replace(/\s+/g, '')));
      socket.emit("request", {data: $.trim($("#input").text().toLowerCase())});
      socket.emit("logging", {
        target: $.trim($("#target").text()),
	input: key,
        word: getSuggest(),	
        key: getKeyboard(),
	visible: getVisibleKeyboard(),
	time: performance.now().toFixed(0).toString(),
	type: 'select_key'
      });
      return false;
    });

    $('#keycontainer').append(keyDiv);
  });

  setKeyVisible();
}

function getSuggest() {
  var suggestedWord = '';
  $("#wordcontainer").children().each(function(index) {
    suggestedWord = suggestedWord + ' ' + $("#wordcontainer").children().eq(index).text();
  });
  return $.trim(suggestedWord);
}

function setSuggest(wordList) {
  $("#wordcontainer").empty();
  wordList.forEach(function(key, index){
    var wordDiv = $('<div>').append(key);

    wordDiv.addClass("word");
    if (key != '') {
      wordDiv.click(function(event){
        if (startTime == undefined) {
	  startTime = performance.now();
        }
        $("#selected").find('span').remove();
        $("#selected").append(' '+$.trim($(this).text()));
        socket.emit("logging", {
          target: $.trim($("#target").text()),
	  input: key,
          word: getSuggest(),	
          key: getKeyboard(),
	  visible: getVisibleKeyboard(),
	  time: performance.now().toFixed(0).toString(),
	  type: 'select_word'
        });
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
  $("#wpm").text("WPM: " + (numWord / minute).toFixed(2));
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
      var preDiv = $('<span>').addClass("writing").append(' ' + newNowInput);
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
    socket.emit("logging", {
      target: $.trim($("#target").text()),
      input: 'swipe_right',
      word: getSuggest(),	
      key: getKeyboard(),
      visible: getVisibleKeyboard(),
      time: performance.now().toFixed(0).toString(),
      type: 'gesture_prev'
    });
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
    socket.emit("logging", {
      target: $.trim($("#target").text()),
      input: 'swipe_right',
      word: getSuggest(),	
      key: getKeyboard(),
      visible: getVisibleKeyboard(),
      time: performance.now().toFixed(0).toString(),
      type: 'gesture_next'
    });
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
    socket.emit("logging", {
      target: $.trim($("#target").text()),
      input: 'swipe_up',
      word: getSuggest(),	
      key: getKeyboard(),
      visible: getVisibleKeyboard(),
      time: performance.now().toFixed(0).toString(),
      type: 'gesture_delete'
    });
  });
});
