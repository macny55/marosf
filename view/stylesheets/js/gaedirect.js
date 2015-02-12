/*!
* gaedirect v3.2.0
* *
* Copyright 2012, Katsuyuki Seino
* Licensed under the GPL Version 2 licenses.
* http://jquery.org/license
*
* Date: Mon May 29 2012
*/
function gae(){
	return "/gaedirect";
}
function add(kind, key, props){
	var query = {};
	query["op"] = "add";
	query["rv"] = "deli";
	return mod(query,kind,key,props);
}

function addj(kind, key, props){
	var query = {};
	query["op"] = "add";
	query["rv"] = "json";
	return modj(query,kind,key,props);
}

function upd(kind, key, props){
	var query = {};
	query["op"] = "upd";
	query["rv"] = "deli";
	return mod(query,kind,key,props);
}

function updj(kind, key, props){
	var query = {};
	query["op"] = "upd";
	query["rv"] = "json";
	return modj(query,kind,key,props);
}

function mod(query,kind,key,props){
	query["kind"] = kind;
	query["key"] = key;
	query["id"] = props;
	var ids = props.split(",");
	query["val"] = "";
	for(var i = 0; i < ids.length ; i++){
		var value = "";
		var ids2 = "";
		var type2 = "";
		if(ids[i].substr(2,1)!=":"){
			ids2 = ids[i];			
		}else{
			ids2 = ids[i].substr(3);
			type2 = ids[i].substr(0,2);
		}		
		var control = ""; 
		var radioval = "";
		var checkval = new Array();
		var node = document.getElementById(ids2);
		/////////////////////////////////////////
		//  Start Add for v30
		//
		if(node == -1 || node == null ) { 
			value = "";
		}else
		/////////////////////////////////////////
		//  End Add for v30
		//			
		if(node.hasChildNodes()) {
			/*  for radio and check and select  */                
			if(node.nodeName == "SELECT"){
				value = $("#"+ids2).val(); 
			}else{
				var len = node.childNodes.length;
				for(var j=0; j < parseInt(len); j++){
					if(node.childNodes[j].nodeName == "INPUT"){
						if(node.childNodes[j].getAttribute("type")=="radio"){
							control = "radio";
							if(node.childNodes[j].checked){
								radioval = node.childNodes[j].getAttributeNode("value").value;
								break;
							}	
						}else if(node.childNodes[j].getAttribute("type")=="checkbox"){
							control = "checkbox";
							if(node.childNodes[j].checked){
								checkval.push(node.childNodes[j].getAttributeNode("value").value);
							}
						}	
					}			
				}
				if(control == "radio"){
					value = radioval;
				}else if(control == "checkbox"){
					var checkval2 = "";
					for(var k = 0; k < checkval.length -1; k++){
						checkval2 += checkval[k] + ","; 
					}
					checkval2 += checkval[k];
					value = checkval2;
				}
			}
		}else { 
			value = $("#"+ids2).val(); 
		}		
		if (value == "" || value == "undefined"){		
			/* value = "N/A";  */			
			if(type2.length == 2){
				if(type2=="sh" || type2=="in" || type2=="lo"){
					value = 0;
				}else if(type2=="fl" || type2=="do"){
					value=0.0;
				}
			}else{
				value="na";
			}							
		}
		if(i < ids.length - 1){
			query["val"] += value + "<p>";
		}else{
			query["val"] += value;
		}
	}	
	return query;
}

function modj(query,kind,key,props){
	var value = null;
	query["kind"] = kind;
	query["key"] = key;
	query["id"] = props;
	var ids = props.split(",");
	query["val"] = "";
	for(var i = 0; i < ids.length ; i++){
		var value = "";
		var ids2 = "";
		var type2 = "";
		if(ids[i].substr(2,1)!=":"){
			ids2 = ids[i];
		}else{
			ids2 = ids[i].substr(3);
			type2 = ids[i].substr(0,2);
		}		
		var control = ""; 
		var radioval = "";
		var checkval = new Array();
		var node = document.getElementById(ids2);
		/////////////////////////////////////////
		//  Start Add for v30
		//
		if(node == -1 || node == null ) { 
			value = "";
		}else
		/////////////////////////////////////////
		//  End Add for v30
		//	
		if(node.hasChildNodes()) {
			/*  for radio and check and select  */                
			if(node.nodeName == "SELECT"){
				value = $("#"+ids2).val(); 
			}else{
				var len = node.childNodes.length;
				for(var j=0; j < parseInt(len); j++){
					if(node.childNodes[j].nodeName == "INPUT"){
						if(node.childNodes[j].getAttribute("type")=="radio"){
							control = "radio";
							if(node.childNodes[j].checked){
								radioval = node.childNodes[j].getAttributeNode("value").value;
								break;
							}	
						}else if(node.childNodes[j].getAttribute("type")=="checkbox"){
							control = "checkbox";							
							if(node.childNodes[j].checked){
								//alert(node.childNodes[j].getAttributeNode("value").value);
								checkval.push(node.childNodes[j].getAttributeNode("value").value);
							}
						}	
					}			
				}
				if(control == "radio"){
					value = radioval;
				}else if(control == "checkbox"){
					var checkval2 = "";
					for(var k = 0; k < checkval.length -1; k++){
						checkval2 += checkval[k] + ","; 
					}
					checkval2 += checkval[k];
					value = checkval2;
				}
			}
		}else { 
			value = $("#"+ids2).val(); 
		}	
		
		if (value == "" || value == "undefined"){		
			/* value = "N/A";  */			
			if(type2.length == 2){
				if(type2=="sh" || type2=="in" || type2=="lo"){
					value = 0;
				}else if(type2=="fl" || type2=="do"){
					value = 0.0;
				}
			}else{
				value = "na";
			}							
		}
		if(i < ids.length - 1){
			query["val"] += value + "<p>";
		}else{
			query["val"] += value;
		}
	}
	return query;
}

