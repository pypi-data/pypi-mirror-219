$(document).ready(function(){
    /*$(document).bind('keydown',function(e){
        if ( e.keyCode == 123 /!* F12 *!/) {
            alert("F12 사용이 불가합니다.");
            e.preventDefault();
            e.returnValue = false;
        }
    });*/
});

/**
 * Json Type Ajax Function
 *
 * @param url
 * @param data
 * @param successFn
 */
function fn_ajax_json(url, data, type, successFn){
    $.ajax({
        type: 'post',
        cache: false,
        url: url,
        data: data,
        dataType: type,
        success: successFn,
        error: function() {
            loading.hide();
            alert("일시적인 오류가 발생되었습니다.\n현재 페이지를 새로고침 합니다.");
            return false;
        }
    });
}

function fn_ajax_json2(url, data, type, successFn){
    $.ajax({
        type: 'post',
        cache: false,
        async : false,
        url: url,
        data: data,
        dataType: type,
        success: successFn,
        error: function() {
            loading.hide();
            alert("일시적인 오류가 발생되었습니다.\n현재 페이지를 새로고침 합니다.");
            return false;
        }
    });
}

function fn_ajax_jsonp(url, data, type, successFn){
    $.ajax({
        type: 'post',
        cache: false,
        async : false,
        url: url,
        data: data,
        dataType: type,
        success: successFn,
        error: function() {
            loading.hide();
            alert("일시적인 오류가 발생되었습니다.\n현재 페이지를 새로고침 합니다.");
            return false;
        }
    });
}



/**
 * Json Type Ajax Function
 *
 * @param url
 * @param data
 * @param successFn
 */
function fn_ajax_file_json(url, data, type, successFn){
    $.ajax({
        type: 'post',
        cache: false,
        url: url,
        data: data,
        dataType: type,
        contentType: false,
        processData: false,
        success: successFn,
        error: function() {
            loading.hide();
            alert("일시적인 오류가 발생되었습니다.\n현재 페이지를 새로고침 합니다.");
            location.href=location.href;
            return false;
        }
    });
}

/**
 * Json Type Ajax Function
 *
 * @param url
 * @param data
 * @param successFn
 */
function fn_ajax_juso_json(type, url, header, data, datatype, successFn){
    $.ajax({
        type: type,
        cache: false,
        url: url,
        headers: header,
        data: data,
        dataType: datatype,
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        success: successFn,
        error: function() {
            loading.hide();
            alert("일시적인 오류가 발생되었습니다.\n현재 페이지를 새로고침 합니다.");
            location.href=location.href;
            return false;
        }
    });
}

/**
 * INPUT TEXT NULL 체크
 *
 * @param obj
 *            확인할 객체
 * @returns {Boolean}
 */
function fn_text_null_check(obj){
    var re_val=true;
    obj.each(function(index, item){
        if($(item).hasClass('dates')){
            var obj_title=$(item).attr('title');
            var start_input=$(item).parent().find('input[type=text]:eq(0)');
            var end_input=$(item).parent().find('input[type=text]:eq(1)');
            var start_val=Number($(item).parent().find('input[type=text]:eq(0)').val().replace(/[-|.]/g, ""));
            var end_val=Number($(item).parent().find('input[type=text]:eq(1)').val().replace(/[-|.]/g, ""));
            if($(item).hasClass('null_false')){
                if(!start_val){
                    start_input.focus();
                    alert(obj_title + " 시작일은 필수 입력란 입니다. 해당란을 입력해 주십시오.");
                    re_val=false;
                    return false;
                }else if(!end_val){
                    end_input.focus();
                    alert(obj_title + " 종료일은 필수 입력란 입니다. 해당란을 입력해 주십시오.");
                    re_val=false;
                    return false;
                }else{
                    if(start_val > end_val){
                        end_input.focus();
                        alert(obj_title + " 종료일은 시작일보다 빠를수 없습니다.");
                        re_val=false;
                        return false;
                    }
                }
            }else{
                if($(item).hasClass('validation')){
                    if(start_val > end_val){
                        end_input.focus();
                        alert(obj_title + " 종료일은 시작일보다 빠를수 없습니다.");
                        re_val=false;
                        return false;
                    }
                }
            }
        }else{
            if(!$(item).prop('disabled')){
                if($(item).hasClass('null_false')){
                    if($(item).hasClass('editor')){
                        var validator=new Trex.Validator();
                        var content=Editor.getContent();
                        if(!validator.exists(content)){
                            alert('내용을 입력하세요');
                            re_val=false;
                            Editor.focus();
                            return false;
                        }
                    }else{
                        var obj_title = $(item).attr('title');
                        if(obj_title == ""){
                            obj_title=$('label[for=' + $(item).attr('id') + ']').text().replace(/<(\/)?([a-zA-Z]*)(\s[a-zA-Z]*=[^>]*)?(\s)*(\/)?>/g, "").replace(/[*]/gi, "").replace(/\n/gi, "");
                        }
                        if($(item).val() == ""){
                            $(item).focus();
                            alert(obj_title + "는(은) 필수 입력란 입니다.\n해당란을 입력(선택)해 주십시오");
                            re_val=false;
                            return false;
                        }else{
                            if($(item).hasClass('validation')){
                                var validation_data=fn_validation_check($(item));
                                if(validation_data[0]){
                                    $(item).val('');
                                    $(item).focus();
                                    alert(validation_data[1]);
                                    re_val=false;
                                    return false;
                                }
                            }
                        }
                    }
                }else{
                    if($(item).val() != ""){
                        if($(item).hasClass('validation')){
                            var validation_data=fn_validation_check($(item));
                            if(validation_data[0]){
                                $(item).val('');
                                $(item).focus();
                                alert(validation_data[1]);
                                re_val=false;
                                return false;
                            }
                        }
                    }
                }
            }
        }
    });
    return re_val;
}

