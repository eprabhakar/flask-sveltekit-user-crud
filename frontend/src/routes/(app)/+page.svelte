<!-- frontend/src/routes/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { session } from '$lib/stores/session';

  $: if ($session.user) {
    goto('/dashboard');
  } else {
    goto('/login');
  }

  let cards = Array.from({ length: 6 }, (_, i) => `Card ${i + 1}`);
</script>

<h2 class="text-2xl font-semibold mb-4">Main Content Area</h2>
<p class="text-gray-600">
  This is the content inside <code>+page.svelte</code>. The layout (navbar and sidebar) is shared.
</p>

<!-- Responsive Grid inside Main -->
<div class="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 mt-6">
  {#each cards as card}
    <div class="bg-gray-50 border rounded-xl p-4 shadow hover:shadow-md transition">
      <h3 class="font-bold text-lg text-blue-600">{card}</h3>
      <p class="text-gray-500 mt-2">Some content inside the card.</p>
    </div>
  {/each}
</div>

<p>Redirecting...</p>


