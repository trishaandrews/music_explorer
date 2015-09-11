$(document).ready(function() {
  var selected_labels = [];
  NoResults = "No Results"; //TODO No Results message for empty autocomplete
  $('#autocomplete').autocomplete({
    source: function (request, response) {
        $.getJSON('../autocomplete',{ //'{{ url_for("autocomplete") }}',{
            search: request
            }, response);
        },
    minLength: 1,                      
  });
  $("#autocomplete").on("autocompleteselect", function(event, ui) {
    selected_labels.push(ui.item.value);
    console.log(ui.item.cluster)
    $.ajax({
        url: '../add_entry', //'{{ url_for("add_entry") }}',
        data: ui.item,
        type: 'POST',
        success: function (data) {
            json_data = JSON.parse(data);
            //console.log(JSON.parse(data));
            recs = "Recommendations:<br> <ul>";
            recs = box_content(json_data, recs);
            $('#reccontent').html(recs);
        }
    });
    var output = "Chosen songs:<br> <ul>"
    output = box_content(selected_labels, output);
    $('#outputcontent').html(output);
    $(this).val(''); return false; 
  });
  function box_content(data_list, words){
        for(var i=0; i<data_list.length; i++){
            display_words = "";
            if(data_list[i].value){
                display_words = data_list[i].value;
            }else{
                display_words = data_list[i];
            }
            labels = display_words.replace(",", "");
            labels = labels.replace(/\W/g, ' ');
            labels = labels.replace(/ /g, "%20");
            words += '<li><a target="_blank" href="https://www.youtube.com/results?search_query=' + labels +'">'+display_words+'</a></li>';
            }
            words += "</ul>";
        return words;
    }
   $('#refresh').on('click', function (event, ui) {
        $.ajax({
            url: '../refresh_recs', //'{{ url_for("refresh_recs") }}',
            success: function (data) {
                json_data = JSON.parse(data);
                recs = "Recommendations:<br> <ul>";
                recs = box_content(json_data, recs);
                $('#reccontent').html(recs);
            }
        });
   });
});
