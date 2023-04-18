<script lang="ts">
	import { goto } from '$app/navigation';
	import { transferFunds } from '$lib/api/users';
	import { getToken } from '$lib/stores/token';
    import type { UserInfo } from '../types/Users';

    export let userInfo: UserInfo;
    export let test: boolean = false;

    async function submit(event: SubmitEvent) {
        let form = new FormData(event.target);

        await transferFunds(getToken(), { target: form.get('recepient'), sum: form.get('amount') });
        await goto('/account');
    };

</script>

<div>
    <h2>Transfer funds</h2>
    <div>
        <form on:submit|preventDefault={submit}>
            <div class='form-field'>
                <input type='string' id='recepient' name='recepient' placeholder="email of recepient" />
            </div>
            
            <div class='form-field'>
                <input type='number' id='amount' name='amount' placeholder="amount ot transfer"/>
            </div>
            
            <button disabled={test}>Send</button>
        </form>
    </div>
</div>
