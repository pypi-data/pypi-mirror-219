var oneNum = -1;

var areaCd = new Array('10','11','12','13','14','15','16','26','17','18','19','20','21','22','23','24','25');

/* 숫자키만 입력가능  */
$('.numOnly').keypress(function (event) {
    if (event.which && (event.which <= 47 || event.which >= 58) && event.which != 8) {
        event.preventDefault();
    }
});

$(document).ready(function(){
    gnb(); //GNB메뉴

    //소수점포함
    $('.num_only3').css('imeMode','disabled').keypress(function(event) {
        if(event.which && ( event.which < 45 || event.which > 57) ) {
            event.preventDefault();
        }
    }).keyup(function(){
        if( $(this).val() != null && $(this).val() != '' ) {
            $(this).val( $(this).val().replace(/[^\.0-9]/g, '') );
        }
    });

    //유관기관 선택
    $('#urlSelect').on('change',function(){
        var urlPage = $("select[name=urlSelect]").val();
        $('#urlGo').attr('href',urlPage);
    });
})

//GNB메뉴
function gnb(){
    if(oneNum != -1) activeSub();
    $("#gnb>ul").children("li").each(function(){
        $(this).mouseenter(function(){
            if(oneNum != -1) {
                $("#gnb>ul").children("li").eq(oneNum).removeClass("on");
            }
            $("#menu").stop().animate({height:323}, 400, "easeOutCubic").css("border-bottom","1px solid #d9d9db");
            $(this).addClass("on");
        })
            .focusin(function(){
                $(this).mouseenter();
            })

        $(this).mouseleave(function(){
            $(this).removeClass("on");
            $("#menu").stop().animate({height:60}, 400, "easeOutCubic").css("border-bottom","none");
            if(oneNum != -1) {
                activeSub()
            }
        })

            .focusout(function(){
                $(this).mouseleave();
            })
    });
}

function activeSub(){
    $("#gnb>ul").children("li").eq(oneNum).addClass("on");
}

/*kft 정보공개서*/
function isNumberKey(evt) {

    var _value = event.srcElement.value;

    // 소수점 둘째자리까지만 입력가능
    var _pattern2 = /^\d*[.]\d{2}$/; // 현재 value값이 소수점 둘째짜리 숫자이면 더이상 입력 불가

    if (_pattern2.test(_value)) {

        alert("소수점 둘째자리까지만 입력가능합니다.");
        return false;
    }
    return true;
}

function replaceAll(str, searchStr, replaceStr) {
    return str.split(searchStr).join(replaceStr);
}

function numberWithCommasRtn(x) {
    return  x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

}

