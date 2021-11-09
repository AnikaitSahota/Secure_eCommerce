import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import * as checks from '../../components/LoginCheck';
import api from '../api';

function AdminSignup() {
	const router = useRouter();
	const [name, setName] = useState('');
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [phoneNumber, setPhoneNumber] = useState('');

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
		setName(name.trim());
		setPhoneNumber(phoneNumber.trim());
		setEmail(email.trim());
	}

	function securityCheck() {
		myTrim();
		const lengthChecked = checks.lengthCheck(username, password);
		if (lengthChecked[0]) {
			const usernameChecked = checks.usernameCheck(username);
			if (usernameChecked[0]) {
				const passwordChecked = checks.passwordCheck(password);
				if (passwordChecked[0]) {
					const body = {
						name: name,
						username: username,
						email_id: email,
						password: password,
						contact_number: phoneNumber,
					};
					fetch(`${api}/admin/signup/`, {
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
								date.setDate(date.getMinutes() + 10);
								document.cookie = `email=${email}; expires=${date};`;
								router.push(`/Admin/adminSignupOTP`);
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
					<h2>Signup (Admin)</h2>
					<div className='inputGroup'>
						<label className='inputLabel'>Full Name</label>
						<input
							className='input'
							type='text'
							id='name'
							name='name'
							value={name}
							onChange={(e) => setName(e.target.value)}
						/>
					</div>
					<div className='inputGroup'>
						<label className='inputLabel'>Email</label>
						<input
							className='input'
							type='email'
							id='email'
							name='email'
							value={email}
							onChange={(e) => setEmail(e.target.value)}
						/>
					</div>
					<div className='inputGroup'>
						<label className='inputLabel'>Phone Number</label>
						<input
							className='input'
							type='number'
							id='phoneNumber'
							name='phoneNumber'
							value={phoneNumber}
							onChange={(e) => setPhoneNumber(e.target.value)}
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
						<Link href='/Admin/adminLogin'>
							<a className='link'>Login</a>
						</Link>
						<Link href='/Seller/sellerLogin'>
							<a className='link'>Seller?</a>
						</Link>
						<Link href='/Buyer/buyerLogin'>
							<a className='link'>Buyer?</a>
						</Link>
					</div>
				</div>
			</div>
		</div>
	);
}

export default AdminSignup;
