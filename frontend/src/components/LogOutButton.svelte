<script lang="ts">
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';

  async function logout() {
    await fetch('/logout', {
      method: 'POST',
      credentials: 'include'
    });
    session.set({ user: null });
    goto('/login');
  }
</script>

<button on:click={logout}>
  Logout
</button>
<style>
  button {
    background-color: #f44336; /* Red */
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
  }

</style>