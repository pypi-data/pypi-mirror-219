<script>
  let open = true;

  function toggleSidebar() {
    open = !open;
  }

  let activeLink = "Home";

  function setActiveLink(link) {
    activeLink = link;
  }
</script>

<aside class="sidemenu" style="width: {open ? '100%' : '40px'}">
  {#if open}
    <a
      href="/"
      class="sidebar-link {activeLink === 'Home' ? 'active' : ''}"
      on:click={() => setActiveLink("Home")}
      on:keypress={() => setActiveLink("Home")}>Home</a
    >

    <a
      href="/data"
      class="sidebar-link {activeLink === 'Data' ? 'active' : ''}"
      on:click={() => setActiveLink("Data")}
      on:keypress={() => setActiveLink("Data")}>Data</a
    >

    <a
      href="/embeddings"
      class="sidebar-link {activeLink === 'Embeddings' ? 'active' : ''}"
      on:click={() => setActiveLink("Embeddings")}
      on:keypress={() => setActiveLink("Embeddings")}>Embeddings</a
    >

    <a
      href="/chatbot"
      class="sidebar-link {activeLink === 'Chatbot' ? 'active' : ''}"
      on:click={() => setActiveLink("Chatbot")}
      on:keypress={() => setActiveLink("Chatbot")}>Chatbot</a
    >

    <a
      href="/feedback"
      class="sidebar-link {activeLink === 'Feedback' ? 'active' : ''}"
      on:click={() => setActiveLink("Feedback")}
      on:keypress={() => setActiveLink("Feedback")}>Feedback</a
    >
  {/if}
</aside>

<style>
  :root {
    --headerHeight: 60px; /* Adjust as necessary */
  }

  .sidemenu {
    padding: calc(var(--headerHeight) * 1.1) 10px;
    background-color: var(--white);
    min-height: 100vh;
    text-align: center;
    border-right: var(--line);
    transition: width 0.3s ease;
  }

  .sidemenu span a {
    text-decoration: none;
    color: black;
  }

  .sidemenu a.sidebar-link {
    display: block;
    text-align: left;
    padding: 15px;
    cursor: pointer;
    box-sizing: border-box;
    text-decoration: none;
    color: var(--black);
    margin: 2px;
  }

  .sidemenu a.sidebar-link:hover {
    background-color: var(--primary);
    margin: 2px;
  }

  .sidemenu a.sidebar-link.active {
    border-left: 4px solid var(--black);
    background-color: var(--primary);
    font-weight: bold;
  }
</style>
