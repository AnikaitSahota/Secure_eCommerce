import SellerNavbar from '../../../components/SellerNavbar';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerProductCard from '../../../components/SellerProductCard';
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
			if (typeTemp !== 'seller') {
				router.push('/');
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
		fetch(`${api}/seller/get-products/`, {
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
					console.log(res.status);
					alert(res.status);
				}
			});
	}, []);

	useEffect(() => {
		setProducts((prev) => prev);
	}, [products]);

	function addProduct() {
		router.push(`/Seller/Product/addProduct`);
	}

	return (
		<div>
			<SellerNavbar />
			<div className='content'>
				<button className='addProduct' onClick={(e) => addProduct()}>
					Add Product
				</button>
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

export default Product;
