<input type="search" id="item-autocomplete" name="item" />
<div id="user-list">
TODO
</div>

<script>

// https://codepen.io/anon/pen/LRGQAv

function layout_list(container, max_items_per_col) {
    listItem = 'li',
    listClass = 'sub-list';
    container.each(function() {
        var items = $(this).find(listItem);
        var id_item = 0;
		while (id_item < items.length)
		{
			$(this).append($('<ul></ul>').addClass(listClass));
			for (var j = 0; j < max_items_per_col; j++) {
				$(this).find('.' + listClass).last().append(items[id_item]);
				id_item++;
				if (id_item >= items.length)
					break;
			}
		}
    });
}

function refresh_user_list() {
	$.get( "/api/user_list", function(data) {
		html = "<ul class=\"split-list\">\n";
		data.forEach(function(item) {
			html += "<li>" + item[0];
			html += "<input type=\"text\" value=\"" + item[1] + "\">";
			html += "</li>\n";
		});
		html += "</ul>\n";
		$("#user-list").html(html);
		var elem = $("#user-list .split-list");
		layout_list(elem, 20);
	});
}

var elements = [
% for item in items:
  { title: '{{item["name"]}}',
    simplified_name: '{{item["simplified_name"]}}',
    group: '{{item["aisle"]}}'},
% end
];

$(document).ready(function() {

	refresh_user_list();

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
