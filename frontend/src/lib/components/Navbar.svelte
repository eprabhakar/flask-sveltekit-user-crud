<script lang="ts">
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';
  import { Badge, Navbar, Button, Dropdown, DropdownItem } from 'flowbite-svelte';
  import { ChevronDownOutline } from "flowbite-svelte-icons";
  import UserList from './UserList.svelte';
  
  export let user: { username: string;  avatar?: string };

  let showDropdown = false;

  function toggleDropdown() {
    showDropdown = !showDropdown;
  }
  

  function handleExternalLink(url:string) {
    const confirmLeave = confirm(`You are about to leave this site and go to:\n\n${url}\n\nDo you want to continue?`);
    if (confirmLeave) {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  }

  async function logout() {
    console.log('Logging out...');
    await fetch('http://localhost:5000/logout', {
      method: 'POST',
      credentials: 'include'
    });
    session.set({ user: null });
    goto('/login');
  }
</script>

<nav class="flex items-center justify-between px-6 py-3 bg-white rounded-1g shadow-md">
  <!-- div class="text-xl font-bold text-gray-800">Center for Distance Education</div --> 
  <div class="flex items-center space-x-3">
    <img src="/logo.jpg" alt="Logo" class="h-16 w-16 object-contain" />
    <div class="flex flex-col leading-tight">
      <span class="text-base font-semibold font-poppins text-blue-600">ACHARYA NAGARJUNA UNIVERSITY -CDE</span>
      <span class="text-xs text-black-500">Nagarjuna Nagar, Guntur - 522 510</span>
      <span class="text-xs text-black-500">Andhra Pradesh, India    
        <a 
          target="_blank" 
          rel="noopener noreferrer" 
          on:click|preventDefault={() => handleExternalLink('https://www.nagarjunauniversity.ac.in/')}
          href='https://www.nagarjunauniversity.ac.in/' 
          class="text-blue-600 underline hover:text-blue-800">website
        </a>
      </span>
    </div>
  </div>

  <div class="relative">
    <button on:click={toggleDropdown} class="flex items-center gap-2 focus:outline-none">
      <img src={user.avatar || '/avatar.jpg'} alt="avatar" class="w-8 h-8 rounded-full border" />
      <span class="hidden md:block text-sm text-gray-700"><Badge color="gray">{user.username}</Badge></span>
      <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    {#if showDropdown}
      <div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow z-50">
        <a href="/profile" class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-100">Profile</a>
        <a href="/settings" class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-100">Settings</a>
        <hr />
        <button on:click={logout} class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100">Logout</button>
      </div>
    {/if}
  </div>
</nav>
<!-- Navbar class="bg-white border-b px-4">
  <div class="flex items-center justify-between w-full">
    <a href="/" class="text-xl font-semibold text-gray-800">MyApp</a>
    <Button>Drop</Button>
    <Dropdown simple>
     
      <DropdownItem href="/profile">Profile</DropdownItem>
      <DropdownItem href="/settings">Settings</DropdownItem>
      <DropdownItem onclick={logout} class="w-full text-left block px-4 py-2 hover:bg-gray-100">Log out</DropdownItem>
    </Dropdown>
  </div>
</Navbar -->