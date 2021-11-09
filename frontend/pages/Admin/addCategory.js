import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import AdminNavbar from '../../components/AdminNavbar';
import api from '../api';

function AddCategory() {
	const router = useRouter();
	const [name, setName] = useState('');
	const [description, setDescription] = useState('');
	const [token, setToken] = useState('');
	const [username, setUsername] = useState('');

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
			setUsername(usernameTemp);
			if (typeTemp !== 'admin') {
				router.push('/');
			}
		}
	}, []);

	function myTrim() {
		setName((prev) => prev.trim());
		setDescription((prev) => prev.trim());
	}

	function securityCheck() {
		myTrim();
		const body = {
			name: name,
			description: description,
			token: token,
			username: username,
		};
		fetch(`${api}/admin/addCategory/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					router.push(`/Admin/Verify/category`);
				} else {
					alert(res.status);
				}
			});
	}

	return (
		<div>
			<AdminNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<h2>Add Category</h2>
						<div className='inputGroup'>
							<label className='inputLabel'>Category Name</label>
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
							<label className='inputLabel'>
								Category Description
							</label>
							<textarea
								className='input'
								value={description}
								onChange={(e) => setDescription(e.target.value)}
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
					</div>
				</div>
			</div>
		</div>
	);
}

export default AddCategory;