function rev(kind, key, props){
	var query = {};
	query["op"] = "rev";
	query["rv"] = "deli";
	query["kind"] = kind;
	query["key"] = key;
	query["id"] = props;
	return query;
}

function revj(kind, key, props){
	var query = {};
	query["op"] = "rev";
	query["rv"] = "json";
	query["kind"] = kind;
	query["key"] = key;
	query["id"] = props;
	return query;
}

function del(kind, key){
	var query = {};
	query["op"] = "del";
	query["rv"] = "deli";
	query["kind"] = kind;
	query["key"] = key;	
	query["id"] = "";
	query["val"] = "";
	return query;
}

function delj(kind, key){
	var query = {};
	query["op"] = "del";
	query["rv"] = "json";
	query["kind"] = kind;
	query["key"] = key;	
	query["id"] = "";
	query["val"] = "";
	return query;
}

/////////////////////////////////////////////
//  Add for 3.0
//  login
function login0(){
	return "/uadmin";
}
function login1(){
	var query = {};
	query["userid"]  = document.getElementById("userid").value;
	query["passwd"]  = document.getElementById("passwd").value;
	return query;
}
function login2(res){
	var dat = $.parseJSON(res);
	if(dat.status == "OK"){
		menuval = 1;
		var meta= document.createElement("meta");
		meta.setAttribute("http-equiv", "refresh");
		meta.setAttribute("content", "0.1;url="+dat.udirec);
		var parent = document.getElementsByTagName("body"); 
		parent[0].appendChild(meta); 
		var direc = dat.udirec.split("/");
		var storage = sessionStorage;
		storage.setItem("ucap", direc[1]);
	}else if(dat.status == "NO"){
		return dat.comment;
	}
}

function evalmenu(){
	var storage = sessionStorage;
	var direc1 = storage.getItem("ucap");
	if(location.href.indexOf(direc1) < 0){
		var elm = document.getElementsByTagName("body");
		while(elm[0].firstChild){
			elm[0].removeChild(elm[0].firstChild);
		}			
	}
}

function ginit (){
	var query = {};
	query["OFFSET"] = "";
	query["LIMIT"] = "";
	query["EQUAL"] = "";
	query["NOT_EQUAL"] = "";
	query["SORT"] = "";
	query["LESS_THAN"] = "";
	query["LESS_THAN_OR_EQUAL"] = "";
	query["GREATER_THAN"] = "";
	query["GREATER_THAN_OR_EQUAL"] = "";
	query["IN"] = "";
	return query;
}
function qinit(kind, prop){
	var query = ginit();
	query["rv"] = "deli";
	query["kind"] = kind;
	query["key"] = "none";		
	query["id"] = prop;
	return query;
}

function qinitj(kind, prop){
	var query = ginit();
	query["rv"] = "json";
	query["kind"] = kind;
	query["key"] = "none";		
	query["id"] = prop;
	return query;
}

