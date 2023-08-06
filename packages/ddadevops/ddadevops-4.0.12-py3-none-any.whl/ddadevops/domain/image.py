from typing import List, Dict
from .common import (
    filter_none,
    Validateable,
)


class Image(Validateable):
    def __init__(
        self,
        inp: dict,
    ):
        self.image_dockerhub_user = inp.get("image_dockerhub_user")
        self.image_dockerhub_password = inp.get("image_dockerhub_password")
        self.image_tag = inp.get("image_tag")
        self.image_build_commons_path = inp.get("image_build_commons_path")
        self.image_use_package_common_files = inp.get(
            "image_use_package_common_files", True
        )
        self.image_build_commons_dir_name = inp.get(
            "image_build_commons_dir_name", "docker"
        )

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("image_dockerhub_user")
        result += self.__validate_is_not_empty__("image_dockerhub_password")
        if not self.image_use_package_common_files:
            result += self.__validate_is_not_empty__("image_build_commons_path")
            result += self.__validate_is_not_empty__("image_build_commons_dir_name")
        return result

    def build_commons_path(self):
        commons_path = [
            self.image_build_commons_path,
            self.image_build_commons_dir_name,
        ]
        return "/".join(filter_none(commons_path)) + "/"

    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return [
            {
                "gopass_path": "meissa/web/docker.com",
                "gopass_field": "login",
                "name": "image_dockerhub_user",
            },
            {
                "gopass_path": "meissa/web/docker.com",
                "name": "image_dockerhub_password",
            },
        ]
