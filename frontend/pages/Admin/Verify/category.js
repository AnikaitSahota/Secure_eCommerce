import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import AdminCategoryCard from '../../../components/AdminCategoryCard';
import AdminNavbar from '../../../components/AdminNavbar';
import AdminProductCard from '../../../components/AdminProductCard';
import BuyerNavbar from '../../../components/BuyerNavbar';
import BuyerProductCard from '../../../components/BuyerProductCard';
import UserCheck from '../../../components/userCheck';
import api from '../../api';

function Category() {
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
			if (typeTemp !== 'admin') {
				router.push('/');
			}
		}
	}, []);

	useEffect(() => {
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

	useEffect(() => {
		setCategories((prev) => prev);
	}, [categories]);

	return (
		<div>
			<AdminNavbar />
			<div className='content'>
				{categories.map((e, i) => {
					return <AdminCategoryCard key={i} productName={e.name} />;
				})}
			</div>
		</div>
	);
}

export default Category;
