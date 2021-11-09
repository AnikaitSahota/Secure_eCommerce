import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerCategoryCard from '../../../../components/BuyerCategoryCard';
import BuyerNavbar from '../../../../components/BuyerNavbar';
import BuyerProductCard from '../../../../components/BuyerProductCard';
import api from '../../../api';

function BuyerCategoryAccount() {
	const router = useRouter();
	const { category_name } = router.query;
	const [isFirstRender, setFirstRender] = useState(true);
	const [products, setProducts] = useState([]);
	const [token, setToken] = useState('');
	const [type, setType] = useState('');
	const [username, setUsername] = useState('');

	useEffect(() => {
		if (isFirstRender && category_name) {
			setFirstRender(false);
			const cookie = document.cookie;
			if (!cookie) {
				router.push(`/`);
			} else {
				var cookies = cookie.split(';');
				var tokenTemp = cookies[0].split('=')[1];
				var typeTemp = cookies[1].split('=')[1];
				var usernameTemp = cookies[2].split('=')[1];
				setToken(tokenTemp);
				setType(typeTemp);
				setUsername(usernameTemp);
				if (typeTemp !== 'buyer') {
					router.push('/');
				}
			}

			const body = {
				token: tokenTemp,
				username: usernameTemp,
				category_name: category_name,
			};
			fetch(`${api}/product/specific-category/`, {
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
	});

	return (
		<div>
			<BuyerNavbar />
			<div className='content'>
				<h1 style={{ textAlign: 'center', padding: '3rem' }}>
					{category_name}
				</h1>
				{products.map((e, i) => {
					return (
						<BuyerProductCard
							key={i}
							productName={e.name}
							productDescription={e.description}
							productId={e.id}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default BuyerCategoryAccount;
