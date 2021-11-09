import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerCategoryCard from '../../../../components/SellerCategoryCard';
import SellerNavbar from '../../../../components/SellerNavbar';
import api from '../../../api';

function ProductCategories() {
	const router = useRouter();
	const [categories, setCategories] = useState([]);
	const [token, setToken] = useState('');
	const [type, setType] = useState('');
	const [username, setUsername] = useState('');

	useEffect(() => {
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
			if (typeTemp !== 'seller') {
				router.push('/');
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
