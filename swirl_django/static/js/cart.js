let updateBtns = document.getElementsByClassName('update_cart');
let addFavoriteButton = document.getElementsByClassName('update_favorite');


for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let action = this.dataset.action;
		console.log('productId', productId, 'action', action);
		console.log('User', user);
		if (user == 'AnonymousUser') {
			addCookieItem(productId, action);
		} else {
			updateUserOrder(productId, action);
		}
	});
}
for (let i = 0; i < addFavoriteButton.length; i++) {
	addFavoriteButton[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let action = this.dataset.action;
		console.log('productId', productId, 'action', action);
		console.log('User', user);
		addFavoriteItem(productId, action);	
	});
}

	

	

function addCookieItem(productId, action) {
	if (action == 'add') {
		if (cart[productId] == undefined) {
			cart[productId] = { 'quantity': 1 };
		} else {
			cart[productId]['quantity'] += 1;
		}
	}
	if (action == 'remove') {
		cart[productId]['quantity'] -= 1;
		if (cart[productId]['quantity'] <= 0) {
			console.log('removed item');
			delete cart[productId];
		}
	}
	console.log('Cart', cart);
	document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
	location.reload()
}
function addFavoriteItem(productId,action) {
	if(action =='add') {
		if(favorite[productId]== undefined) {
			favorite[productId] = {'quantity':1}
		}else if ( favorite[productId]==1) {
			return
		}
	}
	if (action == 'remove') {
		favorite[productId]['quantity'] -= 1;
		if (favorite[productId]['quantity'] <= 0) {
			console.log('removed item');
			delete favorite[productId];
		}
	}
	document.cookie = 'favorite=' + JSON.stringify(favorite) + ';domain=;path=/';
	location.reload();
}

function updateUserOrder(productId, action) {
	console.log('user is logged in,sending data');
	let url = '/update_item/';
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			productId: productId,
			action: action,
		}),
	})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('data', data);
			location.reload();
		});
}

