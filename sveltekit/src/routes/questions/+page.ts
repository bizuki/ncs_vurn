import { fetchQuestionsList } from '$lib/api/questions.js';

export async function load({ }) {
    let questions = await fetchQuestionsList('1');

    return { questions };
}
