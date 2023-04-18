import { browser } from '$app/environment';
import axios from 'axios';

export const makeClient = () => axios.create({
    baseURL: browser ? 'http://localhost:8080/api/' : 'http://fastapi:8080/api/',
    timeout: 1000
});

export const getResponse = async (func) => {
    try {
        return await func();
    } catch (error) {
        const { response } = error;
        if (response.data.context) {
            alert(response.data.context?.message);
        } else {
            alert('Something went wrong during request');
        }
    }
}