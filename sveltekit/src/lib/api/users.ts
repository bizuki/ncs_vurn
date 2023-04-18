import { getResponse, makeClient } from './client'
import type { UserInfo } from '../types/Users'

export const fetchUserInfo = async (token: string, id?: number) : Promise<UserInfo> => {
    let client = makeClient();
    
    client.interceptors.request.use(config => {
        config.headers['Authorization'] = `Bearer ${token}`;
        return config;
    });
    
    let response = id ? await client.get(`users/${id}`) : await client.get(`users/me`);
    return response.data;
};

export const fetchTestUserInfo = async () : Promise<UserInfo> => {
    let client = makeClient();
    return await getResponse(async () => {
        let response = await client.get(`users/test`);
        return response.data;
    })
};

type TransferParams = {
    target: string,
    sum: number
};

export const transferFunds = async (token: string, transferParams: TransferParams) : Promise<UserInfo> => {
    let client = makeClient();
    
    client.interceptors.request.use(config => {
        config.headers['Authorization'] = `Bearer ${token}`;
        return config;
    });
    
    return await getResponse(async () => {
        let response = await client.get(`users/transfer/${transferParams.target}/${transferParams.sum}`);
        return response.data;
    })
    
};
