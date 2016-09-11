<input type="search" id="item-autocomplete" name="item" />

<script>
var cities = [
  'Stockholm',
  'New York',
  'Oslo',
  'San Fransisco',
  'Säffle',
  'Göteborg',
  'Mogadishu',
  'Washington',
  'Madrid',
  'Paris',
  'Arboga',
  'Moscow'
];

$(document).ready(function() {

	console.log("toto");
  	// Local source, string array. Simplest setup possible
	$('#item-autocomplete').betterAutocomplete('init', cities, {}, {});
});

</script>
