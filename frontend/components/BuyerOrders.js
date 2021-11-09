import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function BuyerOrder(props) {
	const orderName = props.orderName;
	const orderQuantity = props.orderQuantity;
	const orderAmount = props.orderAmount;
	const orderTime = new Date(props.orderTime).toString();

	return (
		<div className='buyerProductCard'>
			<h3>Product Name: {orderName}</h3>
			<p>Quantity Purchased: {orderQuantity}</p>
			<p>Order Time: {orderTime}</p>
			<h3>Total Amount Paid: {orderAmount}</h3>
		</div>
	);
}

export default BuyerOrder;
