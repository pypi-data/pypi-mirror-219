import os
import subprocess
import tempfile
from typing import Tuple, Union

from repo2docker.buildpacks.base import BuildPack
from repo2docker.buildpacks.aicrowd_cacher.query_sources import (
    APIQuerySource,
    BaseQuerySource,
    CSVQuerySource,
)


class AIcrowdCachingBuildpack(BuildPack):
    def __init__(self):
        super().__init__()

        self.found_repo_match: bool = False
        self.found_deps_match: bool = False
        self.cache_image: Union[None, str] = None

        # this would only work in the context of AIcrowd Image Builder
        self.image_tag = os.getenv("BUILDER_IMAGE_TAG", "")

        self.source: BaseQuerySource = (
            APIQuerySource()
            if not os.getenv("AICROWD_R2D_DEBUG_CSV_QUERY_SOURCE")
            else CSVQuerySource()
        )

    def detect(self) -> bool:
        """
        Checks if we can re-use some older image either completely or for dependencies

        Returns:
            should we use this buildpack?
        """
        rhash, dhash = self.get_repo_hash()

        # update ONLY AFTER querying
        available_images = self.source.query(rhash, dhash)
        self.source.update(rhash, dhash, self.image_tag)

        if len(available_images.get("repo", [])) > 0:
            self.found_repo_match = True
            self.cache_image = available_images["repo"][0]
        elif len(available_images.get("deps", [])) > 0:
            self.found_deps_match = True
            self.cache_image = available_images["deps"][0]
        else:
            return False

        return self.found_repo_match or self.found_deps_match

    def get_repo_hash(self) -> Tuple[str, str]:
        """
        Calculates the hash for
         - entire repository
         - files specifying dependencies

        Returns:
            the hashes for repository and dependencies
        """
        tmpfile, tmpfile_name = tempfile.mkstemp()
        tmpfile_deps, tmpfile_deps_name = tempfile.mkstemp()

        calc_md5_proc = subprocess.Popen(
            [
                "find",
                ".",
                "-type",
                "f",
                "-not",
                "-path",
                "./.git/*",
                "-exec",
                "md5sum",
                "{}",
                ";",
            ],
            stdout=subprocess.PIPE,
        )
        calc_md5_proc_stdout = calc_md5_proc.communicate()[0]

        sorted_hash_proc = subprocess.Popen(
            ["sort", "-k", "2"], stdin=subprocess.PIPE, stdout=tmpfile
        )
        sorted_hash_proc.communicate(input=calc_md5_proc_stdout)

        dep_hash_proc = subprocess.Popen(
            [
                "grep",
                "-E",
                # if even one of these are different, we shouldn't use old cached image
                r"apt\.txt|requirements\.txt|environment\.yml|Dockerfile",
                tmpfile_name,
            ],
            stdout=tmpfile_deps,
        )
        dep_hash_proc.wait()

        repo_hash = (
            # run md5sum on the file containing hash for each file
            subprocess.Popen(["md5sum", tmpfile_name], stdout=subprocess.PIPE)
            # get the hash for that
            .stdout.read()
            .decode("utf-8")
            .strip()
            # the output is 94837593847acde... FILE_NAME
            # we are only interested in the hash part
            .split()[0]
        )
        deps_hash = (
            subprocess.Popen(["md5sum", tmpfile_deps_name], stdout=subprocess.PIPE)
            .stdout.read()
            .decode("utf-8")
            .strip()
            .split()[0]
        )

        os.remove(tmpfile_name)
        os.remove(tmpfile_deps_name)

        return repo_hash, deps_hash

    def render(self, build_args=None):
        """
        Return the dockerfile

        Args:
            build_args: passed by r2d, has some custom info

        Returns:
            the dockerfile in string
        """
        build_args = build_args or {}
        user = build_args.get("NB_USER", "aicrowd")

        if self.found_repo_match:
            return f"FROM {self.cache_image}"
        elif self.found_deps_match:
            return "\n".join(
                [
                    f"FROM {self.cache_image}",
                    "USER root",
                    f"RUN rm -r /home/{user}",
                    f"COPY --chown={user} src/ /home/{user}",
                    f"USER {user}",
                ]
            )
        else:
            raise ValueError("Unreachable")
