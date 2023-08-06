<script>
  export let showModal = false;
  let isInteresting = false;
</script>

{#if showModal}
  <div class="backdrop" class:interesting={isInteresting} on:click|self>
    <div class="modal">
      <slot />
    </div>
  </div>
{/if}
