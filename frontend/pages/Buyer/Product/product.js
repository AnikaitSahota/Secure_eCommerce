import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../../components/BuyerNavbar';
import BuyerProductCard from '../../../components/BuyerProductCard';
import UserCheck from '../../../components/userCheck';
import api from '../../api';

function Product() {
	const router = useRouter();
	const [products, setProducts] = useState([]);
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

		fetch(`${api}/product/all-products/`)
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					setProducts(res.data);
				} else {
					alert(res.status);
				}
			});
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
