from collections import defaultdict

from markdown.extensions.toc import slugify
import mkdocs

class CisoControlsPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("root_url", mkdocs.config.config_options.Type(str, default="/controls/")),
        ("control_sources", mkdocs.config.config_options.Type(list, default=[])),
    )

    def on_config(self, config):
         self.tags = defaultdict(list)
         self.root_url = self.config.get('root_url')
         self.control_sources = self.config.get('control_sources')

    def on_pre_build(*args, **kwargs):
        return

    def on_nav(*args, **kwargs):
        return

    def on_page_markdown(self, markdown, page, config, files):
        # TODO: Render tag index
        # Add page to tags index
        for tag in page.meta.get("tags", []):
            self.tags[tag].append(page)

    def on_page_context(self, context, page, config, nav):
        # Inject tags into page (after search and before minification)
        if "tags" in page.meta:
            context["tags"] = [
                self._render_tag(tag)
                    for tag in page.meta["tags"]
            ]
            print(context["tags"])

    # Render the given tag, linking to the tags index (if enabled)
    def _render_tag(self, tag):
        url = None
        for control_source in self.control_sources:
            if tag.startswith(control_source):
                url = self.root_url + \
                    slugify(control_source, '-') + "#" + \
                    slugify(tag, '-')
        if not url:
            raise Exception("Unrecognized control source")
        return dict(name = tag, type = type, url = url)
