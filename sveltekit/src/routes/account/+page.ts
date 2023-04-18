import { getToken } from '$lib/stores/token';
import { fetchUserInfo } from '$lib/api/users'
import { redirect } from '@sveltejs/kit';

export async function load({ }) {
	const token = getToken();

    if (!token) {
        throw redirect(302, '/login');
    }

    let userInfo = await fetchUserInfo(token);

    return { userInfo };
}
