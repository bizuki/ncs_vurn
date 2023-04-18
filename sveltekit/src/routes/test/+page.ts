import { fetchTestUserInfo } from '$lib/api/users'

export async function load({ }) {
    let userInfo = await fetchTestUserInfo();

    return { userInfo };
}
