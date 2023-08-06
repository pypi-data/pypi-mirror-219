<script>
  import Header from "./Header.svelte";
  import Sidemenu from "./Sidemenu.svelte";
  import "./normalize.css";
  import "./styles.css";
  //   import "../app.css";
  export const ssr = false;
  export const csr = true;
  export const prerender = false;

  //   this is the main.js
  let open = true;

  function handleSidebarToggle(event) {
    open = event.detail;
  }
</script>

<div class="grid-sidemenu">
  <Header />
  <Sidemenu />

  <main class="layout">
    <slot />
  </main>

  <!-- <footer>
    <p>
      visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn SvelteKit
    </p>
  </footer> -->
</div>

<style>
</style>
