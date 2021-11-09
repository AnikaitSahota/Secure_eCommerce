import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerNavbar from '../../components/SellerNavbar';
import api from '../api';

function SellerAccount() {
	const router = useRouter();
	const [name, setName] = useState('');
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [phoneNumber, setPhoneNumber] = useState('');
	const [editable, setEditable] = useState(true);
	const [verified, setVerified] = useState('');
	const [token, setToken] = useState('');
	const [usernameCurr, setUsernameCurr] = useState('');

	useEffect(() => {
		const cookie = document.cookie;
		if (!cookie) {
			router.push(`/`);
		} else {
			var cookies = JSON.parse(cookie.split('=')[1]);
			var tokenTemp = cookies.token;
			var typeTemp = cookies.type;
			var usernameTemp = cookies.username;
			setToken(tokenTemp);
			setUsernameCurr(usernameTemp);
			if (typeTemp !== 'seller') {
				router.push('/');
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
		fetch(`${api}/seller/get-seller-details/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					setName(res.data.name);
					setEmail(res.data.email_id);
					setPhoneNumber(res.data.contact_number);
					setVerified(res.data.verified);
					setUsername(res.data.username);
				} else {
					alert(res.status);
				}
			});
	}, []);

	function myTrim() {
		setUsername(username.trim());
		setName(name.trim());
		setPhoneNumber(phoneNumber.trim());
		setEmail(email.trim());
	}

	function securityCheck() {
		myTrim();
		const body = {
			name: name,
			contact_number: phoneNumber,
			token: token,
			username: username,
		};
		fetch(`${api}/seller/update-seller-details/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					alert('Information Successfully Updated');
					setEditable((prev) => !prev);
				} else {
					alert(res.status);
				}
			});
	}

	function makeEdits() {
		setEditable((prev) => !prev);
	}

	function logout() {
		const body = { token: token, username: usernameCurr };
		fetch(`${api}/seller/logout/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					document.cookie =
						'info=; expires = Thu, 01 Jan 1970 00:00:00 UTC;';
					router.push(`/Seller/sellerLogin`);
				} else {
					alert(res.status);
				}
			});
	}

	useEffect(() => {
		const editButton = document.getElementById('edit');
		if (editable) {
			editButton.style.display = 'block';
		} else {
			editButton.style.display = 'none';
		}

		const submit = document.getElementById('submit');
		if (editable) {
			submit.style.display = 'none';
		} else {
			submit.style.display = 'block';
		}
	}, [editable]);

	return (
		<div>
			<SellerNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<div className='flex_between'>
							<h2>Seller Information</h2>
							<h3
								onClick={makeEdits}
								id='edit'
								style={{ cursor: 'pointer' }}
							>
								EDIT
							</h3>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Full Name</label>
							<input
								className='input'
								type='text'
								id='name'
								name='name'
								disabled={editable}
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
								disabled={true}
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
								disabled={editable}
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
								disabled={true}
								value={username}
								onChange={(e) => setUsername(e.target.value)}
							/>
						</div>
						<h3>
							You are {verified ? 'Verified' : 'Not Verified'}
						</h3>
						<button
							className='submitButton'
							id='submit'
							onClick={(e) => {
								e.preventDefault;
								securityCheck();
							}}
						>
							Submit
						</button>
						<button
							className='logoutButton'
							onClick={(e) => logout()}
						>
							Logout
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}

export default SellerAccount;
