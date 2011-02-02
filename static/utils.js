
function $(id) {
	return document.getElementById(id);
}

function request(url, on_success, userdata, method, data) {
	if(!on_success) { on_success = null; }
	if(!method) { method = 'GET'; }
	if(!data) { data = null; }
	
	var xmlhttp = null;
	
	// Mozilla
	if(window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}
	
	// IE
	else if (window.ActiveXObject) {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.open(method, url, true);
	xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	if(data) {
		xmlhttp.setRequestHeader("Content-length", data.length);
	}
	xmlhttp.setRequestHeader("Connection", "close");
	xmlhttp.setRequestHeader("If-Modified-Since", "");
	xmlhttp.setRequestHeader("If-None-Match", "");
	xmlhttp.onreadystatechange = function() {
		if(xmlhttp.readyState != 4) {
			$('request_state').className = 'loading';
		}
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			if(on_success) {
				//document.write('<pre>' + xmlhttp.responseText + '</pre>');
				on_success(eval('(' + xmlhttp.responseText + ')'), userdata);
			}
			$('request_state').className = 'done';
		}
	}
	xmlhttp.send(data);
}

function tags2path(ts, t) {
	var s = '';
	for(var i in ts) {
		s += ts[i] + '/';
	}
	if(t != null) {
		s += t + '/';
	}
	return s;
}

function clear_node(n) {
	while(n.hasChildNodes()) {
		n.removeChild(n.firstChild);
	}
}

function set_text(n, t) {
	//var txt = document.createTextNode(t);
	
	//n.appendChild(txt);
	n.textContent = t;
	n.innerText = t;
}


// source: http://www.codeproject.com/KB/miscctrl/JS_Inspect_Object.aspx
function inspect(obj, maxLevels, level)
{
  var str = '', type, msg;

    // Start Input Validations
    // Don't touch, we start iterating at level zero
    if(level == null)  level = 0;

    // At least you want to show the first level
    if(maxLevels == null) maxLevels = 1;
    if(maxLevels < 1)     
        return '<font color="red">Error: Levels number must be > 0</font>';

    // We start with a non null object
    if(obj == null)
    return '<font color="red">Error: Object <b>NULL</b></font>';
    // End Input Validations

    // Each Iteration must be indented
    str += '<ul>';

    // Start iterations for all objects in obj
    for(property in obj)
    {
      try
      {
          // Show "property" and "type property"
          type =  typeof(obj[property]);
          str += '<li>(' + type + ') ' + property + 
                 ( (obj[property]==null)?(': <b>null</b>'):('')) + '</li>';

          // We keep iterating if this property is an Object, non null
          // and we are inside the required number of levels
          if((type == 'object') && (obj[property] != null) && (level+1 < maxLevels))
          str += inspect(obj[property], maxLevels, level+1);
      }
      catch(err)
      {
        // Is there some properties in obj we can't access? Print it red.
        if(typeof(err) == 'string') msg = err;
        else if(err.message)        msg = err.message;
        else if(err.description)    msg = err.description;
        else                        msg = 'Unknown';

        str += '<li><font color="red">(Error) ' + property + ': ' + msg +'</font></li>';
      }
    }

      // Close indent
      str += '</ul>';

    return str;
}


