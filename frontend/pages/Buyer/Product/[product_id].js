import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import BuyerNavbar from '../../../components/BuyerNavbar';
import api from '../../api';

function BuyerProductSingle() {
	const router = useRouter();
	const { product_id } = router.query;
	const [name, setName] = useState('');
	const [category, setCategory] = useState('');
	const [description, setDescription] = useState('');
	const [price, setPrice] = useState(0);
	const [quantity, setQuantity] = useState(0);
	const [img1, setImg1] = useState('');
	const [img2, setImg2] = useState('');
	const [buyAmount, setBuyAmount] = useState(0);
	const [buyPrice, setBuyPrice] = useState(0);
	const [token, setToken] = useState('');
	const [username, setUsername] = useState('');
	const [isFirstRender, setFirstRender] = useState(true);
	const [editbale, setEditable] = useState(true);

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
					}
				}
			}

			const body = {
				id: product_id,
			};
			fetch(`${api}/product/specific-product/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(body),
			})
				.then((res) => res.json())
				.then((res) => {
					if (res.status == 'success') {
						const temp = JSON.parse(res.data);
						setName(temp.name);
						setPrice(temp.price);
						setQuantity(temp.inventory);
						setCategory(temp.category);
						setDescription(temp.description);
						setImg1(temp.img1);
						setImg2(temp.img2);
					} else {
						alert(res.status);
					}
				});
		}
	});

	function buyProduct() {
		setEditable((prev) => !prev);
	}

	function placeOrder() {
		const body = {
			token: token,
			username: username,
			id: product_id,
			quantity: buyAmount,
		};
		fetch(`${api}/customer/buy-product/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 'success') {
					alert(
						`${buyAmount} quantity of ${name} has been purchased successfully. Current Balance is ${res.balance}`
					);
					router.push('/Buyer/Product/product');
				} else {
					alert(res.status);
				}
			});
		setEditable((prev) => !prev);
	}

	useEffect(() => {
		const submit = document.getElementById('submit');
		const hidden = document.getElementById('hidden');
		if (editbale) {
			submit.style.display = 'block';
			hidden.style.display = 'none';
		} else {
			submit.style.display = 'none';
			hidden.style.display = 'block';
		}
	}, [editbale]);

	useEffect(() => {
		setBuyPrice(buyAmount * price);
	}, [buyAmount]);

	return (
		<div>
			<BuyerNavbar />
			<div className='centerScreenContainer'>
				<div className='cell'>
					<div style={{ width: '100%' }}>
						<div
							style={{
								display: 'flex',
								justifyContent: 'space-around',
							}}
						>
							<img src={img1} style={{ width: '35%' }} />
							<img src={img2} style={{ width: '35%' }} />
						</div>
						<h1>{name}</h1>
						<h4>{category}</h4>
						<p>{description}</p>
						<p>{quantity} pieces left</p>
						<h3>${price}</h3>
						<button
							className='addBalance'
							style={{ marginBottom: '1rem' }}
							onClick={(e) => {
								alert(`Your link is: ${api}${router.asPath}`);
							}}
						>
							Get Share Link
						</button>
						<button
							className='addBalance'
							onClick={(e) => buyProduct()}
							id='submit'
						>
							Buy
						</button>
						<div id='hidden'>
							<div className='inputGroup'>
								<label className='inputLabel'>
									Buy Quantity
								</label>
								<input
									className='input'
									type='number'
									id='buyAmount'
									name='buyAmount'
									value={buyAmount}
									onChange={(e) =>
										setBuyAmount(e.target.value)
									}
								/>
							</div>
							<h3>Total Payable Amount : ${buyPrice}</h3>
							<button
								className='addBalance'
								onClick={(e) => placeOrder()}
								id='pay'
							>
								Place Order
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default BuyerProductSingle;
