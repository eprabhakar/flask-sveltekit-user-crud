<!-- src/routes/+layout.svelte -->
<script lang="ts">
  
  //let { children } = $props();
  const { children, data } = $props();
  //import "../app.css";  
  import { session } from '$lib/stores/session';
  import { onMount } from 'svelte';

  // Sync server-provided user into store
  onMount(() => {
    if (data?.user) {
      session.set({ user: data.user });
    }
  });
</script>

{@render children()}


