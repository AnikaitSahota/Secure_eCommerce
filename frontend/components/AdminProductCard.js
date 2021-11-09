import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import api from '../pages/api';

function AdminProductCard(props) {
	const router = useRouter();
	const productName = props.productName;
	const productDescription = props.productDescription.slice(0, 100) + '...';
	const productId = props.productId;

	const [token, setToken] = useState('');
	const [username, setUsername] = useState('');

	useEffect(() => {
		const cookie = document.cookie;
		if (!cookie) {
			router.push(`/`);
		} else {
			var cookies = JSON.parse(cookie.split('=')[1]);
			var tokenTemp = cookies.token;
			var typeTemp = cookies.type;
			var usernameTemp = cookies.username;
			setToken(tokenTemp);
			setUsername(usernameTemp);
			if (typeTemp !== 'admin') {
				router.push('/');
			}
		}
	});

	function clicked() {
		const body = {
			token: token,
			username: username,
			id: productId,
		};
		fetch(`${api}/admin/delete-product/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					const box = document.getElementById(productName);
					box.style.backgroundColor = '#dd2222';

					const buttons = box.getElementsByTagName('button');
					for (let i = 0; i < buttons.length; i++) {
						buttons[i].style.display = 'none';
					}
				} else {
					alert(res.status);
				}
			});
	}

	return (
		<div className='buyerProductCard' id={productName}>
			<h3>{productName}</h3>
			<p className='buyerProductCardBody'>{productDescription}</p>
			<button className='delete' id='delete' onClick={(e) => clicked()}>
				Delete
			</button>
		</div>
	);
}

export default AdminProductCard;
