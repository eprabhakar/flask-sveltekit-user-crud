<!-- src/lib/components/UserList.svelte -->
<script lang="ts">
  import "../../app.css";
  export let users: any[] = [];
  //export let isAdmin: boolean = false;
  //export let onDelete: (id: number) => void = () => {};
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
          <input
            type="text"
            placeholder="Search"
            class="text-sm px-4 py-2 bg-gray-100 border-gray-300  focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

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
            {#each users as user}
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
