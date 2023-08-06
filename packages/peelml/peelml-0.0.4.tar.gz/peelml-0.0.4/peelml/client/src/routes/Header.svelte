<script>
  import logo from "$lib/images/logo.svg";
  import github from "$lib/images/github.svg";
</script>

<header>
  <div class="corner">
    <div class="logo-bg">
      <a href="https://www.cambioml.com">
        <img src={logo} alt="CambioML Logo" />
      </a>
    </div>
    <h1 class="logo">CambioML</h1>
  </div>
  <nav>
    <a href="/">Home</a>
    <a href="/data">data</a>
    <a href="/randomnumber">Rand</a>
    <a href="/uploadTest">test</a>
    <a href="/upload">upload</a>
    <a href="https://github.com/cambioml" target="_blank">
      <img src={github} alt="GitHub" />
    </a>
  </nav>
</header>

<style>
  .logo-bg {
    width: 2em;
    height: 2em;
    border-radius: 50%;
    background: var(--primary);
  }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .corner {
    display: flex;
    align-items: center;
  }

  img {
    width: 2em;
    height: 2em;
    object-fit: contain;
    vertical-align: middle; /* new style to align the image in the middle */
  }

  nav {
    display: flex;
    align-items: center;
  }

  a:hover {
    color: var(--color-theme-1);
  }
</style>
