
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import "../../app.css";
  //let { children } = $props();
  const { children, data } = $props();
  //import "../app.css";  
  import { Sidebar, SidebarItem } from 'flowbite-svelte';
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';
  import Navbar from '$lib/components/Navbar.svelte';
  import { derived}  from 'svelte/store';

  import { page }  from '$app/stores';
  // ...other imports and code...
  const currentPath = derived(page, ($page)=>($page.url.pathname));


  import { onMount } from 'svelte';

  // Sync server-provided user into store
  onMount(() => {
    if (data?.user) {
      session.set({ user: data.user });
    }
  });

  async function logout() {
    console.log('Logging out...');
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
    console.log('Menu item clicked:', item.name + ' - href:', item.href, ' - action:', item.action);
    if (item.type === 'logout') {
      logout();
    } else if (item.href) {
      goto(item.href);
    }
  }
  
</script>

<main class="min-h-screen flex flex-col">
  <!-- Top Navbar -->

    {#if data?.user} 
      <Navbar user={data.user} />
    {/if}



  <!-- Main Layout: Sidebar + Content -->
  <div class="flex min-h-screen font-poppins bg-gray-100">
    <!-- Sidebar -->
    <aside class="text-white  w-64 min-h-screen">
      <div class="p-2 bg-gray-600  border-b border-gray-600 text-white">
        <h1 class="text-sm  tracking-wide">Admission Management</h1>
      </div>
      <div class="h-full">
        <nav class=" shadow-lg divide-gray-200">
          {#each menuItems as item}
            <button
              onclick={() => handleMenuClick(item)}
              class="p-4 block w-full pl-10 pr-6 py-2 text-gray text-left text-sm
                 hover:bg-gray-600 transition-all duration-150
                {($page.url.pathname === item.href) 
                  ? 'bg-gray-400 tracking-wide text-gray' 
                  : 'text-gray-500'}"
              >
              {item.name}
            </button>
          {/each}
        </nav>
      </div>
    </aside>

    <section class="flex-1 overflow-auto bg-gray-100 p-4">
      <div class=" bg-white  shadow-md ">
        {@render children()}<!-- <slot />  This renders the content from +page.svelte -->
      </div>
    </section>
  </div>
</main>

<!-- {@render children()} -->


