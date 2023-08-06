from cubicweb_web.devtools.testlib import AutomaticWebTest


class AutomaticWebTest(AutomaticWebTest):
    def to_test_etypes(self):
        return {"File"}

    def list_startup_views(self):
        return ()


if __name__ == "__main__":
    from unittest import main

    main()
