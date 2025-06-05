
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import "../../app.css";
  //let { children } = $props();
  const { children, data } = $props();
  //import "../app.css";  
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';
  import { onMount } from 'svelte';

  // Sync server-provided user into store
  onMount(() => {
    if (data?.user) {
      session.set({ user: data.user });
    }
  });

  async function logout() {
    await fetch('http://localhost:5000/logout', {
      method: 'POST',
      credentials: 'include'
    });
    session.set({ user: null });
    goto('/login');
  }
  
  const menuItems = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Profile', href: '/profile' },
    { name: 'Settings', href: '/settings' },
    { name: 'Logout', action: logout, type: 'logout' }
  ];

  function handleMenuClick(item: any) {
    if (item.type === 'logout') {
      logout();
    } else if (item.href) {
      goto(item.href);
    }
  }
  //let menu = ["Dashboard", "Profile", "Settings", "Logout"];
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
        {#each menuItems as item}
          <button
            onclick={() => handleMenuClick(item)}
            class="block w-full text-left px-3 py-2 rounded hover:bg-gray-500 transition"
          >
            {item.name}
          </button>
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


