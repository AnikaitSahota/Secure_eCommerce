import { useEffect, useState } from 'react';
import BuyerCategoryCard from '../../../../components/BuyerCategoryCard';
import BuyerNavbar from '../../../../components/BuyerNavbar';
import api from '../../../api';

function ProductCategories() {
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
