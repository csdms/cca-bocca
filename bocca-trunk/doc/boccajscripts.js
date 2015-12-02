// Execute a function on page load
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}

//addLoadEvent(populateTable);
addLoadEvent(function() {
  /* more code to run on page load */ 
});


function toUnicode(theString) {
  var unicodeString = '';
  for (var i=0; i < theString.length; i++) {
    var theUnicode = theString.charCodeAt(i).toString(16).toUpperCase();
    while (theUnicode.length < 4) {
      theUnicode = '0' + theUnicode;
    }
    theUnicode = '\\u' + theUnicode;
    unicodeString += theUnicode;
  }
  return unicodeString;
}

function floatLayer(SRC) {
	var tDIV = document.getElementById(SRC)
	var par = tDIV.parentNode;
	var posx = 0;
	var posy = 0;
	var left = 0;
	var top = 0;

	posx = par.offsetLeft + par.clientWidth/2;
	posy = par.offsetTop + 30;

	if (shorthelptext[SRC] == "undefined") {
		tDIV.innerHTML = "not supported";
	} else {
		tDIV.innerHTML = shorthelptext[SRC];
	}
	var floatWidth = tDIV.clientWidth;
	// Calculate the placement of the float layer
	top = (posy + 15) 
	if (posx + floatWidth + 20 > document.body.clientWidth) {
		if (posx > (floatWidth + 20))
			left = posx - floatWidth - 20
		else
			left = document.body.clientWidth - floatWidth
	} else {
		left = (posx + 20) 
	}
	tDIV.style.left = left + "px";
	tDIV.style.top = top + "px";
	tDIV.style.visibility = "visible";
	tDIV.style.cursor = "hand";
	//showHelp(SRC);
}


function hideLayer(SRC) {
	var tDIV = document.getElementById(SRC);
	tDIV.style.visibility = 'hidden';
}

function showHelp(command) {
	var helpBox = document.getElementById("helptext");
	var thestring = helptext[command];
	if (helpBox.firstChild) helpBox.removeChild(helpBox.firstChild);
	//prenode = document.createElement("pre");
	helpBox.appendChild(document.createTextNode(thestring));
	//helpBox.innerHTML = thestring;
}

function getElementsByAttribute(attr, val, container) {
	container = container || document
	var all = container.all || container.getElementsByTagName('*')
	var arr = []
	for ( var k = 0; k < all.length; k++)
		if (all[k].getAttribute(attr) == val)
			arr[arr.length] = all[k]
	return arr
}
