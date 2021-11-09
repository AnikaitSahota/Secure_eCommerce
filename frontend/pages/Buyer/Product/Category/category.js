import { useEffect, useState } from 'react';
import BuyerCategoryCard from '../../../../components/BuyerCategoryCard';
import BuyerNavbar from '../../../../components/BuyerNavbar';
import api from '../../../api';

function ProductCategories() {
	const [categories, setCategories] = useState([]);

	useEffect(() => {
		const cookie = document.cookie;
		if (!cookie) {
			router.push(`/`);
		} else {
			var cookies = JSON.parse(cookie.split('=')[1]);
			var tokenTemp = cookies.token;
			var typeTemp = cookies.type;
			var usernameTemp = cookies.username;
			if (typeTemp !== 'buyer') {
				router.push('/');
			}
		}

		fetch(`${api}/product/all-categories/`)
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
			<BuyerNavbar />
			<div className='content'>
				{categories.map((e, i) => {
					return <BuyerCategoryCard categoryName={e.name} key={i} />;
				})}
			</div>
		</div>
	);
}

export default ProductCategories;
