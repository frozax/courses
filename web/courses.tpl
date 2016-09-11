<input type="search" id="item-autocomplete" name="item" />

<script>
var elements = [
% for item in items:
  { title: '{{item["name"]}}', group: '{{item["aisle"]}}' },
% end
];

$(document).ready(function() {

  	// Local source, string array. Simplest setup possible
	$('#item-autocomplete').betterAutocomplete('init', elements, {}, {});
});

</script>
