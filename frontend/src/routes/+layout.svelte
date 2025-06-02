<!-- src/routes/+layout.svelte -->
<script lang="ts">
  export let data;
  import { session } from '$lib/stores/session';
  import { onMount } from 'svelte';

  // Sync server-provided user into store
  onMount(() => {
    if (data?.user) {
      session.set({ user: data.user });
    }
  });
</script>

<slot />
