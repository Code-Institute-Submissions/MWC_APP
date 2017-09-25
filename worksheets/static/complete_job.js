 //ajax to complete jobs:     
 $(document).ready(function () {

    $(".compl_btn").click(function() {
        var parent_id = 'card_' + $(this).attr('id'); //id of the card displaying the job, used to dismiss later
        var compl_address = $(this).attr('data_address'); //customer address
        var payment_status = $(this).attr('data_payment'); //paid or owed
        var jobid = $(this).attr('id');// id of the job to be checked in
        //for returning the csrf token (Django doesn't render external js files):--------------
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
        });
        //if JQuery script is run on the page then can pass the token via renderer: {{ CSRF_token}}
        //-----------------------------------------------------------------------------------------
        $.ajax({
            url: $(this).attr('data_url'), 
            type: "POST",
            data: {                
                payment_status,
                jobid  
            },
            success: function(result){    
                $('#modal_address').html('<h5>'+ compl_address +'</h5>');
                if(payment_status='paid'){
                    $('#modal_message').html('<p>Job has been checked in as Completed/Paid</p>');
                }
                else {               //owed        
                    $('#modal_message').html('<p>Job has been checked in as Completed/Owed</p>');
                }
                $('#modal_btn').attr('data_parentid', parent_id);
                $('#confirmation_modal').removeClass('red');
                $('#confirmation_modal').modal('open');                   
        }
        ,
        error: function (jqXHR, status, err) {
            $('#modal_address').html('<h4>'+ compl_address +'</h4>');
            $('#confirmation_modal').addClass('red');
            $('#modal_message').html('<p>There was an error when trying to check in this job. Status: ' + status + '</p>');
          
        },
        complete: function (jqXHR, status) {             
        }
        });            
    });  


    $("#modal_btn").click(function() {
        var div_id = $(this).attr('data_parentid')
        alert(div_id);
        $('#'+div_id ).slideUp();
        //TODO check if div is empty and replace html
    });   

    // //job details modal:---------------
    // $(".job_details_btn").click(function() {
    //     //for returning the csrf token (Django doesn't render external js files):--------------
    //     alert('ok!')
    //     function getCookie(name) {
    //         var cookieValue = null;
    //         if (document.cookie && document.cookie !== '') {
    //             var cookies = document.cookie.split(';');
    //             for (var i = 0; i < cookies.length; i++) {
    //                 var cookie = jQuery.trim(cookies[i]);
    //                 // Does this cookie string begin with the name we want?
    //                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
    //                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //                     break;
    //                 }
    //             }
    //         }
    //         return cookieValue;
    //     }
        
    //     var csrftoken = getCookie('csrftoken');

    //     function csrfSafeMethod(method) {
    //         // these HTTP methods do not require CSRF protection
    //         return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    //     }
    //     $.ajaxSetup({
    //         beforeSend: function(xhr, settings) {
    //             if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    //                 xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //             }
    //         }
    //     });
    //     //if JQuery script is run on the page then can pass the token via renderer: {{ CSRF_token}}
    //     //-----------------------------------------------------------------------------------------
    //     $.ajax({
    //         url: $(this).attr('data_url'), 
    //         type: "GET",
    //         // data: {                
    //         //     csrftoken  
    //         // },
    //         success: function(result){    
    //             $('#modal_message').html(result);
    //             $('#job_details_modal').modal('open');        
    //     }
    //     ,
    //     error: function (jqXHR, status, err) {
    //         $('#job_details_modal').html("<h4>Sorry, there has been an error" + err + "</h4>");
    //         $('#job_details_modal').modal('open');        
      
    //     },
    //     complete: function (jqXHR, status) {             
    //     }
    //     });            
    // });  
    //Materialize initializations:
    $('.collapsible').collapsible();    
    $(".button-collapse").sideNav();
    $('.modal').modal();       
});

