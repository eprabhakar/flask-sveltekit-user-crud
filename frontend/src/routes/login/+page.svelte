
<script lang="ts">
  import { page } from '$app/state';
  import { session } from '$lib/stores/session';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  let username = '', password = '', error = '', success = '';

  $: {
    const params = page.url.searchParams;
    if (params.get('registered') === 'true') {
      success = 'Registration successful. You can now log in.';
    }
  }

  async function login() {
    error = '';
    const res = await fetch('http://localhost:5000/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (res.ok) {
      const user = await res.json();
      session.set({ user });
      goto('/dashboard');
    } else {
      error = 'Invalid login';
    }
  }
</script>

<h1 class="text-3xl font-bold underline">
  UMS - CDE ANU
</h1>
<style lang="postcss">
  @reference "tailwindcss";
  :global(html) {
    background-color: theme(--color-gray-100);
  }
</style>

<form on:submit|preventDefault={login}>
  <input bind:value={username} placeholder="Username" required />
  <input type="password" bind:value={password} placeholder="Password" required />
  <button type="submit">Login</button>
</form>

{#if success}
  <p style="color: green">{success}</p>
{/if}

{#if error}
  <p style="color: red">{error}</p>
{/if}

<p>Don't have an account? <a href="/register">Register here</a></p>
<p>Forgot your password? <a href="/reset-password">Reset it here</a></p>