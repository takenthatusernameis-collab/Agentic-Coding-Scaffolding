"""Tests for nntplib_utils."""

import nntplib_utils


def test_exports():
    for name in ["NNTP", "NNTP_SSL", "GroupInfo", "ArticleInfo", "create_nntp",
                 "create_nntp_ssl", "is_available"]:
        assert hasattr(nntplib_utils, name)
