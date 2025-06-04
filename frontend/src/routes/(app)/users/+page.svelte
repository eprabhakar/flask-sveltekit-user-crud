<script lang="ts">
  import { onMount } from 'svelte';
  import { session } from '$lib/stores/session';
  import { goto } from '$app/navigation';

  let users: any[] = [];
  let error: string | null = null;
  $: isAdmin = $session.user?.role === 'admin';

  onMount(async () => {
    if (!isAdmin) {
      error = 'Access denied. Admins only.';
      return;
    }

    try {
      const res = await fetch('http://localhost:5000/users', {
        credentials: 'include'
      });
      if (!res.ok) {
        error = (await res.json()).error || 'Failed to load users';
      } else {
        users = await res.json();
      }
    } catch (err) {
      error = 'Network error';
    }
  });
</script>

{#if error}
  <p style="color: red">{error}</p>
{:else if isAdmin}
  <h2>All Users</h2>
  <ul>
    {#each users as user}
      <li>{user.username} – {user.email}</li>
    {/each}
  </ul>
{:else}
  <p>Checking role...</p>
{/if}
<style>
  h2 {
    color: #333;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    padding: 8px;
    border-bottom: 1px solid #ccc;
  }

  p {
    color: red;
  }
</style>