$(document).ready(function () {
    $(".paid_btn").click(function() {
        var url = $(this).attr('data_url');
        var rowID = $(this).attr('data_rowID'); 
        var address = $(this).attr('data_address');        
        $("#modal_paid_btn").attr('data_url', url);
        $("#modal_paid_btn").attr('data_rowID', rowID);
        $("#modal_paid_btn").attr('data_address', address);
        $("#modal_title").html(address);
        $('#modal_confirm').modal('open');        
    });

    $("#modal_paid_btn").click(function() {
        var rowID = $(this).attr('data_rowID');
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        })
        $.ajax({            
            url: $(this).attr('data_url'), 
            type: "POST",
            success: function(data){  
                if (data.result=="success"){
                    $('#row_'+rowID).slideUp();            
                }
                else {
                    $('#ajax_err_modal_content').html('<h4>There was an error: '+ data.message+'</h4>')
                    $('#ajax_err_modal').modal('open');                      
                }
        },
        error: function (jqXHR, status, err) {
            $('#ajax_err_modal_content').html('<h4>Sorry there was an error when trying to save the job (Error:'+err+')</h4>')
            $('#ajax_err_modal').modal('open');
        },
        complete: function (jqXHR, status) {             
        }
        });
        
            //TODO check if div is empty and replace html
                       
    })
    //Materialize initializations:
    $('.collapsible').collapsible();    
    $(".button-collapse").sideNav();
    $('.modal').modal({dismissible: false});     //user has to click button to fire sliding up of card  

})