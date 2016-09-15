<table><tr><td>
	<input type="search" id="item-autocomplete" name="item" />
	<div id="user-list">
	</div>
</td><td style="width: 100%">
	<div id="shop-list">
	</div>
</td></tr></table>
<script>

//
// TODO TODO
// Récupérer la liste du magasin une fois pour toute, conserver les données brutes à un format qui nous plait (celle du REST par exemple).
// Puis créer la liste et avec des fonctino set_item_state(id, "user-selected") changer que ce qu'il faut


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


function update_product_comment(product, comment)
{
	post("/api/user_list/update_comment", {product: product, comment: comment}, refresh_both_lists);
}

function update_user_list_on_page(user_data)
{
	var l = $("#user-list");
	l.html("<ul class=\"split-list\">\n");
	var ul = l.find(".split-list");
	var i = 0;
	user_data.forEach(function(item) {
		var item_name = "userlistitem" + i;
		html_item = "<li class=\"li_user_item\"><div class='div_user_item' id=\"" + item_name + "\">" + item[0] + "</div>";
		html_item += "<div class='div_user_comment'><input id=\"" + item_name + "input\" type=\"text\" value=\"" + item[1] + "\"></div>";
		html_item += "</li>\n";
		ul.append(html_item);
		$("#" + item_name).click({item_name: item[0]}, function(data) { 
			remove_item(data.data.item_name, null);
		});
		$("#" + item_name + "input").change({item_name: item[0]}, function(event) {
			update_product_comment(event.data.item_name, event.currentTarget.value);
		});
		i++;
	});
	layout_list(ul, 70);
}

function update_shop_list_on_page(shop_data)
{
	var l = $("#shop-list");
	l.html("<ul class=\"split-list\">\n");
	var ul = l.find(".split-list");
	var i = 0;
	shop_data.forEach(function(item) {
		var item_name = "shoplistitem" + i;
		var li_class = "";
		var inner_code = "";
		if (item[1] == "aisle-name")
		{
			li_class = "li_aisle";
		}
		else if (item[1] == "spacer")
		{
			return;
			//li_class = "li_spacer";
		}
		else if (item[1] == "product")
		{
			li_class = "li_product";
		}
		else if(item[1] == "selected-product")
		{
			li_class = "li_product_selected";
		}
		var html_item = "<li class=\"" + li_class + "\"><div id='" + item_name + "'>";
		html_item += item[0];
		html_item += "</div></li>\n";
		ul.append(html_item);
		if (item[1] == "product" || item[1] == "selected-product") {
			$("#" + item_name).click({item_name: item[0]}, function(data) { 
				var selected = data.currentTarget.parentNode.className == "li_product_selected";
				console.log(selected);
				if (selected)
					remove_item(data.data.item_name, data.currentTarget);
				else
					add_item(data.data.item_name, data.currentTarget);
			});
		}
		i++;
	});
	layout_list(ul, 56);
}

function post(url, dict, success)
{
	$.ajax({url: url,
		    data: JSON.stringify(dict),
            type: "POST",
		    contentType: "application/json",
            success: success});
}

function remove_item(item, target)
{
	post("/api/user_list/remove_item", {item: item}, function(){
		// success, refresh user list and select our list
		refresh_user_list();
		if (target)
			target.parentNode.className = "li_product";
		else
			refresh_shop_list();
	});
}

function add_item(item, target)
{
	post("/api/user_list/add_item", {item: item}, function() {
		refresh_user_list();
		if (target)
			target.parentNode.className = "li_product_selected";
		else
			refresh_shop_list();
	});
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
			add_item(result.title, null);
			$input[0].value = "";
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
