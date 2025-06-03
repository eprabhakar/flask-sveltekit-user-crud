<!-- src/lib/components/UserList.svelte -->
<script lang="ts">
  export let users: any[] = [];
  //export let isAdmin: boolean = false;
  //export let onDelete: (id: number) => void = () => {};
</script>

<ul>
  {#each users as u}
    <li>
      {u.username} - {u.email} ({u.role})
    </li>
  {/each}
</ul>
