<script lang="ts">
    import type { UserInfo } from '../types/Users';

    export let userInfo: UserInfo;

</script>

<div class="user-info">
    <div>
        <h2>Account info</h2>
        <ul>
            <li>Name: {userInfo.first_name} {userInfo.last_name}</li>
            <li>Email: {userInfo.email}</li>
            {#if userInfo.balance != undefined}
            <li>Current balance: {userInfo.balance}</li>
            {/if}
        </ul>
    </div>
</div>

<style>

    .user-info {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

</style>
