<!-- src/lib/components/UserList.svelte -->
<script lang="ts">
  import "../../app.css";
  import { Search } from 'lucide-svelte';
  export let users: any[] = [];
  let filteredUsers: any[] = []; // Users filtered based on search
  let query = '';
  $: displayUsers = query.trim() ? filteredUsers : users;
  let showSearchForm = false;

  // Toggle search form visibility
  function toggleSearchForm() {
    showSearchForm = !showSearchForm;
    if(!showSearchForm) {
      query = ''; // Reset search query when closing the form
      filteredUsers = []; // Reset filtered users
    }
  }

    // Handle search form submission
  async function handleSearchSubmit() {
    handleSearchInput();
  }
  // Filter users based on search query
  function handleSearchInput() {
    const lowerQuery = query.toLowerCase();
    filteredUsers = users.filter(user =>
      user.username.toLowerCase().includes(lowerQuery) ||
      user.email.toLowerCase().includes(lowerQuery)
    );
    
  }
</script>

<main class="flex-1 overflow-auto ">
   <!-- Main Utility Card with Content -->
    <div class="w-full bg-white shadow-md overflow-hidden">
      <!-- Title and actions -->
      <div class="px-4 bg-white shadow-md border border-gray-200 border-collapse flex items-center justify-between">
        <!-- Title / Breadcrumb -->
        <div class="text-sm font-semibold text-gray-800">
          User >> List
        </div>

        <!-- Actions -->
        <div class="flex space-x-1 p-1">
          <button
            class="inline-flex items-center gap-2 bg-gray-100 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 transition" 
            on:click={toggleSearchForm}
            aria-label="Search"
          >
            <span class="flex items-center justify-center w-6 h-6 bg-white text-blue-600 rounded-full">
              <Search size="16" />
            </span>
            <span class="text-sm font-medium">Search</span>
          </button>
        </div>
      </div>
      
      {#if showSearchForm}
        <div class="mt-4 px-2">
          <form on:submit|preventDefault={handleSearchSubmit} class="w-full max-w-md mb-6 flex gap-2">
            <div class="relative flex-grow">
              <input 
                type="text" 
                bind:value={query} 
                placeholder="username or email" 
                class="text-sm px-2 py-1 border border-gray-200 w-full"
              />
            </div>
            <button
              type="submit"
              class="text-sm bg-gray-100 hover:bg-gray-300 text-black py-1 px-2"
            >
              Search
            </button>
          </form>
        </div>
      {/if}


      <!-- Main Content Below Header -->
      <div class="p-2  bg-white">
        <!-- You can replace this with your dynamic content -->
        <table class="min-w-full  border border-gray-200 border-collapse divide-y divide-gray-200">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 border border-gray-200 py-2 text-left text-sm font-semibold text-gray-700">Name</th>
              <th class="px-4 border border-gray-200 py-2 text-left text-sm font-semibold text-gray-700">Email</th>
              <th class="px-4 border border-gray-200 py-2 text-left text-sm font-semibold text-gray-700">Role</th>
              <th class="px-4 border border-gray-200 py-2 text-sm font-semibold text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white">
            {#each displayUsers as user}
              <tr class="hover:bg-gray-50">
                <td class="px-4 border border-gray-200 py-2 text-sm text-gray-900">{user.username}</td>
                <td class="px-4 border border-gray-200 py-2 text-sm text-gray-600">{user.email}</td>
                <td class="px-4 border border-gray-200 py-2 text-sm text-gray-600">{user.role}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
</main>
