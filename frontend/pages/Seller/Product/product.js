import SellerNavbar from '../../../components/SellerNavbar';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerProductCard from '../../../components/SellerProductCard';
import api from '../../api';

function Product() {
	const router = useRouter();
	const [products, setProducts] = useState([]);

	useEffect(() => {
		const cookie = document.cookie;
		if (!cookie) {
			router.push(`/`);
		} else {
			var cookies = JSON.parse(cookie.split('=')[1]);
			var tokenTemp = cookies.token;
			var typeTemp = cookies.type;
			var usernameTemp = cookies.username;
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
