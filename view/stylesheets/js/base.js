function url_jump() {
    document.form1.tag.blur();
    var num = document.form1.tag.selectedIndex;
    location.href = document.form1.tag.options[num].value;
}

function disp_logout(status){ 
    // 「OK」時の処理開始 ＋ 確認ダイアログの表示
    if(window.confirm( status  + '？')){
	location.href = "http://project-marosf.appspot.com/logout";
	//location.href = "http://localhost:8090/logout";
    }
}

function disp_re_get(){ 
    // 「OK」時の処理開始 ＋ 確認ダイアログの表示
    if(window.confirm('Data is updated')){
	//location.href = "http://kindle-loves-tweet.appspot.com/delete_all?usr_id={{usr_id}}";
        location.href = "http://project-marosf.appspot.com/main";
    }
}