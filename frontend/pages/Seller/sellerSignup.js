import Link from 'next/link';
import { useState } from 'react';
import * as style from '../../styles/signup.module.css';

function SellerSignup() {
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
		<div className='centerScreenContainer'>
			<div className='cell'>
				<div style={{ width: '100%' }} method='POST'>
					<h2>Signup (Seller)</h2>
					<div className='inputGroup'>
						<label className='inputLabel'>Full Name</label>
						<input
							className='input'
							type='text'
							id='name'
							name='name'
						/>
					</div>
					<div className='inputGroup'>
						<label className='inputLabel'>Email</label>
						<input
							className='input'
							type='email'
							id='email'
							name='email'
						/>
					</div>
					<div className='inputGroup'>
						<label className='inputLabel'>Phone Number</label>
						<input
							className='input'
							type='number'
							id='phoneNumber'
							name='phoneNumber'
						/>
					</div>
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
						<Link href='/Seller/sellerLogin'>
							<a className='link'>Login</a>
						</Link>
						<Link href='/Buyer/buyerLogin'>
							<a className='link'>Customer?</a>
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

export default SellerSignup;
