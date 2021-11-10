import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import AdminNavbar from '../../../components/AdminNavbar';
import AdminSellerCard from '../../../components/AdminSellerCard';
import api from '../../api';

function AdminVerifySeller() {
	const router = useRouter();
	const [sellers, setSellers] = useState([]);

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

					const body = { token: tokenTemp, username: usernameTemp };
					fetch(`${api}/admin/get-sellers/`, {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify(body),
					})
						.then((res) => res.json())
						.then((res) => {
							if (res.status == 'success') {
								setSellers(res.data);
							} else {
								alert(res.status);
							}
						});
				}
			}
		}
	}, []);

	useEffect(() => {
		setSellers((prev) => prev);
	}, [sellers]);

	return (
		<div>
			<AdminNavbar />
			<div className='content'>
				{sellers.map((e, i) => {
					return (
						<AdminSellerCard
							key={i}
							name={e.name}
							username={e.username}
							email={e.email_id}
							phone={e.contact_number}
							verified={e.verified}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default AdminVerifySeller;
