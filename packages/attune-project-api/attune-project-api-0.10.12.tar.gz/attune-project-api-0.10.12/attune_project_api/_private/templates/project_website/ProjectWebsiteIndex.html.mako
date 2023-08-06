<%page args="projectMetadata, blueprints"/>
<!doctype html>
<html lang="en">
<%include
    file="ProjectWebsiteIndexHead.html.mako"
    args="projectMetadata=projectMetadata"/>
<body>

<!-- Project breadcrumbs -->
<%include
    file="ProjectWebsiteIndexBreadcrumbs.html.mako"
    args="projectMetadata=projectMetadata"/>

<!-- Project Header -->
<%include
    file="ProjectWebsiteIndexHeader.html.mako"
    args="projectMetadata=projectMetadata"/>

<div class="documentation">
    <div class="container px-0">
        <div class="row">
            <!-- Documentation and Instruction Sets -->
<%include
    file="ProjectWebsiteIndexBlueprintsList.html.mako"
    args="blueprints=blueprints"/>
<%include
    file="ProjectWebsiteIndexAttuneAd.html.mako"/>
        </div>
<%include
    file="ProjectWebsiteIndexJoinDiscord.html.mako"/>
    </div>
</div>
<%include
    file="ProjectWebsiteIndexScripts.html.mako"/>
</body>
</html>
