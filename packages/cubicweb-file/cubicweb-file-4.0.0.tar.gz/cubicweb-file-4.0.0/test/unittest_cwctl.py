from cubicweb import Binary
from cubicweb.cwconfig import CubicWebConfiguration

from cubicweb_file.ccplugin import FileRefreshHashCommand
from cubicweb_web.devtools.testlib import WebCWTC, WebApptestConfiguration


class FileRefreshCommandTC(WebCWTC):
    def setUp(self):
        super().setUp()
        self.orig_config_for = CubicWebConfiguration.config_for

        def config_for(appid):
            return WebApptestConfiguration(appid, __file__)

        CubicWebConfiguration.config_for = staticmethod(config_for)

    def tearDown(self):
        CubicWebConfiguration.config_for = self.orig_config_for
        super().tearDown()

    def test_refresh(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.vreg.config["compute-hash"] = 0
            for i in range(10):
                fobj = cnx.create_entity(
                    "File",
                    data_name="foo%d.txt" % i,
                    data_format="text/plain",
                    data=Binary(b"xxx"),
                )
                self.assertEqual(None, fobj.data_hash)
            for i in range(10):
                fobj = cnx.create_entity(
                    "MyFile",
                    data_name=f"foo{i}.png",
                    data_format="image/png",
                    data=Binary(b"xxx"),
                )
                self.assertEqual(None, fobj.data_hash)
            cnx.commit()
        FileRefreshHashCommand(None).run([self.appid])
        with self.admin_access.repo_cnx() as cnx:
            self.assertFalse(
                cnx.execute(
                    "Any X WHERE X is_instance_of File, " "NOT X data_hash NULL"
                )
            )

        cmd = FileRefreshHashCommand(None)
        cmd.config.force = True
        cmd.run([self.appid])
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(
                10,
                len(
                    cnx.execute(
                        "Any X WHERE X is_instance_of File, "
                        'X data_hash LIKE "{sha256}%"'
                    )
                ),
            )

        cmd.config.subclasses = True
        cmd.run([self.appid])
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(
                20,
                len(
                    cnx.execute(
                        "Any X WHERE X is_instance_of File, "
                        'X data_hash LIKE "{sha256}%"'
                    )
                ),
            )


if __name__ == "__main__":
    from unittest import main

    main()
