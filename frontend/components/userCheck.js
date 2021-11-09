function UserCheck() {
	const cookie = document.cookie;

	if (!cookie) {
		console.log('No Cookie Present');
		return [false, null];
	} else {
		var info = document.cookie.split('=')[1];
		const user = JSON.parse(info);
		return [true, user];
	}
}

export default UserCheck;