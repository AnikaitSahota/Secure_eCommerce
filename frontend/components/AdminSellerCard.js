import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import api from '../pages/api';

function AdminSellerCard({ name, verified, username, phone, email }) {
	const router = useRouter();

	const [token, setToken] = useState('');
	const [usernameCurr, setUsernameCurr] = useState('');

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
					setToken(tokenTemp);
					setUsernameCurr(usernameTemp);
					if (typeTemp !== 'admin') {
						router.push('/');
					}
				}
			}
		}

		if (verified) {
			const box = document.getElementById(name);
			box.style.backgroundColor = '#22dd22';

			const buttons = box.getElementsByTagName('button');
			buttons[0].style.display = 'none';
		}
	}, []);

	function verifyNow() {
		const body = {
			token: token,
			username: usernameCurr,
			sellerUsername: username,
		};
		fetch(`${api}/admin/verify-seller/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					const box = document.getElementById(name);
					box.style.backgroundColor = '#22dd22';

					const buttons = box.getElementsByTagName('button');
					buttons[0].style.display = 'none';
				} else {
					alert('Unable to verify');
				}
			});
	}

	function deleteNow() {
		const body = {
			token: token,
			username: usernameCurr,
			sellerUsername: username,
		};
		fetch(`${api}/admin/delete-seller/`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					const box = document.getElementById(name);
					box.style.backgroundColor = '#dd2222';

					const buttons = box.getElementsByTagName('button');
					for (let i = 0; i < buttons.length; i++) {
						buttons[i].style.display = 'none';
					}
				} else {
					alert('Unable to Delete');
				}
			});
	}

	return (
		<div className='buyerProductCard' id={name}>
			<h3>{name}</h3>
			<h5>{username}</h5>
			<p>{email}</p>
			<p>{phone}</p>
			<div>
				<button
					className='verify'
					id='verify'
					onClick={(e) => verifyNow()}
					style={{ marginBottom: '1rem' }}
				>
					Verify
				</button>
				<button
					className='delete'
					id='delete'
					onClick={(e) => deleteNow()}
				>
					Delete
				</button>
			</div>
		</div>
	);
}

export default AdminSellerCard;
