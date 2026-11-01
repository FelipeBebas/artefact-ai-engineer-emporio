/**
 * Empório da Música - Custom Client Script
 * Redireciona o clique no botão "Readme" do header para o repositório do projeto no GitHub.
 */
document.addEventListener("DOMContentLoaded", () => {
    const GITHUB_REPO_URL = "https://github.com/FelipeBebas/artefact-ai-engineer-emporio";

    // Intercepta cliques no botão de readme na fase de captura (antes da abertura do modal)
    document.addEventListener(
        "click",
        (event) => {
            const readmeBtn = event.target.closest("#readme-button");
            if (readmeBtn) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                window.open(GITHUB_REPO_URL, "_blank");
            }
        },
        true
    );
});
