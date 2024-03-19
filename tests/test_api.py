# -*- coding: utf-8 -*-

from prompt_catalog import api


def test():
    _ = api


if __name__ == "__main__":
    from prompt_catalog.tests import run_cov_test

    run_cov_test(__file__, "prompt_catalog.api", preview=False)
