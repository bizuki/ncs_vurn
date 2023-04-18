<script lang="ts">
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import { getToken } from "$lib/api/security";
	import { AxiosError } from "axios";
	import { useForm, required, minLength, email, pattern } from "svelte-use-form";
	
	const form = useForm({
		email: { validators: [required, minLength(6), email]},
		password: { validators: [required, minLength(6), pattern('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])')]}
	});

    async function submit(event) {
        const formData = new FormData(event.target);
        try {

            let token = await getToken(formData);
            browser && localStorage.setItem('access_token', token.access_token);
            browser && localStorage.setItem('refresh_token', token.refresh_token);
            await goto('/account')
        } catch (exc) {
            if (exc instanceof AxiosError) {
                error = exc;
                alert('Invalid credentials')
            }
        }
        error = undefined;
        
    };

    let error: AxiosError | undefined = undefined;
	
</script>

<form use:form on:submit|preventDefault={submit}>
  <div class='form-field'>
    <input type='username' id='username' name='username' placeholder="email" />
  </div>
  
  <div class='form-field'>
    <input type='password' id='password' name='password' placeholder="password"/>
  </div>

  <button disabled={!$form.valid}>Save</button>
  
</form>

<style>
	.form-field {
        flex:content;
        flex-direction: column;
		margin-bottom: 10px;
	}
	
	input:invalid {
		border: 1px solid red;
	}
	
</style>