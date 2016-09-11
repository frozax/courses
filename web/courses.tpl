<input type="search" id="item-autocomplete" name="item" />

<script>
var elements = [
% for item in items:
  { title: '{{item["name"]}}', group: '{{item["aisle"]}}' },
% end
  {title: 'Stockholm', group: "toto"},
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

  	// Local source, string array. Simplest setup possible
	$('#item-autocomplete').betterAutocomplete('init', elements, {}, {});
});

</script>
