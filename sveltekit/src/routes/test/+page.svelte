<script lang="ts">
  import Transfer from "$lib/components/Transfer.svelte";
import UserInformation from "$lib/components/UserInformation.svelte";

  export let data;

  $: ({userInfo} = data);

</script>

<svelte:head>
  <title>Test account</title>
</svelte:head>

<h1>Test account</h1>
You can't actually transfer funds from test account
<div class="user-page">
    <UserInformation userInfo={userInfo}/>
    <Transfer userInfo={userInfo} test={true}/>
</div>

<style>
  .user-page {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    margin: 10px;
  }
</style>