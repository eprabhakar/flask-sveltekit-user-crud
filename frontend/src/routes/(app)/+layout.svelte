
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
  <div class="flex min-h-screen font-poppins text-gray-800 bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-md hidden md:block">
      <div class="p-4 bg-gray-600 border-b border-gray-600 text-white">
        <h1 class="text-sm  tracking-wide">Admission Management</h1>
      </div>
      <div class="bg-gray-100 text-gray-800 h-full">
        <nav class="divide-y divide-gray-200">
          {#each menuItems as item}
            <button
              onclick={() => handleMenuClick(item)}
              class="p-4 block w-full pl-10 pr-6 py-2 text-left text-sm
                 hover:bg-gray-600 transition-all duration-150
                {($page.url.pathname === item.href) 
                  ? 'bg-gray-400 tracking-wide font-semibold text-white' 
                  : 'text-gray-500'}"
              >
              {item.name}
            </button>
          {/each}
        </nav>
      </div>
    </aside>

    <!-- Sidebar 
    <Sidebar class="w-64 bg-gray-100 border-r p-4 hidden md:block" style="min-height: 100vh;" >
 
      {#each menuItems as item}
        <SidebarItem onclick={() => handleMenuClick(item)} class="cursor-pointer">
          <span>{item.icon}</span>  
          <span class="ml-2">{item.name}</span>
        </SidebarItem>
      {/each}
    </Sidebar> -->

    <!-- Page content goes here -->
    <section class="flex-1 overflow-auto bg-gray-100 p-6">
      <div class="max-w-5xl mx-auto bg-white  shadow-md p-6">
        {@render children()}<!-- <slot />  This renders the content from +page.svelte -->
      </div>
    </section>
  </div>
</main>

<!-- {@render children()} -->


