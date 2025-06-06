<!-- src/lib/components/UserList.svelte -->
<script lang="ts">
  import "../../app.css";
  export let users: any[] = [];
  //export let isAdmin: boolean = false;
  //export let onDelete: (id: number) => void = () => {};
</script>

<h2 class="text-xl font-semibold text-gray-800">User List</h2>
  <div class="overflow-x-auto rounded-lg shadow-md border border-gray-200 bg-white p-4">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-100">
        <tr>
          <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Name</th>
          <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Email</th>
          <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Role</th>
          <th class="px-4 py-2 text-sm font-semibold text-gray-700">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        {#each users as user}
          <tr class="hover:bg-gray-50">
            <td class="px-4 py-2 text-sm text-gray-900">{user.username}</td>
            <td class="px-4 py-2 text-sm text-gray-600">{user.email}</td>
            <td class="px-4 py-2 text-sm text-gray-600">{user.role}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

