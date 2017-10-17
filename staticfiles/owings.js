$( document ).ready(function() {       
    (function ($) {
        jQuery.expr[':'].Contains = function(a,i,m){
            return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
        };
       
        function listFilter(header, list) {
          var input = $("#input_search")
          $(input)
            .change( function () {
              var filter = $(this).val();
              if(filter) {
                $(list).find(".address:not(:Contains(" + filter + "))").parent().hide();
                $(list).find(".address:Contains(" + filter + ")").parent().show();
              } else {
                $(list).find("tr").show();
              }
              return false;
            })
          .keyup( function () {
              $(this).change();
          });
        }
      
        $(function () {
          listFilter($("#header"), $("#invoice_list"));
        });
      }(jQuery));
    });