import Link from 'next/link';
import { useState } from 'react';
import * as checks from '../../components/LoginCheck';
import * as style from '../../styles/login.module.css';

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
					console.log(username);
					console.log(password);
				} else {
					console.log(passwordChecked[1]);
				}
			} else {
				console.log(usernameChecked[1]);
			}
		} else {
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
						<Link href='/Admin/buyerLogin'>
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
