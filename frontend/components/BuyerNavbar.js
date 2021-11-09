import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function BuyerNavbar() {
	const [search, setSearch] = useState('');
	const router = useRouter();
	const [username, setUsername] = useState('');

	useEffect(() => {
		const cookie = document.cookie;
		if (!cookie) {
			router.push(`/`);
		} else {
			var cookies = JSON.parse(cookie.split('=')[1]);
			var tokenTemp = cookies.token;
			var typeTemp = cookies.type;
			var usernameTemp = cookies.username;
			setUsername(usernameTemp);
		}
	}, []);

	function onSearch() {
		router.push(`/Buyer/Product/Search/${search}`);
	}

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
				<button className='searchButton' onClick={(e) => onSearch()}>
					Search
				</button>
			</div>
			<Link href={`/Buyer/${username}`}>
				<a>Account</a>
			</Link>
		</div>
	);
}

export default BuyerNavbar;
