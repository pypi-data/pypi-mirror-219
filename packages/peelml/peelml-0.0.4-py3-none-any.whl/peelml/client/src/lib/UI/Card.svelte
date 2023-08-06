<script>
    export let title;
    export let buttonText;
    export let text;
    export let link;
  </script>
  
  <div class="card">
    <h5>{title}</h5>
    <p>{text}</p>
    <a href={link}>
      <button>{buttonText}</button>
    </a>
  </div>
  