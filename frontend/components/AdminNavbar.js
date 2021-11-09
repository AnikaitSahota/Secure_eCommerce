import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function AdminNavbar() {
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
			if (typeTemp !== 'admin') {
				router.push('/');
			}
		}
	}, []);

	return (
		<div className='navbar'>
			<div>
				<Link href='/Admin/Verify/product'>
					<a>Products</a>
				</Link>
				<Link href='/Admin/Verify/seller'>
					<a style={{ marginLeft: '1rem' }}>Sellers</a>
				</Link>
				<Link href='/Admin/Verify/category'>
					<a style={{ marginLeft: '1rem' }}>Category</a>
				</Link>
				<Link href='/Admin/addCategory'>
					<a style={{ marginLeft: '1rem' }}>Add Category</a>
				</Link>
			</div>
			<Link href={`/Admin/${username}`}>
				<a>Account</a>
			</Link>
		</div>
	);
}

export default AdminNavbar;
