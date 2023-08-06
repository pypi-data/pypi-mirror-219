<script>
  let rand = -1;

  console.log("hthth");

  function getRand() {
    fetch("./rand")
      .then((d) => d.text())
      .then((d) => (rand = d));
  }
</script>

<svelte:head>
  <title>Rand</title>
  <meta name="description" content="About this app" />
</svelte:head>

<h1>Your number is {rand}!</h1>
<button on:click={getRand}>Get a random number</button>
