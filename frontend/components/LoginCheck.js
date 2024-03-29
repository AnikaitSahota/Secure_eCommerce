function lengthCheck(username, password) {
	if (username.length < 8) {
		return [false, 'Username Too Short!'];
	} else if (password.length < 8) {
		return [false, 'Password Too Short!'];
	}
	return [true, 'Length Checked'];
}

function usernameCheck(username) {
	const pattern = new RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$');
	if (pattern.test(username)) {
		return [true, 'Username Checked'];
	} else {
		return [
			false,
			'Username must have: capital letter, small letter and number',
		];
	}
}

function passwordCheck(password) {
	const pattern = new RegExp(
		'^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[-+_!@#$%^&*.,?]).+$'
	);
	if (pattern.test(password)) {
		return [true, 'Password Checked'];
	} else {
		return [
			false,
			'Password must have: capital letter, small letter, number and special character',
		];
	}
}

export default lengthCheck;
export { lengthCheck, usernameCheck, passwordCheck };
