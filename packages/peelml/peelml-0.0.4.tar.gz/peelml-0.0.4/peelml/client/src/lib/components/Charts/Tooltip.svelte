<script>
  export let content = {};
  export let x = 0;
  export let y = 0;
</script>

<div class="tooltip" style={`left: ${x}px; top: ${y}px`}>
  <p>
    {content.file}
    <br />
    {content.size}
  </p>
</div>

<style>
  .tooltip {
    position: absolute;
    background-color: white;
    border: 2px solid black;
    padding: 4px 5px;
    pointer-events: none;
    opacity: 0.95;
    transition: 0.5s;
  }
</style>
