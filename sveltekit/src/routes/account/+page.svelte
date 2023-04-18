<script lang="ts">
	import Transfer from "$lib/components/Transfer.svelte";
  import UserInformation from "$lib/components/UserInformation.svelte";

  export let data;

  $: ({userInfo} = data);

</script>

<svelte:head>
  <title>Account</title>
</svelte:head>

<h1>Your personal account</h1>
<div class="user-page">
  <UserInformation userInfo={userInfo}/>
  <Transfer userInfo={userInfo}/>
</div>

<style>
  .user-page {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    margin: 10px;
  }
</style>