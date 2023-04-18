import { browser } from "$app/environment";

export const getToken = (name: string = 'access_token') => {
    return browser && localStorage.getItem(name);
}