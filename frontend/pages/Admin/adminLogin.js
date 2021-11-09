import Link from 'next/link';
import router from 'next/router';
import { useState } from 'react';
import * as checks from '../../components/LoginCheck';
import * as style from '../../styles/login.module.css';
import api from '../api';

function AdminLogin() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

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
					console.log(JSON.stringify(body));
					fetch(`${api}/admin/login/`, {
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
								document.cookie = `token=${res.token}; expires = ${date}`;
								document.cookie = `type=admin; expires = ${date}`;
								document.cookie = `username=${username}; expires = ${date}`;
								router.push(`/Admin/Verify/seller`);
							} else {
								alert(res.status);
								console.log('Login Failed');
							}
						});
				} else {
					alert(passwordChecked[1]);
					console.log(passwordChecked[1]);
				}
			} else {
				alert(usernameChecked[1]);
				console.log(usernameChecked[1]);
			}
		} else {
			alert(lengthChecked[1]);
			console.log(lengthChecked[1]);
		}
	}

	return (
		<div className={style.centerScreenContainer}>
			<div className={style.cell}>
				<div style={{ width: '100%' }}>
					<h2>Login (Admin)</h2>
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
						<Link href='/Admin/adminSignup'>
							<a className='link'>Signup</a>
						</Link>
						<Link href='/Buyer/buyerLogin'>
							<a className='link'>Customer?</a>
						</Link>
						<Link href='/Seller/sellerLogin'>
							<a className='link'>Seller?</a>
						</Link>
					</div>
				</div>
			</div>
		</div>
	);
}

export default AdminLogin;
