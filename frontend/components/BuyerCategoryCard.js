import { useRouter } from 'next/router';

function BuyerCategoryCard({ categoryName }) {
	const router = useRouter();

	function clicked() {
		router.push(`/Buyer/Product/Category/${categoryName}`);
	}

	return (
		<div>
			<h1 className='category' onClick={(e) => clicked()}>
				{categoryName}
			</h1>
		</div>
	);
}

export default BuyerCategoryCard;
