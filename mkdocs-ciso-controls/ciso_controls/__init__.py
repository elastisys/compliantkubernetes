# Inspired by:
# - https://github.com/squidfunk/mkdocs-material/tree/8.2.16/material/plugins/tags
# - https://github.com/aklajnert/mkdocs-simple-hooks/blob/v0.1.5/mkdocs_simple_hooks/__init__.py

from collections import defaultdict
import logging
import os
import sys

from markdown.extensions.toc import slugify
import mkdocs
from natsort import natsorted

class CisoControlsPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("root_url", mkdocs.config.config_options.Type(str, default="controls/")),
    )

    def on_config(self, config):
        self.tags = { } # shape: Dict[tags_index, Dict[tag, list of pages]]
        self.root_url = self.config.get('root_url')

        # mkdocs-material will only show tags on pages if its own built-in tags
        # plugin is enabled. Trick the partials/content.html template into
        # believing that.
        config["plugins"]["material/tags"] = None

    # Move tags indexes to the end to ensure we first collect all page tags
    def on_nav(self, nav, config, files):
        tags_indexes = []
        for filename, file in files.src_paths.items():
            if file.url.startswith(self.root_url):
                tags_indexes.append(file)
        for file in tags_indexes:
            files.remove(file)
            files.append(file)
            tags_index = file.name
            self.tags[tags_index] = defaultdict(list)
            log.info(f'Found tags index URL: {file.url}')

    def on_page_markdown(self, markdown, page, config, files):
        if page.url.startswith(self.root_url):
            log.info(f"Rendering tags index: {page.file.url}")
            return self.__render_tag_index(markdown, page)

        # Add page to tags index
        for tag in page.meta.get("tags", []):
            tags_index = self._tag_to_tags_index(tag)
            self.tags[tags_index][tag].append(page)

    def on_page_context(self, context, page, config, nav):
        # Inject tags into page (after search and before minification)
        if "tags" in page.meta:
            context["tags"] = [
                self._render_tag(tag)
                    for tag in page.meta["tags"]
            ]

    # Our slugify
    def slugify(self, name):
        return slugify(name, '-')

    # Map a tag to a tags index
    def _tag_to_tags_index(self, tag):
        slugified_tag = self.slugify(tag)
        for tags_index in self.tags.keys():
            if slugified_tag.startswith(tags_index):
                return tags_index
        log.info(
            'Collected the following tags indexes: ' +
            ' '.join(self.tags.keys()))
        log.error(f'No tags index for tag: {tag}')
        sys.exit()

    # Render tags index
    def __render_tag_index(self, markdown, page):
        if not "[TAGS]" in markdown:
            markdown += "\n[TAGS]"

        tags_index = page.file.name
        tags = self.tags[tags_index]

        # Replace placeholder in Markdown with rendered tags index
        return markdown.replace("[TAGS]", "\n".join([
            self.__render_tag_links(*args, self_page=page)
                for args in natsorted(tags.items())
        ]))

    # Render the given tag and links to all pages with occurrences
    def __render_tag_links(self, tag, pages, self_page):
        content = [f"## <span class=\"md-tag\">{tag}</span>", ""]
        for page in pages:
            url = mkdocs.utils.get_relative_url(
                page.file.src_path.replace(os.path.sep, "/"),
                self_page.file.src_path.replace(os.path.sep, "/")
            )

            # Ensure forward slashes, as we have to use the path of the source
            # file which contains the operating system's path separator.
            content.append("- [{}]({})".format(
                page.meta.get("title", page.title),
                url
            ))

        # Return rendered tag links
        return "\n".join(content)

    # Render the given tag, linking to the tags index
    def _render_tag(self, tag):
        tags_index = self._tag_to_tags_index(tag)
        url = self.root_url + \
            self.slugify(tags_index) + "#" + \
            self.slugify(tag)
        return dict(name = tag, type = type, url = url)

# Set up logging
log = logging.getLogger("mkdocs")
log.addFilter(mkdocs.commands.build.DuplicateFilter())
