/**
 * Created by ajava on 17. 4. 19.
 */

function getCookie(name, document, jQuery) {
    "use strict";
    var cookievalue = null, cookies = null;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookievalue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookievalue;
}

function csrfSafeMethod(method) {
    "use strict";
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function humanFileSize(bytes, si=false, dp=1) {
    try{
        const thresh = si ? 1000 : 1024;

        if (Math.abs(bytes) < thresh) {
        return bytes + ' B';
        }

        const units = si
        ? ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
        let u = -1;
        const r = 10**dp;

        do {
        bytes /= thresh;
        ++u;
        } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);


        return bytes.toFixed(dp) + ' ' + units[u];
    }
    catch (e) {
        return '-';
    }
}


function singleCSVUploader( app_name, form_id, options ) {
  let extension = 'csv'
  let max_file_size = '700MB'
  let mime_type_title = 'CSV files'

  let uploader = new plupload.Uploader({
    runtimes: 'html5,html4',
    browse_button: options.browse_button_id,
    container: document.getElementById(form_id),
    // url: options.s3_url, // dynamically set-up
    file_data_name: "file",
    multi_selection: false,
    multipart: true,
    multipart_params: {},
    filters: {
      max_file_size: max_file_size,
      mime_types: [{title: mime_type_title, extensions: extension}]
    },
    flash_swf_url: "/static/vendors/plupload/Moxie.swf",
    silverlight_xap_url: "/static/vendors/plupload/Moxie.xap"
  });

  function enableSubmitButton(enable) {
    $('#'+form_id).find('button:submit').attr('disabled', enable);
  }
  function showAddButton(enable) {
    if (enable) {
      $('#'+options.browse_button_id).show();
      setHiddenId('');
    } else {
      $('#'+options.browse_button_id).hide();
    }
  }
  function setHiddenId(value){
      $('#' + options.hidden_id ).val(value);
  }

  function updateS3settings(uploader, file){
    $.ajax({
      type: "POST",
      url: options.before_upload,
      data: {
        id: file.id,
        name: file.name,
        type: file.type,
        size: file.size,
        dest: app_name
      },

      success: function (data) {
        file.name = data.filename;
        uploader.settings.url = data.aws_payload['form_action'];
        delete data.aws_payload['form_action'];

        uploader.settings.multipart_params = {}
        Object.keys(data.aws_payload).forEach(function (key) {
          uploader.settings.multipart_params[key] = data.aws_payload[key];
        });

        setTimeout(function () {
          uploader.start();
        }, 1);
      },
      error:function(request,status,error) {
        uploader.trigger(
            "Error",
            {
              code: plupload.Uploader.SECURITY_ERROR,
              message: error,
              file: file
            }
        );
      }
    });
  }

  uploader.bind('StateChanged', function(uploader) {
    let remainCount = $('.btn-upload:not([style*="display: none"])').length ;
    // $('#'+form_id).find('button:submit').attr('disabled', remainCount !== 0);
  });

  uploader.bind('FilesAdded', function (uploader, files) {
    if ( files.length > 1 ) return ;
    enableSubmitButton(false);
    showAddButton(false);
    let file = files[0];

    updateS3settings(uploader, file);
    let containerDiv = $('<div>', {'id': file.id,'class': 'd-flex justify-content-between align-items-center px-3'}),
        progressWrapper = $("<div />", {"id": file.id + '-progressWrap', "class": "progress  w-100", 'style': 'height:25px;'}),
        progressDiv = $("<div />", {"id": file.id + '-bar', "class": "progress-bar progress-bar-striped progress-bar-animated", "role": "progressbar", "aria-valuenow": "0", "aria-valuemin": "0", "aria-valuemax": "100", "style": 'width: 0%'}),
        removeButton = $('<button />', {
            'class': 'btn btn-outline-danger removeBtn btn-sm mx-3',
            'type': 'button',
            'data-target': file.id,
            'id': file.id + '-removeBtn'
        }),
        svg=$('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-trash" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path></svg>');

    svg.append('삭제');
    removeButton.append(svg);

    progressWrapper.append(progressDiv);
    containerDiv.append(progressWrapper);
    containerDiv.append(removeButton);

    $('#' + options.browse_button_id).after(containerDiv);
    $(containerDiv).on("click", ".removeBtn", function(){
       $(this).parent().remove();
       showAddButton(true);
       uploader.removeFile(file);
       uploader.trigger('StateChanged');
       setHiddenId('');
    });
  });

  uploader.bind('UploadProgress', function(uploader, file) {
    $('#'+file.id+'-bar').css('width', file.percent+'%').attr('aria-valuenow', file.percent);
  });

  uploader.bind('FileUploaded', function(uploader, file, response) {
    // <i class="bi bi-trash"></i>
      console.log(response);

    let responseData = $.parseXML(response.response),
        resp = $(responseData).find('PostResponse'),
        callbackData = {
            bucket: resp.find('Bucket').text(),
            key: resp.find('Key').text(),
            filename: file.name,
            filesize: file.size,
            app_name: app_name,
            content_type: file.type,
            browse_button_id: options.browse_button_id,
            file_type: options.file_type,
        };

    $.ajax({
        type: "POST",
        url: options.after_upload,
        data: callbackData,

        success: function (data) {
            $('#' + file.id + '-progressWrap').remove();
            let removeBtn = $('#' + file.id + '-removeBtn');
            removeBtn.before(
                $('<span>' + data.filename + '</span><span>(' + data.filesize + ')</span>')
            );
           setHiddenId(data.id);
        },
        error:function(request,status,error) {
            uploader.trigger(
                "Error",
                {
                    code: plupload.Uploader.SECURITY_ERROR,
                    message: error,
                    file: file
                }
            )
        }
    });
  });

  uploader.bind('Error', function (up, error) {
    alert("오류 : " + error.message);
    $('#' + error.file.id).remove();
    up.removeFile( error.file );
    showAddButton(true);
  });

  uploader.init();
  uploader.trigger('StateChanged');
  uploader.refresh();

  return uploader;
}
