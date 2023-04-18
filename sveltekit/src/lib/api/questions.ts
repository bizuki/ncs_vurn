import { getResponse, makeClient } from './client'
import type { Question } from '../types/Questions'

export const fetchQuestionsList = async (page: string) : Promise<Question[]> => {
    let client = makeClient();
    
    return await getResponse(async () => {
        let response = await client.get(`questions/recent?page=${page}`);
        return response.data.items;
    });
};

export const createQuestion = async (text: string) : Promise<Question> => {
    let client = makeClient();
    
    return await getResponse(async () => {
        let response = await client.post(`questions`, {text: text});
        return response.data.items;
    });
};