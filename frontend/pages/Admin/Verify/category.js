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
			const allCookies = cookie.split(';');
			for (let i = 0; i < allCookies.length; i++) {
				var [cookieName, cookieValue] = allCookies[i].split('=');
				if (cookieName == 'info') {
					var cookies = JSON.parse(cookieValue);
					var tokenTemp = cookies.token;
					var typeTemp = cookies.type;
					var usernameTemp = cookies.username;
					if (typeTemp !== 'admin') {
						router.push('/');
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
				}
			}
		}
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
