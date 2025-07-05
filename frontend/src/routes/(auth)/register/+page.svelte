<script lang="ts">
  import { goto } from '$app/navigation';

  let username = '', email = '', password = '', error = '';

  async function register() {
    error = '';
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, email, password })
    });

    if (res.ok) {
      goto('/login?registered=true');
    } else {
      const data = await res.json();
      error = data?.error || 'Registration failed';
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
  <h2 class="text-2xl font-bold text-center text-blue-600 mb-6">Register</h2>
  <form on:submit|preventDefault={register} class="space-y-4">
    <input 
      bind:value={username} 
      placeholder="Username" 
      class="w-full px-4 py-2 border rounded-lg"
      required 
    />
    <input 
      type="email" bind:value={email} 
      placeholder="Email" 
      class="w-full px-4 py-2 border rounded-lg"
      required 
    />
    <input 
      type="password" bind:value={password} 
      placeholder="Password" 
      class="w-full px-4 py-2 border rounded-lg"
      required 
    />
    <button 
      type="submit"
      class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg"
    >
      Register
    </button>
  </form>

  {#if error}
    <p style="color: red">{error}</p>
  {/if}
  <p>Already have an account? <a href="/login" class="text-blue-600 hover:text-blue-800 underline">Login here</a></p>
</div>
