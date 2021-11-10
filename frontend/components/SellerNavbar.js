import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function SellerNavbar() {
	const router = useRouter();
	const [username, setUsername] = useState('');

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
					setUsername(usernameTemp);
					if (typeTemp !== 'seller') {
						router.push('/');
					}
				}
			}
		}
	}, []);

	return (
		<div className='navbar'>
			<div>
				<Link href='/Seller/Product/product'>
					<a>Products</a>
				</Link>
				<Link href='/Seller/Product/Category/category'>
					<a style={{ marginLeft: '1rem' }}>Categories</a>
				</Link>
			</div>
			<Link href={`/Seller/${username}`}>
				<a>Account</a>
			</Link>
		</div>
	);
}

export default SellerNavbar;
