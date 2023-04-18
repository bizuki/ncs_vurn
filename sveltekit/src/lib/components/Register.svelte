<script lang="ts">
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import { getToken, register } from "$lib/api/security";
    import type { AxiosError } from "axios";
	import { useForm, required, minLength, email, pattern } from "svelte-use-form";
	
	const form = useForm({
		email: { validators: [required, minLength(6), email]},
		password: { validators: [required, minLength(6), pattern('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])')]}
	});

    async function submit(event) {
        const formData = new FormData(event.target);
        
        await register(formData);

        formData.delete('first_name');
        formData.delete('last_name');

        let token = await getToken(formData);
        browser && localStorage.setItem('access_token', token.access_token);
        browser && localStorage.setItem('refresh_token', token.refresh_token);
        
        await goto('/account');
        
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

  <div class='form-field'>
    <input type='string' id='first_name' name='first_name' placeholder="first name"/>
  </div>

  <div class='form-field'>
    <input type='string' id='last_name' name='last_name' placeholder="last name"/>
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