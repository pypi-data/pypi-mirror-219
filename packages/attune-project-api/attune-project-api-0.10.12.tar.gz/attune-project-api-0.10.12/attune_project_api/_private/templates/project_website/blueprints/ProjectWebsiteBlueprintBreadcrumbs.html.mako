<%page args="projectMetadata, blueprint"/>
<!-- Project breadcrumbs -->
<nav aria-label="breadcrumb">
    <ol class="breadcrumb m-0">
        <li class="breadcrumb-item" aria-current="page">
            <a
                href="https://www.servertribe.com/"
                target="_blank">
                ServerTribe
            </a>
        </li>
        <li class="breadcrumb-item" aria-current="page">
            <a
                href="https://github.com/attune-Automation/"
                target="_blank">
                Attune Automation Projects
            </a>
        </li>
        <li class="breadcrumb-item">
            <a href="index.html">
            ${projectMetadata.name}
            </a>
        </li>
        <li class="breadcrumb-item active" aria-current="page">
            <strong>${blueprint.name}</strong>
        </li>
    </ol>
</nav>