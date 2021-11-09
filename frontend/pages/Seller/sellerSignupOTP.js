import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState } from 'react';
import api from '../api';

function SellerSignupOTP() {
	const router = useRouter();
	const [otp, setOtp] = useState('');

	function securityCheck() {
		const email = document.cookie.split('=')[1];
		const body = { email_id: email, OTP: otp };
		console.log(body);
		fetch(`${api}/seller/OTPverification/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		})
			.then((res) => res.json())
			.then((res) => {
				console.log(res);
				if (res.status == 'success') {
					document.cookie =
						'email=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
					console.log(document.cookie);
					router.push(`/Seller/sellerLogin`);
				} else {
					alert(res.status);
				}
			});
	}

	return (
		<div className='centerScreenContainer'>
			<div className='cell'>
				<div style={{ width: '100%' }}>
					<h3>OTP has been sent to your registered Email</h3>
					<div className='inputGroup'>
						<label className='inputLabel'>Enter OTP</label>
						<input
							className='input'
							type='text'
							id='name'
							name='name'
							value={otp}
							onChange={(e) => setOtp(e.target.value)}
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
	);
}

export default SellerSignupOTP;
