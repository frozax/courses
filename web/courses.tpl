<input type="search" id="item-autocomplete" name="item" />

<script>
var elements = [
% for item in items:
  { title: '{{item["name"]}}',
    simplified_name: '{{item["simplified_name"]}}',
    group: '{{item["aisle"]}}'},
% end
];

$(document).ready(function() {

  	// Local source, string array. Simplest setup possible
	$('#item-autocomplete').betterAutocomplete('init', elements, {}, {
		select: function(result, $input) { // Custom select callback
			console.log($input);
		},
		queryLocalResults: function(query, resource, caseSensitive) {
			var results = [];
			query = query.unidecode();
			$.each(resource, function(i, value) {
				if(value.simplified_name.indexOf(query) >= 0) {
					// Match found in title field
					results.push(value);
				}
			});
			return results;
		}
	});
});

</script>
