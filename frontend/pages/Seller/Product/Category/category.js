import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerCategoryCard from '../../../../components/SellerCategoryCard';
import SellerNavbar from '../../../../components/SellerNavbar';
import api from '../../../api';

function ProductCategories() {
	const router = useRouter();
	const [categories, setCategories] = useState([]);

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
					if (typeTemp !== 'seller') {
						router.push('/');
					}
				}
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
		fetch(`${api}/seller/get-categories/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					setCategories(res.data);
				} else {
					alert(res.status);
				}
			});
	}, []);

	return (
		<div>
			<SellerNavbar />
			<div className='content'>
				{categories.map((e, i) => {
					return <SellerCategoryCard categoryName={e.name} key={i} />;
				})}
			</div>
		</div>
	);
}

export default ProductCategories;
