import router from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../components/BuyerNavbar';
import api from '../api';

function BuyerAccount() {
	const [name, setName] = useState('');
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [phoneNumber, setPhoneNumber] = useState('');
	const [address, setAddress] = useState('');
	const [editable, setEditable] = useState(true);

	const [balance, setBalance] = useState(0);
	const [newBalance, setNewBalance] = useState(0);
	const [addShow, setAddShow] = useState(false);
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
			if (typeTemp !== 'buyer') {
				router.push('/');
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
		fetch(`${api}/customer/get-customer-details/`, {
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
					setUsername(res.data.username);
					setPhoneNumber(res.data.contact_number);
					setAddress(res.data.address);
					setBalance(res.balance);
				} else {
					alert(res.status);
				}
			});
	}, []);

	function myTrim() {
		setUsername(username.trim());
		setAddress(address.trim());
		setName(name.trim());
		setPhoneNumber(phoneNumber.trim());
		setEmail(email.trim());
	}

	function securityCheck() {
		myTrim();
		const body = {
			token: token,
			username: usernameCurr,
			name: name,
			address: address,
			contact_number: phoneNumber,
		};
		fetch(`${api}/customer/update-customer-details/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					alert('Information Updated successfully');
				} else {
					alert(res.status);
				}
			});
		setEditable((prev) => !prev);
	}

	function makeEdits() {
		setEditable((prev) => !prev);
	}

	function showAddBalance() {
		setAddShow((prev) => !prev);
	}

	function addBalance() {
		const body = {
			token: token,
			username: usernameCurr,
			amount: newBalance,
		};
		fetch(`${api}/customer/update-wallet/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					setBalance(res.balance);
					alert('Balance Updated Successfully');
					setAddShow((prev) => !prev);
				} else {
					alert(res.status);
				}
			});
	}

	function logout() {
		const body = { token: token, username: usernameCurr };
		fetch(`${api}/customer/logout/`, {
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

	useEffect(() => {
		const temp = document.getElementsByClassName('newAmount');
		for (let i = 0; i < temp.length; i++) {
			if (addShow) {
				temp[i].style.display = 'block';
			} else {
				temp[i].style.display = 'none';
			}
		}

		const button = document.getElementById('addBalance');
		if (!addShow) {
			button.style.display = 'block';
		} else {
			button.style.display = 'none';
		}

		setNewBalance(0);
	}, [addShow]);

	return (
		<div>
			<BuyerNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<div className='flex_between'>
							<h2>Customer Information</h2>
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
						<div className='inputGroup'>
							<label className='inputLabel'>Address</label>
							<textarea
								className='input'
								id='address'
								name='address'
								disabled={editable}
								value={address}
								onChange={(e) => setAddress(e.target.value)}
							/>
						</div>
						<button
							className='submitButton'
							onClick={(e) => {
								e.preventDefault;
								securityCheck();
							}}
							id='submit'
						>
							Submit
						</button>
					</div>
				</div>
				<div className='cell'>
					<h3 style={{ width: '100%' }}>Balance : {balance}</h3>
					<div className={['inputGroup', 'newAmount'].join(' ')}>
						<label className='inputLabel'>Enter Amount</label>
						<input
							className='input'
							type='number'
							id='newBalance'
							name='newBalance'
							value={newBalance}
							onChange={(e) => setNewBalance(e.target.value)}
						/>
					</div>
					<button
						className='addBalance'
						id='addBalance'
						onClick={(e) => showAddBalance()}
					>
						Add Balance
					</button>
					<button
						className={['addBalance', 'newAmount'].join(' ')}
						onClick={(e) => addBalance()}
						id={'submit'}
					>
						Submit Balance
					</button>
				</div>
				<div className='logoutButton' onClick={(e) => logout()}>
					Logout
				</div>
			</div>
		</div>
	);
}

export default BuyerAccount;
