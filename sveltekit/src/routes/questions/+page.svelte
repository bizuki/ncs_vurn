<script lang="ts">
	import { goto } from '$app/navigation';
	import { createQuestion, fetchQuestionsList } from '$lib/api/questions.js';

    export let data;

    $: ({questions} = data);

    async function submit(event: SubmitEvent) {
        let form = new FormData(event.target);

        await createQuestion(form.get('text')!);
        
        questions = await fetchQuestionsList('1');
        await goto('/questions');
        return false;
    };


</script>

<svelte:head>
  <title>Questions</title>
</svelte:head>

<h1>Ask your question</h1>

<form on:submit={submit}>
    <div class='form-field'>
        <input type='string' id='text' name='text' placeholder="your question" />
    </div>
    
    <button>Send</button>
</form>

<h1>Recently asked questions</h1>

{#each questions as {text}}
    <div>{text}</div>
{/each}