function dsp(resp, props, target){
	if(resp.substr(0,3)=="NO:"){
		if (arguments.length == 2) {		
			if(document.getElementById("status")){
				var node = document.getElementById("status");
				if(node.nodeName != "INPUT"){
					$("#status").text(resp.substr(3));
				}else{
					$("#status").val(resp.substr(3));
				}
				return;
			}else if(document.getElementById("stat")){
				var node = document.getElementById("stat");
				if(node.nodeName != "INPUT"){
					$("#stat").text(resp.substr(3));
				}else{
					$("#stat").val(resp.substr(3));
				}	
				return;
			}
		}else if(arguments.length == 3){
			var node = document.getElementById(target);
			if(node.nodeName != "INPUT"){
				$("#"+target).text(resp.substr(3));
			}else{
				$("#"+target).val(resp.substr(3));
			}	
			return;
		}		
	}
	var val = resp.split("<p>");
	var ids = props.split(",");
	var ids2 = "";
	var type2 = "";
	for(var i = 0; i < ids.length ; i++){
		if(ids[i].substr(2,1)!=":"){
			ids2 = ids[i];
		}else{
			ids2 = ids[i].substr(3);
			type2 = ids[i].substr(0,2);
		}
		var node = document.getElementById(ids2);
		if(node.hasChildNodes()) {
			if(node.nodeName == "SELECT"){
				$("#"+ids2).val(val[i]);				
			}else{
				var len = node.childNodes.length;
				for(var j=0; j < parseInt(len); j++){
					if(node.childNodes[j].nodeName == "INPUT"){
						if(node.childNodes[j].getAttribute("type")=="radio"){
							var name = node.childNodes[j].getAttribute("name");
							var dat = new Array(val[i]);							
							$("input[name="+name+"]").val(dat);
						}else if(node.childNodes[j].getAttribute("type")=="checkbox"){
							var name = node.childNodes[j].getAttribute("name");
							var dat = val[i].split(",");
							$("input[name="+name+"]").val(dat);
						}else if(node.childNodes[j].getAttribute("type")=="input"){
							$("#"+ids2).val(val[i]); 
						}else {
							$("#"+ids2).val(val[i]); 
						}						
					}			
				}		
			}
		}else if(node.nodeName == "INPUT"){
			$("#"+ids2).val(val[i]); 
		}else if(node.nodeName == "TEXTAREA"){
			$("#"+ids2).val(val[i]); 
		}else{
			$("#"+ids2).text(val[i]); 
		}
	}	
}	

function dspj(res, props, target){
	//alert("dspj");
	var jdat = $.parseJSON(res);
	//alert(jdat.status);
	$("#stat").text(jdat.status);	 
	if(res.search(",") == -1){
		return;
	}
	var ids = props.split(",");
	var ids2 = "";
	var type2 = "";
	for(var i = 0; i < ids.length ; i++){
		if(ids[i].substr(2,1)!=":"){
			ids2 = ids[i];
		}else{
			ids2 = ids[i].substr(3);
			type2 = ids[i].substr(0,2);
		}
		var node = document.getElementById(ids2);
		if(node == null){ continue;	}
		if(node.hasChildNodes()) {
			//alert(0);
			if(node.nodeName == "SELECT"){
				$("#"+ids2).val(eval("jdat."+ids2));
			}else{
				var len = node.childNodes.length;
				for(var j=0; j < parseInt(len); j++){
					if(node.childNodes[j].nodeName == "INPUT"){
						if(node.childNodes[j].getAttribute("type")=="radio"){
							var name = node.childNodes[j].getAttribute("name");
							var rdat = new Array(eval("jdat."+ids2));
							$("input[name="+name+"]").val(rdat);
						}else if(node.childNodes[j].getAttribute("type")=="checkbox"){
							var name = node.childNodes[j].getAttribute("name");
							var rdat = new Array(eval("jdat."+ids2));
							var chkval = (""+ rdat).split(",");
							$("input[name="+name+"]").val(chkval);
						}else if(node.childNodes[j].getAttribute("type")=="input"){
							$("#"+ids2).val(eval("jdat."+ids2));
						}else {
							$("#"+ids2).val(eval("jdat."+ids2));
						}						
					}			
				}		
			}
		}else if(node.nodeName == "INPUT"){
			//alert(1);
			//alert(eval("jdat."+ids2));
			$("#"+ids2).val(eval("jdat."+ids2));
		}else if(node.nodeName == "TEXTAREA"){
			//alert(2);
			//alert(eval("jdat."+ids2));
			$("#"+ids2).val(eval("jdat."+ids2));
		}else{
			//alert(3);
			//alert(eval("jdat."+ids2));
			$("#"+ids2).text(eval("jdat."+ids2));
		}
	}	
}

function dsp2(res, id, target){	
	var tags = "";
	var head = id.split(",");
	var tags = "<table border='1'><tr><th>key</th>";
	for (var i=0; i < head.length; i++){
		tags += "<th>" + head[i] + "</th>";	
	}
	tags += "</tr>"; 
	//alert("res="+res);
	var entity = res.split("<e>");
	for(var i = 0; i < entity.length; i++){
		tags += "<tr>";
		//alert(entity[i]);
		var property = entity[i].split("<p>");
		//alert(property.length);
		for (var j = 0; j < property.length; j++) {
			tags += "<td>" + property[j] + "</td>";
		}
		tags += "</tr>";	 
	}
	tags += "</table>";
	if (arguments.length == 2) {
		//$("#out").html(tags);
		$("#show").html(tags);
	}else if(arguments.length == 3){
		$("#"+target).html(tags);
	}	
}

