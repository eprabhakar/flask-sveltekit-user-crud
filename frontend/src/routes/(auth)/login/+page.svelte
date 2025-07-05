
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
    const res = await fetch('/api/login', {
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
      const err = await res.json();
      alert(err.error || "Username or password is incorrect"); 
    }
  }
</script>


<style lang="postcss">
  @reference "tailwindcss";
  :global(html) {
    background-color: theme(--color-gray-100);
  }
</style>

<div class="bg-white p-6 rounded-xl shadow-md w-full max-w-md">
  <h2 class="text-2xl font-bold text-center text-blue-600 mb-6">Login</h2>
  <form on:submit|preventDefault={login} class="space-y-4">
    <input
      type="text"
      bind:value={username}
      placeholder="Username"
      class="w-full px-4 py-2 border rounded-lg"
      required
    />
    <input
      type="password"
      bind:value={password}
      placeholder="Password"
      class="w-full px-4 py-2 border rounded-lg"
      required
    />
    <button
      type="submit"
      class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg"
    >
      Sign In
    </button>
  </form>
  <p>Don't have an account? <a href="/register" class="text-blue-600 hover:text-blue-800 underline" >Register</a></p>
  <p>Forgot your password? <a href="/reset-password" class="text-blue-600 hover:text-blue-800 underline">Reset</a></p>
</div>


