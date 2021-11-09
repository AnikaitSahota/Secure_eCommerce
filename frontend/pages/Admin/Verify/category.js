import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import AdminCategoryCard from '../../../components/AdminCategoryCard';
import AdminNavbar from '../../../components/AdminNavbar';
import api from '../../api';

function Category() {
	const router = useRouter();
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
