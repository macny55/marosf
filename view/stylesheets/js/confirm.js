function disp_confirm(usr_name){ 
    // 「OK」時の処理開始 ＋ 確認ダイアログの表示
    if(window.confirm('Welcome！ ' + usr_name + ' \n\n Is ' + usr_name + ' used by only Kindle ?')){
	location.href = "http://project-marosf.appspot.com/main";
	//location.href = "http://localhost:8090/main";
	return 0;
    }else{
	location.href = "http://project-marosf.appspot.com/logout";
	//location.href = "http://localhost:8090/logout";
	return 1;
    }
}