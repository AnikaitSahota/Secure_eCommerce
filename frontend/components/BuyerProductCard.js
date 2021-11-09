import { useRouter } from 'next/router';

function BuyerProductCard(props) {
	const router = useRouter();
	const productName = props.productName;
	const productDescription = props.productDescription.slice(0, 100) + '...';
	const productId = props.productId;
	const productImg = props.productImg1;

	function clicked() {
		router.push(`/Buyer/Product/${productId}`);
	}

	return (
		<div className='buyerProductCard'>
			<img src={productImg} style={{ width: '50%' }} />
			<h3>{productName}</h3>
			<p className='buyerProductCardBody'>{productDescription}</p>
			<button className='addBalance' onClick={(e) => clicked()}>
				Buy
			</button>
		</div>
	);
}

export default BuyerProductCard;