function dsp2j(res, id, target){	
	var ids0 = id.split(",");
	var ids = "key,";
	var ids1 = "";
	var ids = new Array();
	ids.push("key");
	for (var i=0; i < ids0.length; i++){
		if(ids0[i].substr(2,1) != ":"){
			ids1 = ids0[i];
		}else{
			ids1 = ids0[i].substr(3);
		}
		ids.push(ids1);
	}	
	var tags = "<table border='1'><tr>";
	for (var i=0; i < ids.length; i++){
		tags += "<th>" + ids[i] + "</th>";	
	}
	tags += "</tr>"; 
	var dat = $.parseJSON(res);
	for(var i = 0; i < dat.entries.length; i++){
		tags += "<tr>";
		for (var j = 0; j < ids.length; j++){
			tags += "<td>" + eval("dat.entries[i]." + ids[j]) + "</td>";	
		}	
		tags += "</tr>";		
	}
	tags += "</table>";
	if (arguments.length == 2) {
		$("#show").html(tags);
	}else if(arguments.length == 3){
		$("#"+target).html(tags);
	}		
}

function getprop(prop){
	var prop1 = prop.split(",");
	var prop2 = "";
	for(var i = 0; i < prop1.length; i++){
		if(prop1[i].indexOf(":")== 2){
			prop2 += prop1[i].substr(3)+ ",";
		}else{
			prop2 += prop1[i]+ ",";
		}
	}
	return prop2.substr(0, prop2.length-1);
}	
function getXhrObj() {
	var xhrObj;
	if (window.XMLHttpRequest) {
		try {
			xhrObj = new XMLHttpRequest();
		} catch (e) {
			xhrObj = false;
		}
	 }else if (window.ActiveXObject){
		try {
			 xhrObj = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e){
			try {
				xhrObj = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (E){
				xhrObj = false;
			}
		}
	}
	return xhrObj;
}
function getsyn(prog, query){
	var indata = setquery(query);
	var xhrObj = getXhrObj();
	xhrObj.open("get", prog+"?"+indata, false);
	xhrObj.send(null);
	return xhrObj.responseText;
}
function getasyn(prog, query){
	var indata = setquery(query);
	var xhrObj = getXhrObj();
	xhrObj.open("get", prog+"?"+indata);
	xhrObj.setRequestHeader("If-Modified-Since", "01 Jan 2000 00:00:00 GMT");
	xhrObj.onreadystatechange = function(){
		if(xhrObj.readyState == 4){
			if(xhrObj.status == 200){
				return xhrObj.responseText;
			}
	    }
	}
	xhrObj.send(null);
}
function postsyn(prog, query){
	var indata = setquery(query);
	var xhrObj = getXhrObj();
	xhrObj.open("post", prog, false);
	xhrObj.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhrObj.send(indata);
	return xhrObj.responseText;	
}

function postasyn(prog, query){
	var indata = setquery(query);
	var xhrObj = getXhrObj();
	xhrObj.open("post", prog);
	xhrObj.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhrObj.setRequestHeader("If-Modified-Since", "01 Jan 2000 00:00:00 GMT");
	xhrObj.onreadystatechange = function(){
		if(xhrObj.readyState == 4){
			if(xhrObj.status == 200){
				//func(xhrObj.responseText);
				return xhrObj.responseText;
			}
	    }
	}
	xhrObj.send(indata);
}
function setquery(query){
	var indata = "";
	var j = 0;
	for (var i in query) {
		if(j==0){
			indata = i+"="+query[i];
			++j;
		}else{
			indata += "&"+i+"="+query[i];
		}
	}
	return indata;
}
function getsynx(prog){
	var xhrObj = getXhrObj();
	xhrObj.open("get", prog, false);
	xhrObj.send(null);
	return xhrObj.responseXML;
}
/* ******************************************************** *
 *                   For Channel API 
 * ******************************************************** */
function capi(){
	return "/channelapi";
}
function getToken(clientId){
	return getsyn(capi()+"?action=open&clientId="+clientId);
}
function cInit(clientId){
	return getsyn(capi()+"?action=cinit&clientId="+clientId);
}

function cClose(clientId){
	return getsyn(capi()+"?action=close&clientId="+clientId);
}
/* ******************************************************** *
 *                   For Image Data 
 * ******************************************************** */
function imageup(){
	return "/imageup";
}
function gen(id){
	var form = "<table><tr><td>aaa</td><td>bbb</td></tr><tr><td>ccc</td><td>ddd</td></tr></table>"; 
	document.getElementById(id).innerHTML = form;		
}