function numberWithCommas(x) {
    var val = x.value;
    val = val.replace(/,/gi,"");
    val = val.replace(/\./g, "");
    if(isNaN(val) == true || x.value ==""){
        x.value = "";
    } else {
        val = replaceAll(val, ".", "");
        x.value = val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
}

//배열 합계 구하기 함수
function sum(array) {
    var result = 0;

    for (var i = 0; i < array.length; i++){
        result += array[i];
    }

    return numberWithCommasRtn(result);
}

/**
 * 도움말 팝업
 * @param url
 * @param intWidth
 * @param intHeight
 * @returns
 */
function OpenWindow(url, width, height) {
    var nm = "_blank";
    var option = 'width='+ width +', height='+ height +', resizable=1, scrollbars=1';
    window.open(url, "_blank", option);
}

function fn_html_regist(){
    /*daumEditor 내용 저장*/
    var content ="";
    try{
        content = Editor.getContent();
        $('#nttCn').val(content);
    }catch(ex){
        console.log("[WARNING] 다음에디터 못찾음");
    }
    fn_regist();
}

//상세보기
function fn_view(url){
    document.frm.action=url;
    document.frm.submit();
}

//삭제
function fn_delete(url){
    if(confirm("삭제하시겠습니까?")) {
        document.frm.action = url;
        document.frm.submit();
    }
}

// 목록
function fn_list(url){
    document.frm.action=url;
    document.frm.submit();
}

//답변
function fn_answer(url){
    if(confirm("답변하시겠습니까?")) {
        document.frm.action = url;
        document.frm.submit();
    }
}

// 등록&수정
function fn_regist(){
    if(confirm("저장하시겠습니까?")) {
        var content ="";
        try{
            content = Editor.getContent();
            $('textarea#editorTarget').val(content);
        }catch(ex){
            console.log("[WARNING] 다음에디터 못찾음");
        }
        document.frm.submit();
    }
}

/**
 * 업로드 파일 공유
 * @param fileNm
 * @param uploadPath
 * @param serviceName
 * @returns
 */
function fileUpLink(fileNm, uploadPath, serviceName){
    $.ajax({
        type: 'post' ,
        data: {fileNm: fileNm, path: uploadPath, sNm: serviceName},
        url: "/cmm/fms/fileUploadLinkAjax.do",
        dataType:'json',
        error: function(data, status, err){
            alert('시스템 에러가 발생하였습니다.\n관리자에게 문의하여 주십시요.'); //통신 에러 상태 확인
        },
        success: function(json){
            if(json.RESULT_FILELINK == "OK"){

            }
            else{
                alert(json.message);
                return;
            }
        }
    });
}


function fnGetCookiePopup(name) {
    var results = document.cookie.match ( '(^|;) ?' + name + '=([^;]*)(;|$)' );
    if ( results )
        return ( unescape ( results[2] ) );
    else
        return null;
}


function fnCheckDate(startDate, endDate,unlmitedUseAt){
    var hours = new Date().getHours()
    hours = hours >= 10 ? hours : '0' + hours;
    var today = getFormatDate(new Date())+ hours;
    var sDate = startDate.replace(/-/g,"");
    var eDate = endDate.replace(/-/g,"");


    if(sDate < today && (eDate > today || unlmitedUseAt =='Y')){
        return true;
    }else{
        return false;
    }
}

function getFormatDate(date){
    var year = date.getFullYear();              //yyyy
    var month = (1 + date.getMonth());          //M
    month = month >= 10 ? month : '0' + month;  //month 두자리로 저장
    var day = date.getDate();                   //d
    day = day >= 10 ? day : '0' + day;          //day 두자리로 저장
    return  year + '' + month + '' + day;
}

function fnSetCookiePopup( name, value, expiredays ) {
    var todayDate = new Date();
    todayDate.setDate( todayDate.getDate() + expiredays );
    if(value != null) {
        document.cookie = name + "=" + escape( value ) + "; path=/; expires=" + todayDate.toGMTString() + ";";
    } else {
        document.cookie = name + "=; path=/; expires=" + todayDate.toGMTString() + ";";
    }
}

function fnPopupCheck(popCd,modalId){
    var chk = document.getElementById("chkPopup");
    if(chk && chk.checked) {
        fnSetCookiePopup( popCd, "done" , 365);
    }
    if(modalId){
        $('#'+modalId).remove();
    }else{

    }
}


function fn_egov_popupOpen_PopupManage(popCd,tmplatCd,width,height,top,left,stopViewAt,popType) {
    var url = "/openPopupManage.do?";

    if(popType=='BNR04') { // 새창팝업
        if(tmplatCd) {
            url = url + "tmplatCd=" + tmplatCd;
        }
        url = url + "stopViewAt=" + stopViewAt;
        url = url + "&popCd=" + popCd;
        var name = popCd;

        openWindows = window.open(url,name,"width="+width+",height="+height+",top="+top+",left="+left+",toolbar=no,status=no,location=no,scrollbars=yes,menubar=no,resizable=yes");

//        openWindows.focus();
    }else if(popType=='BNR05'){ // 모달팝업
        url = "/openPopupManage.do?";
        var data = {
            stopViewAt:stopViewAt,
            popCd:popCd
        };
        var successFn = function (html) {
            $('#modalArea').append(html);
            $('#modal-'+popCd).draggable()
        };
        fn_ajax_json(url, data, 'html', successFn);

    }
}
