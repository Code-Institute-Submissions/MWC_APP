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
            success: function(result){  
                $('#row_'+rowID).slideUp();

                                            
        },
        error: function (jqXHR, status, err) {            
            $('#modal_confirm').html('<h4>'+ $(this).attr('data_address') +'</h4>');
            $('#confirmation_modal').addClass('red');
            $('#modal_message').html('<p>There was an error when trying to check in this job. Status: ' + status + '</p>' +
            '<a href="#!" class="btn waves-effect waves-light right modal-action modal-close">OK</a>');
          
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