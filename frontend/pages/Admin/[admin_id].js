import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import AdminNavbar from '../../components/AdminNavbar';
import api from '../api';

function AdminAccount() {
	const router = useRouter();
	const [name, setName] = useState('');
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [phoneNumber, setPhoneNumber] = useState('');
	const [editable, setEditable] = useState(true);
	const [user, setUser] = useState({});
	const [token, setToken] = useState('');
	const [type, setType] = useState('');
	const [usernameCurr, setUsernameCurr] = useState('');

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
			setUsernameCurr(usernameTemp);
			if (typeTemp !== 'admin') {
				router.push('/');
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
		fetch(`${api}/admin/get-admin-details/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					setUser(res.data);
				} else {
					alert(res.status);
				}
			});
	}, []);

	useEffect(() => {
		setUsername(user.username);
		setEmail(user.email_id);
		setPhoneNumber(user.contact_number);
		setName(user.name);
	}, [user]);

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
		fetch(`${api}/admin/update-admin-details/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
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
		fetch(`${api}/admin/logout/`, {
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
						'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
					document.cookie =
						'type=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
					document.cookie =
						'username=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
					router.push(`/`);
				} else {
					alert(res.status);
					coneole.log('Unable to Logout');
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
			<AdminNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<div className='flex_between'>
							<h2>Admin Information</h2>
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
							You are{' '}
							{user.verified ? 'Verified' : 'Not Verified'}
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

export default AdminAccount;
