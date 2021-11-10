import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerProductCard from '../../../../components/SellerProductCard';
import SellerNavbar from '../../../../components/SellerNavbar';
import api from '../../../api';

function SellerCategoryAccount() {
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
						if (typeTemp !== 'seller') {
							router.push('/');
						}

						const body = {
							token: tokenTemp,
							username: usernameTemp,
							category_name: category_name,
						};
						fetch(`${api}/seller/get-specific-products/`, {
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
			<SellerNavbar />
			<div className='content'>
				<h1 style={{ textAlign: 'center', padding: '3rem' }}>
					{category_name}
				</h1>
				{products.map((e, i) => {
					return (
						<SellerProductCard
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

export default SellerCategoryAccount;
