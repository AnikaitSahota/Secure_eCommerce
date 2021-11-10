import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../components/BuyerNavbar';
import api from '../api';
import BuyerOrder from '../../components/BuyerOrders';

function Orders() {
	const router = useRouter();
	const [orders, setOrders] = useState([]);
	const [token, setToken] = useState('');
	const [type, setType] = useState('');
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
					setType(typeTemp);
					setUsername(usernameTemp);
					if (typeTemp !== 'buyer') {
						router.push('/');
					}
				}
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
		fetch(`${api}/customer/order-history/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					setOrders(res.data);
				} else {
					alert(res.status);
				}
			});
	}, []);

	return (
		<div>
			<BuyerNavbar />
			<div className='content'>
				{orders.map((e, i) => {
					return (
						<BuyerOrder
							key={i}
							orderName={e.product_name}
							orderQuantity={e.quantity}
							orderAmount={e.total_amount}
							orderTime={e.time_of_creation}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default Orders;
