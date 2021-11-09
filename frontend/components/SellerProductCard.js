import { useRouter } from 'next/router';

function SellerProductCard(props) {
	const router = useRouter();
	const productName = props.productName;
	const productDescription = props.productDescription.slice(0, 100) + '...';
	const productId = props.productId;

	function clicked() {
		console.log(productId);
		router.push(`/Seller/Product/${productId}`);
	}

	return (
		<div className='buyerProductCard'>
			<h3>{productName}</h3>
			<p className='buyerProductCardBody'>{productDescription}</p>
			<button className='addBalance' onClick={(e) => clicked()}>
				View
			</button>
		</div>
	);
}

export default SellerProductCard;
