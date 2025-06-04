<!-- This overrides the main layout -->
<script>
  //export let data;
  import "../../../app.css";
</script>

<!-- Full-screen login layout with no inherited nav/sidebar -->
<main class="min-h-screen flex items-center justify-center bg-gray-100">
  <slot />
</main>
