
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import "../../app.css";
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
  let menu = ["Dashboard", "Profile", "Settings", "Logout"];
</script>

<main class="min-h-screen flex flex-col">
  <!-- Top Navbar -->
  <header class="bg-blue-600 text-white p-4 shadow-md">
    <h1 class="text-xl font-bold">Acharya Nagarjuna University</h1>
  </header>

  <!-- Main Layout: Sidebar + Content -->
  <div class="flex flex-1">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-100 border-r p-4 hidden md:block">
      <nav class="space-y-2">
        {#each menu as item}
          <a
            href={`/${item.toLowerCase()}`}
            class="block px-4 py-2 rounded hover:bg-blue-100 text-gray-700 font-medium"
            >{item}
          </a>
        {/each}
      </nav>
    </aside>

    <!-- Page content goes here -->
    <section class="flex-1 p-6 bg-white">
      {@render children()}<!-- <slot />  This renders the content from +page.svelte -->
    </section>
  </div>
</main>

<!-- {@render children()} -->


