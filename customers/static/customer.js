       
       //Return address from Google place API:
        //This is nice and free but will not return 
        //address_line_1/2/3 or County 
        //so not really suitable for production
        //but the autocomplete is easy to implement.
        
        var placeSearch, autocomplete;
        var componentForm = {
            street_number: 'short_name',
            route: 'long_name',
            postal_town: 'long_name',
            postal_code: 'short_name'
        };
        
        function initAutocomplete() {
            // Create the autocomplete object, restricting the search to geographical
            // location types.
            autocomplete = new google.maps.places.Autocomplete(
                /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
                {types: ['geocode']});
        
            // When the user selects an address from the dropdown, populate the address
            // fields in the form.
            autocomplete.addListener('place_changed', fillInAddress);
        }
        
        function fillInAddress() {
            // Get the place details from the autocomplete object.
            var place = autocomplete.getPlace();
                    
            for (var component in componentForm) {
            document.getElementById(component).value = '';
            //should be unnecessary
            }
        
            // Get each component of the address from the place details
            // and fill the corresponding field on the form.
            for (var i = 0; i < place.address_components.length; i++) {
            var addressType = place.address_components[i].types[0];
            if (componentForm[addressType]) {
                var val = place.address_components[i][componentForm[addressType]];
                document.getElementById(addressType).value = val;
            }
            };
            //Django form is generated by template generator
            //so we have to populate form from results of Google autocomplete
            //after if has been generated. Because template engine does not look into ext. JS files, IDs have to be hard-coded
            //Otherwise can use e.g. {{ form.customer_notes.id_for_label }}
            document.getElementById('id_postcode').value=document.getElementById('postal_code').value;
            document.getElementById('id_address_line_1').value=
                    document.getElementById('street_number').value+' '+document.getElementById('route').value;
            document.getElementById('id_city').value=document.getElementById('postal_town').value;
            document.getElementById('id_url').value=place.url;
            document.getElementById('id_longitude').value=Math.round(place.geometry.location.lng()*100000)/100000;            
            document.getElementById('id_latitude').value=Math.round(place.geometry.location.lat()*100000)/100000;            
        }
        
        // Bias the autocomplete object to the user's geographical location,
        // as supplied by the browser's 'navigator.geolocation' object.
        function geolocate() {
            if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var geolocation = {
                //use position.coords. to biase towards current browser location
                lat: 51.528, //position.coords.latitude,
                lng: -0.381 //position.coords.longitude
                };
                var circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy
                });
                autocomplete.setBounds(circle.getBounds());
            });
              }
            }
            