function resize(Tarea){ 
//    var areaH = Tarea.style.height;
//  if(Tarea.value == ""){areaH=26+"px";}
//    areaH = parseInt(areaH) - 30;
//  if(areaH < 30){areaH = 30}
//    Tarea.style.height = areaH + "px";
//  Tarea.style.height = (parseInt(Tarea.scrollHeight)) + "px";
  }
/*
jQuery(function($){
  $('p#contents,p#memo,p#tag').click(function(){
    if(!$(this).hasClass('on')){
      $(this).addClass('on');
      var txt = $(this).text();
      $(this).html('<textarea onkeyup="resize(this)" name="tag">'+txt+'</textarea>');
      $('textarea').autosize();
      $('p#contents > textarea,p#memo > textarea,p#tag > textarea').focus().blur(function(){
        var inputVal = $(this).val();
        if(inputVal===''){
          inputVal = this.defaultValue;
        }else if(inputVal===this.defaultValue){
          inputVal = this.defaultValue;
        }else{
          //POST処理
	    disp_save_contents();
        };
        $(this).parent().removeClass('on').text(inputVal);
      });
    };
  });
});
*/

jQuery(function($){
  $('p#contents').click(function(){
    var form_name = $(this).parent("form").attr("name");
    if(!$(this).hasClass('on')){
      $(this).addClass('on');
      var txt = $(this).text();
      $(this).html('<textarea onkeyup="resize(this)" name="contents">'+txt+'</textarea>');
      $('textarea').autosize();
      $('p#contents > textarea').focus().blur(function(){
        var inputVal = $(this).val();
        if(inputVal===''){
          inputVal = this.defaultValue;
        }else if(inputVal===this.defaultValue){
          inputVal = this.defaultValue;
        }else{
          //POST処理
	    if (disp_save_contents(form_name) == 1){
		inputVal = this.defaultValue;
	    }
        };
        $(this).parent().removeClass('on').text(inputVal);
      });
    };
  });
});

jQuery(function($){
  $('p#memo').click(function(){
    var form_name = $(this).parent("form").attr("name");
    if(!$(this).hasClass('on')){
      $(this).addClass('on');
      var txt = $(this).text();
      $(this).html('<textarea onkeyup="resize(this)" name="memo">'+txt+'</textarea>');
      $('textarea').autosize();
      $('p#memo > textarea').focus().blur(function(){
        var inputVal = $(this).val();
        if(inputVal===''){
          inputVal = this.defaultValue;
        }else if(inputVal===this.defaultValue){
          inputVal = this.defaultValue;
        }else{
          //POST処理
	    if (disp_save_contents(form_name) == 1){
		inputVal = this.defaultValue;
	    }
        };
        $(this).parent().removeClass('on').text(inputVal);
      });
    };
  });
});

jQuery(function($){
  $('p#tag').click(function(){
    var form_name = $(this).parent("form").attr("name");
    if(!$(this).hasClass('on')){
      $(this).addClass('on');
      var txt = $(this).text();
      $(this).html('<textarea onkeyup="resize(this)" name="post_tag">'+txt+'</textarea>');
      $('textarea').autosize();
      $('p#tag > textarea').focus().blur(function(){
        var inputVal = $(this).val();
        if(inputVal===''){
          inputVal = this.defaultValue;
        }else if(inputVal===this.defaultValue){
          inputVal = this.defaultValue;
        }else{
          //POST処理
	    if (disp_save_contents(form_name) == 1){
		inputVal = this.defaultValue;
		}
        };
        $(this).parent().removeClass('on').text(inputVal);
      });
    };
  });
});

function disp_save_contents(form_name){ 
  // 「OK」時の処理開始 ＋ 確認ダイアログの表示
  if(window.confirm('Do you want to save the changes? \n　It cannot be undone.')){
    //location.href = "http://kindle-loves-tweet.appspot.com/{{ url }}";
      var f = document.forms[form_name];
      f.submit();
      return 0;
  }else{
      return 1;
      }
}

function delete_content(param,usr_id,asin,tag){ 
  // 「OK」時の処理開始 ＋ 確認ダイアログの表示
  if(window.confirm('Do you want to delete this content? \n It cannot be undone.')){
      location.href = 'http://project-marosf.appspot.com/delete_content?param=' + param + '&usr_id=' + usr_id + '&asin=' + asin + '&tag=' + tag;
    //location.href = 'http://localhost:8090/delete_content?param=' + param + '&usr_id=' + usr_id + '&asin=' + asin + '&tag=' + tag;
    //location.href = "http://kindle-loves-tweet.appspot.com/{{ url }}";
      return 0;
  }else{
      return 1;
      }
}


function disp_block_line(count){
	//「a」タグに対して動作を定義する。
	//hoverメソッドでonmouseoverとonmouseoutが一気に指定できる。
    var i;
    for(i = 0;i<count;i++){
	$('.delete_button_' + String(i)).hover(
		//over時の動作指定
		function(){
			//parentでaの一つ上のHTML要素つまり親要素を取得できる。
			//そしてその取得した親要素に対してcssメソッドで背景色を変更
			$(this).parent().parent().css( 'background-color', '#F39C12' );
		}
		,
		//out時の動作指定
		function(){
			//over時と同じ。色を元に戻している。
			$(this).parent().parent().css( 'background-color', '#ECF0F1' );
		}
	);}
};

