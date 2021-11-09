import { useRouter } from 'next/router';

function SellerCategoryCard({ categoryName }) {
	const router = useRouter();

	function clicked() {
		router.push(`/Seller/Product/Category/${categoryName}`);
	}

	return (
		<div>
			<h1 className='category' onClick={(e) => clicked()}>
				{categoryName}
			</h1>
		</div>
	);
}

export default SellerCategoryCard;
