import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import * as checks from '../../components/LoginCheck';
import api from '../api';

function BuyerLogin() {
	const router = useRouter();
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

	useEffect(() => {
		const cookie = document.cookie;
		if (cookie) {
			var cookies = JSON.parse(cookie.split('=')[1]);
			var tokenTemp = cookies.token;
			var typeTemp = cookies.type;
			var usernameTemp = cookies.username;
			if (typeTemp == 'seller') {
				router.push('/Seller/Product/product');
			} else if (typeTemp == 'admin') {
				router.push('/Admin/Verify/product');
			} else if (typeTemp == 'buyer') {
				router.push('/Buyer/Product/product');
			}
		}
	}, []);

	function myTrim() {
		setUsername(username.trim());
		setPassword(password.trim());
	}

	function securityCheck() {
		myTrim();
		const lengthChecked = checks.lengthCheck(username, password);
		if (lengthChecked[0]) {
			const usernameChecked = checks.usernameCheck(username);
			if (usernameChecked[0]) {
				const passwordChecked = checks.passwordCheck(password);
				if (passwordChecked[0]) {
					const body = { username: username, password: password };
					fetch(`${api}/customer/login/`, {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify(body),
					})
						.then((res) => res.json())
						.then((res) => {
							if (res.status == 'success') {
								const date = new Date();
								date.setDate(date.getDate() + 1);
								document.cookie = `info={ "token" : "${res.token}", "type" : "buyer", "username" : "${username}"}; expires = ${date}`;
								router.push(`/Buyer/Product/product`);
							} else {
								alert(res.status);
							}
						});
				} else {
					alert(passwordChecked[1]);
				}
			} else {
				alert(usernameChecked[1]);
			}
		} else {
			alert(lengthChecked[1]);
		}
	}

	return (
		<div className='centerScreenContainer'>
			<div className='cell'>
				<div style={{ width: '100%' }}>
					<h2>Login (Customer)</h2>
					<div className='inputGroup'>
						<label className='inputLabel'>Username</label>
						<input
							className='input'
							type='text'
							id='username'
							name='username'
							value={username}
							onChange={(e) => setUsername(e.target.value)}
						/>
					</div>
					<div className='inputGroup'>
						<label className='inputLabel'>Password</label>
						<input
							className='input'
							type='password'
							id='password'
							name='password'
							value={password}
							onChange={(e) => setPassword(e.target.value)}
						/>
					</div>
					<button
						className='submitButton'
						onClick={(e) => {
							e.preventDefault;
							securityCheck();
						}}
					>
						Submit
					</button>
					<div className='spaceBetween'>
						<Link href='/Buyer/buyerSignup'>
							<a className='link'>Signup</a>
						</Link>
						<Link href='/Seller/sellerLogin'>
							<a className='link'>Seller?</a>
						</Link>
						<Link href='/Admin/adminLogin'>
							<a className='link'>Admin?</a>
						</Link>
					</div>
				</div>
			</div>
		</div>
	);
}

export default BuyerLogin;
