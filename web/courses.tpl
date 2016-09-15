<table><tr><td>
	<div style="display: inline-block">
		<input type="search" id="item-autocomplete" name="item" />
		<br /><a class="btn" href="courses/print/"><i class="fa fa-print"></i> Imprimer</a>

	</div>
	<div id="user-list">
	</div>
	<div style="clear: both"><br /><br /><a class="btn" href="#" id="clear_list"><i class="fa fa-trash-o"></i> Effacer liste</a>
	</div>
</td><td style="width: 100%">
	<div id="shop-list">
	</div>
</td></tr></table>
<script>

var SHOP_LIST = Array();
var ITEM_NAME_TO_ITEM = {}; // links between name to item

//
// TODO TODO
// Récupérer la liste du magasin une fois pour toute, conserver les données brutes à un format qui nous plait (celle du REST par exemple).
// Puis créer la liste et avec des fonctino set_item_state(id, "user-selected") changer que ce qu'il faut
// -> Entrer des éléments pas dans la liste


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
	post("/api/user_list/update_comment", {product: product, comment: comment});
}

function update_user_list_on_page(user_data)
{
	SHOP_LIST.forEach(function(item) { item.selected = false; });
	
	var l = $("#user-list");
	l.html("<ul class=\"split-list\">\n");
	var ul = l.find(".split-list");
	var i = 0;
	user_data.forEach(function(item) {
		actual_item = ITEM_NAME_TO_ITEM[item[0]];
		actual_item.selected = true;
		var html_id = "userlistitem" + i;
		html_item = "<li class=\"li_user_item\"><div class='div_user_item' id=\"" + html_id + "\">" + item[0] + "</div>";
		html_item += "<div class='div_user_comment'><input id=\"" + html_id + "input\" type=\"text\" value=\"" + item[1] + "\"></div>";
		html_item += "</li>\n";
		ul.append(html_item);
		$("#" + html_id).click({actual_item_param: actual_item}, function(event) { 
			remove_item(event.data.actual_item_param.item.name);
		});
		$("#" + html_id + "input").change({actual_item_param: actual_item}, function(event) {
			update_product_comment(event.data.actual_item_param.item.name, event.currentTarget.value);
		});
		i++;
	});
	update_shop_list_selections();	
	layout_list(ul, 70);
}
	
function _toggle_item(item)
{
	item.selected = !item.selected;
	if (item.selected) {
		add_item(item.item.name);
	}
	else {
		remove_item(item.item.name);
	}
	update_shop_list_selections();
}

// set up the shop list on the page
function init_shop_list_on_page(data)
{
	var l = $("#shop-list");
	l.html("<ul class=\"split-list\">\n");
	var ul = l.find(".split-list");
	var i = 0;
	data.forEach(function(src_item) {
		if (src_item.type == "spacer")
			return;

		var li_class = "";
		var item_name = "shoplistitem" + i;
		if (src_item.type == "aisle")
		{
			li_class = "li_aisle";
		}
		else if (src_item.type == "product")
		{
			li_class = "li_product";
		}
		var html_item = "<li id='" + item_name + "' class='" + li_class + "'>";
		html_item += src_item.name;
		html_item += "</li>\n";
		ul.append(html_item);
		if (li_class == "li_product") {
			var html_obj = $("#" + item_name);
			item_shop_list = {item: src_item, html_obj: html_obj, selected:false}
			SHOP_LIST.push(item_shop_list);
			ITEM_NAME_TO_ITEM[src_item.name] = item_shop_list;
			html_obj.click({item: item_shop_list}, function(event) { 
				_toggle_item(event.data.item);
			});
		}
		i++;
	});
	layout_list(ul, 56);
}

function update_shop_list_selections()
{
	SHOP_LIST.forEach(function(item) {
		li_class = "li_product_selected";
		if(item.selected)
			item.html_obj.addClass(li_class);
		else
			item.html_obj.removeClass(li_class);
	});
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
	post("/api/user_list/remove_item", {item: item}, function(){
		// success, refresh user list
		refresh_user_list();
	});
}

function add_item(item)
{
	post("/api/user_list/add_item", {item: item}, function() {
		refresh_user_list();
	});
}

function refresh_user_list()
{
	$.get("/api/user_list", update_user_list_on_page);
}

$(document).ready(function() {

	$.get("/api/shop_list", function(data) {
		init_shop_list_on_page(data);
		refresh_user_list();

		// create autocomplete data
		var elements = Array();
		SHOP_LIST.forEach(function (item) {
			elements.push({"title": item.item.name, "group": item.item.aisle, "simplified_name": item.item.simplified_name});
		});

		var new_item = true;
		// Local source, string array. Simplest setup possible
		$('#item-autocomplete').betterAutocomplete('init', elements, {}, {
			select: function(result, $input) { // Custom select callback
				new_item = false;
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
		}).keydown(function (e) {
			if(e.keyCode == 13)  // the enter key code
			{
				if (new_item)
				{
			/*if not self.model.exists(item):
				if self.view.msg_box_yesno(u"Ajouter %s à la liste?" % item):
					self.model.add_item_to_shop_list_temporarily(item)
				else:
					return None
			self.model.add_item(item)*/
					// 
				}
			}
			new_item = true; // not known until selected
		});   
	});

	$("#clear_list").click(function()
	{
		$.get("/api/clear_list", function() {
			refresh_user_list();
		});
	});
});

</script>
