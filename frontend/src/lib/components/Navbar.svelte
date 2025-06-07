<script lang="ts">
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';
  export let user: { username: string;  avatar?: string };

  let showDropdown = false;

  function toggleDropdown() {
    showDropdown = !showDropdown;
  }

  function logout1() {
    // Navigate to logout route or call POST logout
    //window.location.href = '/logout';
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
  <div class="text-xl font-bold text-gray-800">Center for Distance Education</div> 

  <div class="relative">
    <button on:click={toggleDropdown} class="flex items-center gap-2 focus:outline-none">
      <img src={user.avatar || '/avatar.jpg'} alt="avatar" class="w-8 h-8 rounded-full border" />
      <span class="hidden md:block text-sm text-gray-700">{user.username}</span>
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
