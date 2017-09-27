 //ajax to complete jobs:     
 $(document).ready(function () {

    $(".compl_btn").click(function() {
        //grab IDs from card & parent:--------------------------------------------
        var jobid = $(this).attr('data_job');// id of the job to be checked in
        var date = $(this).attr('data_date');//grouping date
        var card_id = "card_"+ jobid  //id of the card displaying the job, used to dismiss later
        var compl_address = $(this).attr('data_address'); //customer address
        var payment_status = $(this).attr('data_payment'); //'paid' or 'owed'
        var headerid = "header_" + date //accordion section header id
        var num_jobs = $('#num_jobs_'+ date);   //span containing number of jobs in section
        var total = $('#total_'+ date); //span containing total ££ in section
        //--------------------------------------------------------------------------        
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
        $.ajax({            
            url: $(this).attr('data_url'), 
            type: "POST",
            data: {                
                payment_status,
                jobid  
            },
            success: function(result){    
                $('#modal_address').html('<h5>'+ compl_address +'</h5>');
                if(payment_status=='paid'){
                    $('#modal_message').html('<p>Job has been checked in as Completed/Paid</p>');
                }
                else {               //owed        
                    $('#modal_message').html('<p>Job has been checked in as Completed/Owed</p>');
                }
                $('#modal_btn').attr('data_jobid', jobid);
                $('#modal_btn').attr('data_date', date);
                $('#confirmation_modal').removeClass('red');
                $('#confirmation_modal').modal('open');                   
        }
        ,
        error: function (jqXHR, status, err) {
            alert("problem")
            $('#modal_address').html('<h4>'+ compl_address +'</h4>');
            $('#confirmation_modal').addClass('red');
            $('#modal_message').html('<p>There was an error when trying to check in this job. Status: ' + status + '</p>');
            $('#confirmation_modal').modal('open');  
          
        },
        complete: function (jqXHR, status) {             
        }
        });            
    });  


    $("#modal_btn").click(function() {
        var jobid = $(this).attr('data_jobid');
        var date = $(this).attr('data_date');        
        var num_jobs = parseInt($('#num_jobs_'+date).text());
        var x = $('#total_'+date).text();
        var total = parseFloat($('#total_'+date).text());
        var amount = parseFloat($('#price_'+jobid).text()); 
        total -= amount;
        num_jobs -= 1
        if (num_jobs==1){
            $('#num_jobs_suffix_'+date).text(' job');
        }
        else {
            $('#num_jobs_suffix_'+date).text(' jobs');
        }
        $('#num_jobs_'+date).text(num_jobs); 
        $('#total_'+date).text(total);
        if (num_jobs==0){
            $('#collapsible_body_'+date).html('<h5 style="font-style:italic">All jobs have been checked in</h5>');
            $('#badge_'+date).removeClass("green").addClass("blue");
            $('#header_'+date).removeClass("darken-2").addClass("darken-4");
        } 
        $('#card_'+jobid ).slideUp();
        //TODO check if div is empty and replace html
    });   

    //job details modal:---------------
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
        $.ajax({
            url: $(this).attr('data_url'), 
            type: "GET",            
            success: function(result){    
                $('#job_details_message').html(result);
                $('#job_details_modal').modal('open');        
        }
        ,
        error: function (jqXHR, status, err) {
            $('#job_details_message').html("<h4>Sorry, there has been an error" + err + "</h4>");
            $('#job_details_modal').modal('open');        
      
        },
        complete: function (jqXHR, status) {             
        }
        });            
    });  
    //Materialize initializations:
    $('.collapsible').collapsible();    
    $(".button-collapse").sideNav();
    $('.modal').modal({dismissible: false});     //user has to click button to fire sliding up of card  
});

