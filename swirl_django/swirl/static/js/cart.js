let updateBtns = document.getElementsByClassName('update_cart');

for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		let productId = this.dataset.product;
		let action = this.dataset.action;
		console.log('productId', productId, 'action', action);
		console.log('User', user);
		if (user === 'AnonymousUser') {
			console.log('not logged in');
		} else {
			updateUserOrder(productId, action);
		}
	});
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
		});
}
