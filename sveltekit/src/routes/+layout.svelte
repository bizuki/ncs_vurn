<script>
    import "../styles.css";

    import Navbar from "$lib/components/Navbar.svelte";
    import { base } from "$app/paths";
    
    import Footer from "$lib/components/Footer.svelte";
    
    import telegramLogo from "$lib/assets/telegram.svg";
    import mailLogo from "$lib/assets/mail.png";
    import githubLogo from "$lib/assets/github.svg";
</script>

<div class="container">
    <Navbar items={[
        {href: `${base}/`, title: "Home"},
        {href: `${base}/questions`, title: "Questions"},
        {href: `${base}/account`, title: "User account"}
    ]}/>

    <main>
        <slot/>
    </main>

    <Footer items={[
        {href: "https://t.me/Bizuki", alt: "telegram", src: telegramLogo},
        {href: "https://github.com/bizuki", alt: "github", src: githubLogo},
        {href: "mailto:dollar.daler@gmail.com", alt: "email", src: mailLogo},
    ]}/>

</div>
