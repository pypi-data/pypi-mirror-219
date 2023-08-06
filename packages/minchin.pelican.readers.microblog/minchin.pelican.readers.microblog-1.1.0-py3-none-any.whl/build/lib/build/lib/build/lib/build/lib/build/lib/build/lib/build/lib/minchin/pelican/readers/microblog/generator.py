import datetime
import re
import logging

from pelican import signals
from pelican.contents import Article
from pelican.readers import BaseReader
from pelican.utils import get_date, pelican_open
from pelican.readers import MarkdownReader

from .constants import (
    LOG_PREFIX,
)


def addMicroArticle(articleGenerator):
    settings = articleGenerator.settings

    # Author, category, and tags are objects, not strings, so they need to
    # be handled using BaseReader's process_metadata() function.
    baseReader = BaseReader(settings)

    file_extensions = [
        "txt",
    ] + MarkdownReader.file_extensions

    micropost_count = 0

    for post in articleGenerator.get_files(
        paths=settings["MICROBLOG_FOLDER"], extensions=file_extensions
    ):
        # raw_content = pelican_open(post)

        content, metadata = MarkdownReader.read(post)

        post_date = metadata["date"]
        post_slug = settings["MICROBLOG_SLUG"] % metadata
        post_save_as = settings["MICROBLOG_SLUG"] % metadata
        post_url = settings["MICROBLOG_SLUG"] % metadata

        # warn if too long
        post_len = len(content)
        if post_len > settings["MICROBLOG_MAX_LENGTH"] + 6:
            logging.warning(
                "%s micropost %s longer than expected (%s > %s)"
                % (LOG_PREFIX, post, post_len - 6, settings["MICROBLOG_MAX_LENGTH"])
            )

        newArticle = Article(
            content,
            {
                "title": None,
                "date": post_date,
                "category": baseReader.process_metadata("category", "micro"),
                # "tags": baseReader.process_metadata("tags", "tagA, tagB"),
                "micro": baseReader.process_metadata("micro", True),
                "slug": baseReader.process_metadata("slug", post_slug),
                "save_as": baseReader.process_metadata("save_as", post_save_as),
                "url": baseReader.process_metadata("url", post_url),
            },
        )

        articleGenerator.articles.insert(0, newArticle)
        micropost_count += 1

        # logging.debug(
        #     '%s MICROBLOG_FOLDER set to "%s"'
        #     % (LOG_PREFIX, pelican.settings["MICROBLOG_FOLDER"])
        # )
    
    logging.info('%s %s microposts added!' % (LOG_PREFIX, micropost_count))
