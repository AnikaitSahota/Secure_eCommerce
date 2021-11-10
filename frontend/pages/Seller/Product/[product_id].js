import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerNavbar from '../../../components/SellerNavbar';
import api from '../../api';

function Product({ props }) {
	const router = useRouter();
	const { product_id } = router.query;
	const [name, setName] = useState('');
	const [description, setDescription] = useState('');
	const [category, setCategory] = useState('');
	const [quantity, setQuantity] = useState(0);
	const [price, setPrice] = useState(0);
	const [img1, setImg1] = useState('');
	const [img2, setImg2] = useState('');
	const [editable, setEditable] = useState(true);
	const [categories, setCategories] = useState([]);
	const [isFirstRender, setFirstRender] = useState(true);
	const [token, setToken] = useState('');
	const [username, setUsername] = useState('');

	useEffect(() => {
		if (isFirstRender && product_id) {
			setFirstRender(false);

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
						setUsername(usernameTemp);
						if (typeTemp !== 'seller') {
							router.push('/');
						}

						const body = {
							token: tokenTemp,
							username: usernameTemp,
						};
						fetch(`${api}/seller/get-categories/`, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json',
							},
							body: JSON.stringify(body),
						})
							.then((res) => res.json())
							.then((res) => {
								if (res.status == 'success') {
									setCategories(res.data);
								} else {
									alert(res.status);
								}
							});

						const body2 = {
							token: tokenTemp,
							username: usernameTemp,
							id: product_id,
						};
						fetch(`${api}/seller/view-product/`, {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json',
							},
							body: JSON.stringify(body2),
						})
							.then((res) => res.json())
							.then((res) => {
								if (res.status == 'success') {
									const temp = JSON.parse(res.data);
									setName(temp.name);
									setDescription(temp.description);
									setCategory(temp.category);
									setQuantity(temp.inventory);
									setPrice(temp.price);
									setImg1(temp.img1);
									setImg2(temp.img2);
								} else {
									alert(res.status);
								}
							});
					}
				}
			}
		}
	});

	function myTrim() {
		setName((prev) => prev.trim());
		setDescription((prev) => prev.trim());
		setCategory((prev) => prev.trim());
	}

	function securityCheck() {
		myTrim();
		const body = {
			token: token,
			username: username,
			id: product_id,
			description: description,
			price: price,
			inventory: quantity,
			img1: img1,
			img2: img2,
		};
		fetch(`${api}/seller/edit-product/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					alert('Information Updated');
				} else {
					alert(res.status);
				}
			});
		setEditable((prev) => !prev);
	}

	useEffect(() => {
		const submit = document.getElementById('submit');
		if (editable) {
			submit.style.display = 'none';
		} else {
			submit.style.display = 'block';
		}

		const edit = document.getElementById('edit');
		if (!editable) {
			edit.style.display = 'none';
		} else {
			edit.style.display = 'block';
		}
	}, [editable]);

	function makeEdits() {
		setEditable((prev) => !prev);
	}

	return (
		<div>
			<SellerNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<div className='flex_between'>
							<h2>Product Information</h2>
							<h3
								onClick={makeEdits}
								id='edit'
								style={{ cursor: 'pointer' }}
							>
								EDIT
							</h3>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Product Name</label>
							<input
								className='input'
								type='text'
								id='name'
								name='name'
								disabled={true}
								value={name}
								onChange={(e) => setName(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Description</label>
							<textarea
								className='input'
								id='description'
								disabled={editable}
								value={description}
								onChange={(e) => setDescription(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Category</label>
							<select
								value={category}
								disabled={true}
								onChange={(e) => setCategory(e.target.value)}
							>
								{categories.map((e, i) => {
									return (
										<option value={e.name} key={i}>
											{e.name}
										</option>
									);
								})}
							</select>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Quantity</label>
							<input
								className='input'
								type='number'
								id='quantity'
								name='quantity'
								disabled={editable}
								value={quantity}
								onChange={(e) => setQuantity(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Price ($)</label>
							<input
								className='input'
								type='number'
								id='price'
								name='price'
								disabled={editable}
								value={price}
								onChange={(e) => setPrice(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Image 1 (URL)</label>
							<input
								className='input'
								type='text'
								disabled={editable}
								value={img1}
								onChange={(e) => setImg1(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Image 2 (URL)</label>
							<input
								className='input'
								type='text'
								disabled={editable}
								value={img2}
								onChange={(e) => setImg2(e.target.value)}
							/>
						</div>
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
					</div>
				</div>
			</div>
		</div>
	);
}

export default Product;
