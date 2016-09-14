<input type="search" id="item-autocomplete" name="item" />
<table><tr><td>
	<div id="user-list">
	</div>
</td><td>
	<div id="shop-list">
	</div>
</td></tr></table>
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

function update_user_list_on_page(user_data)
{
	var l = $("#user-list");
	l.html("<ul class=\"split-list\">\n");
	var ul = l.find(".split-list");
	var i = 0;
	user_data.forEach(function(item) {
		var item_name = "userlistitem" + i;
		html_item = "<li><div id=\"" + item_name + "\">" + item[0] + "</div>";
		html_item += "<input type=\"text\" value=\"" + item[1] + "\">";
		html_item += "</li>\n";
		ul.append(html_item);
		$("#" + item_name).click({item_name: item[0]}, function(data) { 
			remove_item(data.data.item_name);
		});
		i++;
	});
	layout_list(ul, 50);
}

function update_shop_list_on_page(shop_data)
{
	var l = $("#shop-list");
	l.html("<ul class=\"split-list\">\n");
	var ul = l.find(".split-list");
	var i = 0;
	shop_data.forEach(function(item) {
		var item_name = "shoplistitem" + i;
		var html_item = "<li><div id='" + item_name + "'>";
		if (item[1] == "aisle-name")
			html_item += "<b>" + item[0] + "</b>";
		else if (item[1] == "spacer")
			html_item += "&nbsp;";
		else if (item[1] == "product")
			html_item += item[0]
		else if(item[1] == "selected-product")
			html_item += "<font color='#f00'>" + item[0] + "</font>"
		html_item += "</div></li>\n";
		ul.append(html_item);
		if (item[1] == "product" || item[1] == "selected-product") {
			$("#" + item_name).click({item_name: item[0], selected: item[1] == "selected-product"}, function(data) { 
				if (data.data.selected)
					remove_item(data.data.item_name);
				else
					add_item(data.data.item_name);
			});
		}
		i++;
	});
	layout_list(ul, 20);
}

function post(url, dict, success)
{
	$.ajax({url: url,
		    data: JSON.stringify(dict),
            type: "POST",
		    contentType: "application/json",
            success: success});
}

function remove_item(item)
{
	post("/api/user_list/remove_item", {item: item}, refresh_both_lists);
}

function add_item(item)
{
	post("/api/user_list/add_item", {item: item}, refresh_both_lists);
}

function refresh_both_lists()
{
	refresh_user_list();
	refresh_shop_list();
}

function refresh_user_list()
{
	$.get("/api/user_list", update_user_list_on_page);
}

function refresh_shop_list()
{
	$.get("/api/shop_list", update_shop_list_on_page);
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
	refresh_shop_list();

  	// Local source, string array. Simplest setup possible
	$('#item-autocomplete').betterAutocomplete('init', elements, {}, {
		select: function(result, $input) { // Custom select callback
			add_item(result.title);
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
