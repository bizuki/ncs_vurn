import type { Token } from '$lib/types/Tokens';
import { getResponse, makeClient } from './client'

export const getToken = async (form: FormData) : Promise<Token> => {
    let client = makeClient();
    
    return await getResponse(async () => {
        let response = await client.postForm(
            'security/token',
            form
        );
        return response.data;
    })
};

export const register = async (form: FormData) : Promise<Token> => {
    let client = makeClient();
    
    return await getResponse(async () => {
        let response = await client.post(
            'security/register',
            {
                email: form.get('username'),
                password: form.get('password'),
                first_name: form.get('first_name'),
                last_name: form.get('last_name'),
            }
        );
        return response.data;
    });
};
