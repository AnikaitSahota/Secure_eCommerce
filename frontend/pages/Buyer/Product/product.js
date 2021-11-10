import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../../components/BuyerNavbar';
import BuyerProductCard from '../../../components/BuyerProductCard';
import api from '../../api';

function Product() {
	const router = useRouter();
	const [products, setProducts] = useState([]);
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
					if (typeTemp !== 'buyer') {
						router.push('/');
					}

					fetch(`${api}/product/all-products/`)
						.then((res) => res.json())
						.then((res) => {
							if (res.status == 'success') {
								setProducts(res.data);
							} else {
								alert(res.status);
							}
						});
				}
			}
		}
	}, []);

	return (
		<div>
			<BuyerNavbar />
			<div className='content'>
				{products.map((e, i) => {
					return (
						<BuyerProductCard
							key={i}
							productName={e.name}
							productDescription={e.description}
							productId={e.id}
							productImg1={e.img1}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default Product;
