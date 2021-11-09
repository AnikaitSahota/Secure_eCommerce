import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../../../components/BuyerNavbar';
import BuyerProductCard from '../../../../components/BuyerProductCard';
import api from '../../../api';

function SearchProduct() {
	const router = useRouter();
	const { search_query } = router.query;
	const [products, setProducts] = useState([]);
	const [isFirstRender, setFirstRender] = useState(true);
	const [token, setToken] = useState('');
	const [username, setUsername] = useState('');

	useEffect(() => {
		if (isFirstRender && search_query) {
			setFirstRender(false);

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
				if (typeTemp !== 'buyer') {
					router.push('/');
				}
				const body = {
					token: tokenTemp,
					username: usernameTemp,
					search_query: search_query,
				};
				fetch(`${api}/customer/search-products/`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(body),
				})
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
	});

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

export default SearchProduct;
