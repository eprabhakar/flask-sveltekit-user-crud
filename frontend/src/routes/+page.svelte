<!-- frontend/src/routes/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';

  $: if ($session.user) {
    goto('/dashboard');
  } else {
    goto('/login');
  }
</script> 

<p>Redirecting...</p>
