<script>
  let rand = -1;

  console.log("hthth");

  function getRand() {
    fetch("./api/rand")
      .then((d) => d.text())
      .then((d) => (rand = d));
  }
</script>

<svelte:head>
  <title>About</title>
  <meta name="description" content="About this app" />
</svelte:head>

<div>
  <h1>About this app</h1>

  <h1>Your number is {rand}!</h1>
  <button on:click={getRand}>Get a random number</button>

  <p>
    This is a <a href="https://kit.svelte.dev">SvelteKit</a> app. You can make your
    own by typing the following into your command line and following the prompts:
  </p>

  <pre>npm create svelte@latest</pre>

  <p>
    The page you're looking at is purely static HTML, with no client-side
    interactivity needed. Because of that, we don't need to load any JavaScript.
    Try viewing the page's source, or opening the devtools network panel and
    reloading.
  </p>
</div>
