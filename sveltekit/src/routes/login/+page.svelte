<script lang="ts">
	import { goto } from "$app/navigation";
    import Login from "$lib/components/Login.svelte";
	import Register from "$lib/components/Register.svelte";
	import { getToken } from "$lib/stores/token";
	import { Tabs, Tab, TabList, TabPanel } from 'svelte-tabs';
	import { onMount } from "svelte";
    
    onMount(async () => {
        let token = getToken();
        if (token) {
            await goto('/account')
        }
    })
</script>

<Tabs>
    <TabList>
        <Tab>Login</Tab>
        <Tab>Registration</Tab>
    </TabList>
    <TabPanel>
        <Login/>
    </TabPanel>

    <TabPanel>
        <Register/>
    </TabPanel>
</Tabs>

<style>
    :global(.svelte-tabs li.svelte-tabs__tab) {
        color: #53dfd3
    }

    :global(.svelte-tabs li.svelte-tabs__selected) {
        border-bottom: 2px solid #53dfd3;
    }
</style>