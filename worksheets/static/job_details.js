 //ajax to complete jobs:     
 $(document).ready(function () {
    $(".job_details_btn").click(function() {
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
            type: "GET",
            // data: {                
            //     jobid  
            // },
            success: function(result){    
                $('#modal_message').html(result);
                $('#job_details_modal').modal('open');        
        }
        ,
        error: function (jqXHR, status, err) {
            $('#job_details_modal').html("<h4>Sorry, there has been an error" + err + "</h4>");
            $('#job_details_modal').modal('open');        
      
        },
        complete: function (jqXHR, status) {             
        }
        });            
    });  

    
});

//Materialize initializations:
$('.collapsible').collapsible();    
$(".button-collapse").sideNav();
$('.modal').modal();