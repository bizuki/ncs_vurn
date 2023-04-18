<script lang="ts">
    type FooterItem = {
        href: string;
        alt: string;
        src: string;
    };

    export let items: FooterItem[];
</script>

<footer>
    <hr>
    <div class="contacts">
      {#each items as footerItem}
        <a href={footerItem.href}><img src={footerItem.src} alt={footerItem.alt}></a>
      {/each}
    </div>
</footer>

<style>
    
    .contacts {
      text-align: center;
    }
  
</style>
