import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import api from '../pages/api';

function AdminCategoryCard(props) {
	const router = useRouter();
	const productName = props.productName;
	const [token, setToken] = useState('');
	const [username, setUsername] = useState('');

	useEffect(() => {
		const cookie = document.cookie;
		if (!cookie) {
			router.push(`/`);
		} else {
			const allCookies = cookie.split(';');
			for (let i = 0; i < allCookies.length; i++) {
				var [cookieName, cookieValue] = allCookies[i].split('=');
				if (cookieName == 'info') {
					var cookies = JSON.parse(cookieValue);
					var tokenTemp = cookies.token;
					var typeTemp = cookies.type;
					var usernameTemp = cookies.username;
					setToken(tokenTemp);
					setUsername(usernameTemp);
					if (typeTemp !== 'admin') {
						router.push('/');
					}
				}
			}
		}
	}, []);

	function clicked() {
		const body = {
			token: token,
			username: username,
			category_name: productName,
		};
		fetch(`${api}/admin/delete-category/`, {
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
			<button className='delete' id='delete' onClick={(e) => clicked()}>
				Delete
			</button>
		</div>
	);
}

export default AdminCategoryCard;
