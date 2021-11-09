import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import SellerNavbar from '../../../components/SellerNavbar';
import api from '../../api';

function AddProduct() {
	const router = useRouter();
	const [name, setName] = useState('');
	const [description, setDescription] = useState('');
	const [category, setCategory] = useState('');
	const [quantity, setQuantity] = useState(1);
	const [price, setPrice] = useState(0);
	const [img1, setImg1] = useState('');
	const [img2, setImg2] = useState('');
	const [categories, setCategories] = useState([]);
	const [token, setToken] = useState('');
	const [type, setType] = useState('');
	const [username, setUsername] = useState('');

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
			setUsername(usernameTemp);
			if (typeTemp !== 'seller') {
				router.push('/');
			}
		}

		const body = { token: tokenTemp, username: usernameTemp };
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
					setCategory(res.data[0]);
				} else {
					alert(res.status);
				}
			});
	}, []);

	function myTrim() {
		setName(name.trim());
		setDescription(description.trim());
	}

	function securityCheck() {
		myTrim();
		const body = {
			token: token,
			username: username,
			name: name,
			description: description,
			category: category.name,
			inventory: quantity,
			price: price,
			img1: img1,
			img2: img2,
		};
		fetch(`${api}/seller/add-product/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					router.push('/Seller/Product/product');
				} else {
					alert(res.status);
				}
			});
	}

	return (
		<div>
			<SellerNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<h2>Add Product</h2>
						<div className='inputGroup'>
							<label className='inputLabel'>Product Name</label>
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
							<label className='inputLabel'>Description</label>
							<textarea
								className='input'
								id='description'
								value={description}
								onChange={(e) => setDescription(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Category</label>
							<select
								value={category}
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
								value={price}
								onChange={(e) => setPrice(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Image 1 (URL)</label>
							<input
								className='input'
								type='text'
								value={img1}
								onChange={(e) => setImg1(e.target.value)}
							/>
						</div>
						<div className='inputGroup'>
							<label className='inputLabel'>Image 2 (URL)</label>
							<input
								className='input'
								type='text'
								value={img2}
								onChange={(e) => setImg2(e.target.value)}
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

export default AddProduct;
