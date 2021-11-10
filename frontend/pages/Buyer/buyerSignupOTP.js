import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import api from '../api';

function BuyerSignupOTP() {
	const router = useRouter();
	const [otp, setOtp] = useState('');

	function securityCheck() {
		const cookie = document.cookie;
		if (cookie) {
			const allCookies = cookie.split(';');
			for (let i = 0; i < allCookies.length; i++) {
				var [cookieName, cookieValue] = allCookies[i].split('=');
				if (cookieName == 'email') {
					const body = { email_id: cookieValue, OTP: otp };
					fetch(`${api}/customer/OTPverification/`, {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify(body),
					})
						.then((res) => res.json())
						.then((res) => {
							if (res.status == 'success') {
								document.cookie =
									'email=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
								router.push(`/Buyer/buyerLogin`);
							} else {
								alert(res.status);
							}
						});
				}
			}
		}
	}

	useEffect(() => {
		return () => {
			document.cookie = 'email=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
		};
	}, []);

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

export default BuyerSignupOTP;