/*******************************************************************************
 * 영문 숫자 한글 및 기타 체크
 *
 * @param type
 *            체크할 타입
 * @param msg
 *            체크할 메시지
 * @returns {Array}
 */
function fn_validation_check(element){

    var return_ck=null;
    var return_msg=null;
    var validation_type=null;

    if(element.hasClass('number')){
        validation_type=/^[0-9]+$/;
        return_msg="숫자만 입력해주세요.";
    }else if(element.hasClass('double')){
        validation_type=/^[+-]?\d*(\.?\d*)$/;
        return_msg="소수점을 포함한 숫자만 입력하세요.";
    }else if(element.hasClass('eng')){
        validation_type=/^[A-Za-z]$/;
        return_msg="영문만 입력해주세요.";
    }else if(element.hasClass('eng_number')){
        validation_type = /^[a-zA-Z0-9]+$/;
        return_msg="영문과 숫자 조합으로 입력해주세요.";
    }else if(element.hasClass('kor')){
        validation_type=/^[가-힣\s]+$/;
        return_msg="한글만 입력해주세요.";
    }else if(element.hasClass('mail')){
        validation_type=/([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        return_msg="메일만 입력해주세요.";
    }else if(element.hasClass('all')){
        validation_type=/[^(가-힣a-zA-Z0-9)]/;
        return_msg="특수기호는 입력할수 없습니다.";
    }else if(element.hasClass('latlng')){
        validation_type=/^[0-9-.]+$/;
        return_msg="좌표만 입력해주세요.";
    }else if(element.hasClass('mix_engnum')){
        validation_type = /[^a-z0-9]+|^([a-z]+|[0-9]+)$/i;
        return_msg="비밀번호는 영문과 숫자 조합으로 입력해주세요.";
    }

    if(validation_type == null){
        return_ck=true;
        return return_values;
    }

    if(validation_type.test(element.val())){
        return_ck=false;
    }else{
        return_ck=true;
    }

    if(element.hasClass('length')){
        if(element.val().length > Number(element.attr('maxlength')) && element.val().length < Number(element.attr('minlength'))){
            return_msg = obj_title+"는(은) "+element.attr('minlength')+"~"+element.attr('maxlength')+"자 사이의 "+return_msg;
            element.val('');
            element.focus();
            return_ck=false;
        }
    }

    var return_values=[];
    return_values[0]=return_ck;
    return_values[1]=return_msg;
    return return_values;
}

function fn_open_window(url,intWidth,intHeight) {
    var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
    var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;

    var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
    var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

    var left = ((width / 2) - (570 / 2)) + dualScreenLeft;
    var top = ((height / 2) - (420 / 2)) + dualScreenTop;

    window.open(url, "_blank", "width="+intWidth+",height="+intHeight+",scrollbars=yes, resizable=yes, top=" + top + ", left=" + left);
}

function fn_open_modal(url,intWidth,intHeight, obj) {
    var arg = obj;

    var retVal = window.showModalDialog(url, arg, "dialogWidth:"+intWidth+"px;dialogHeight:"+intHeight+"px;status:no;help:no;location:no");

    return retVal;
}

/**
 * 데이터 연계 호출
 * @param json
 * @param targetUrl
 * @param data
 * @returns
 */
function firDataLink(formId, data){
	var url = '/link/dataLink.do';
	
	if(data != null && data != ''){
    	var data = data;
    }
    else {
    	var data = $('#' + formId).serialize();
    }
	var successFn = function(json){
	    if(json.RESULT_DATALINK == 'OK'){
			//alert('연계 성공');
	    }
	    else {
			alert('데이터 연계 중 오류가 발생되었습니다.');
			return;
	    }
	}
	fn_ajax_json(url, data, 'json', successFn);
}