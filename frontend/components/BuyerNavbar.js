import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function BuyerNavbar() {
	const [search, setSearch] = useState('');
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
			if (typeTemp !== 'buyer') {
				router.push('/');
			}
		}
	}, []);

	return (
		<div className='navbar'>
			<div>
				<Link href='/Buyer/Product/product'>
					<a>Products</a>
				</Link>
				<Link href='/Buyer/Product/Category/category'>
					<a style={{ marginLeft: '1rem' }}>Categories</a>
				</Link>
			</div>
			<div style={{ width: '70%' }}>
				<input
					className='searchInput'
					type='text'
					name='search'
					id='search'
					value={search}
					onChange={(e) => setSearch(e.target.value)}
				/>
				<button className='searchButton'>Search</button>
			</div>
			<Link href={`/Buyer/${username}`}>
				<a>Account</a>
			</Link>
		</div>
	);
}

export default BuyerNavbar;
