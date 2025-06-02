<script lang="ts">
  import { goto } from '$app/navigation';

  let username = '', email = '', password = '', error = '';

  async function register() {
    error = '';
    const res = await fetch('http://localhost:5000/register', {
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

<form on:submit|preventDefault={register}>
  <input bind:value={username} placeholder="Username" required />
  <input type="email" bind:value={email} placeholder="Email" required />
  <input type="password" bind:value={password} placeholder="Password" required />
  <button type="submit">Register</button>
</form>

{#if error}
  <p style="color: red">{error}</p>
{/if}
<p>Already have an account? <a href="/login">Login here</a></p>