import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import AdminNavbar from '../../../components/AdminNavbar';
import AdminProductCard from '../../../components/AdminProductCard';
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
			if (typeTemp !== 'admin') {
				router.push('/');
			}
		}
	}, []);

	useEffect(() => {
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

	useEffect(() => {
		setProducts((prev) => prev);
	}, [products]);

	return (
		<div>
			<AdminNavbar />
			<div className='content'>
				{products.map((e, i) => {
					return (
						<AdminProductCard
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
