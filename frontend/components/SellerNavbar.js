import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function SellerNavbar() {
	const router = useRouter();
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
