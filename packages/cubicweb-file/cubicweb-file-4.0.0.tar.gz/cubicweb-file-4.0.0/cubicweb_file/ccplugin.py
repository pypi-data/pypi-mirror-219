"""cubicweb-ctl plugin providing the fsimport command

:organization: Logilab
:copyright: 2010-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

import hashlib

from cubicweb.cwconfig import CubicWebConfiguration
from cubicweb.cwctl import CWCTL
from cubicweb.toolsutils import Command


class FSImportCommand(Command):
    """Import content of a directory on the file system as File entities.
    The instance must use the `file` cube.

    <instance id>
      identifier of the instance where directory's content has to be imported.

    <fs directory>
      directory to import (recursivly)
    """

    name = "fsimport"
    min_args = 2
    arguments = "<instance id> <fs file or directory>..."
    options = (
        (
            "map-folders",
            {
                "short": "F",
                "action": "store_true",
                "default": False,
                "help": (
                    "map file-system directories as Folder entities "
                    "(requires the `folder` cube)."
                ),
            },
        ),
        (
            "filed-under",
            {
                "short": "u",
                "type": "int",
                "help": "put imported file into the folder entity of the given eid.",
            },
        ),
    )

    def run(self, args):
        """run the command with its specific arguments"""
        from cubicweb.server.serverctl import repo_cnx
        from cubicweb_file.fsimport import fsimport

        appid = args.pop(0)
        config = CubicWebConfiguration.config_for(appid)
        repo, cnx = repo_cnx(config)
        repo.hm.call_hooks("server_maintenance", repo=repo)
        with cnx:
            fsimport(
                cnx,
                args,
                parenteid=self.config.filed_under,
                mapfolders=self.config.map_folders,
                bfss="data" in repo.system_source._storages.get("File", ()),
            )
            cnx.commit()


class FileRefreshHashCommand(Command):
    """Import content of a directory on the file system as File entities.
    The instance must use the `file` cube.

    <instance id>
      identifier of the instance where directory's content has to be imported.

    """

    name = "refresh-hash"
    min_args = 1
    arguments = "<instance id>..."
    options = (
        (
            "hash-algorithm",
            {
                "default": None,
                "type": "choice",
                "choices": list(hashlib.algorithms_available),
                "help": (
                    "hash algorithm to use (instead of the one configured "
                    "for the instance)"
                ),
            },
        ),
        (
            "force",
            {
                "short": "f",
                "action": "store_true",
                "default": False,
                "help": (
                    "Force the computation of hash if the instance "
                    "'compute-hash' option if False."
                ),
            },
        ),
        (
            "subclasses",
            {
                "action": "store_true",
                "default": False,
                "help": "Also refresh hash for entity types that inherit from File",
            },
        ),
    )

    def run(self, args):
        """run the command with its specific arguments"""
        from cubicweb.server.serverctl import repo_cnx

        appid = args.pop(0)
        config = CubicWebConfiguration.config_for(appid)

        repo, cnx = repo_cnx(config)
        if repo.vreg.config["compute-hash"] or self.config.force:
            repo.hm.call_hooks("server_maintenance", repo=repo)
            alg = self.config.hash_algorithm

            with cnx:
                with cnx.deny_all_hooks_but():
                    etypes = ["File"]
                    if self.config.subclasses:
                        etypes.extend(
                            cnx.repo.schema["File"].specialized_by(recursive=True)
                        )
                    print("ETYPES=", etypes)
                    for etype in etypes:
                        for e in cnx.execute(f"Any X WHERE X is {etype}").entities():
                            print("update hash for", e)
                            e.cw_set(data_hash=e.compute_hash(alg=alg))
                    cnx.commit()


CWCTL.register(FSImportCommand)
