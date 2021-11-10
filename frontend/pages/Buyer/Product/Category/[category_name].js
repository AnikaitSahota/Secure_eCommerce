import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../../../components/BuyerNavbar';
import BuyerProductCard from '../../../../components/BuyerProductCard';
import api from '../../../api';

function BuyerCategoryAccount() {
	const router = useRouter();
	const { category_name } = router.query;
	const [isFirstRender, setFirstRender] = useState(true);
	const [products, setProducts] = useState([]);

	useEffect(() => {
		if (isFirstRender && category_name) {
			setFirstRender(false);
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
						if (typeTemp !== 'buyer') {
							router.push('/');
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
				}
			}
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
							productImg1={e.img1}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default BuyerCategoryAccount;
