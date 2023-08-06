import tarfile
from io import BytesIO

from loguru import logger

import docker
from train_lib.docker_util import TIMEOUT
from train_lib.security.constants import TrainTags
from train_lib.security.train_config import TrainConfig


def extract_train_config(img: str, config_path: str = "/opt/train_config.json"):
    """
    Extract the train configuration json from the specified image and return it as a dictionary
    :param img: docker image identifier
    :param config_path: path of the config file inside the image
    :return: dictionary containing the  security values stored inside the train:config.json
    """
    with extract_archive(img, config_path) as config_archive:
        config_file = config_archive.extractfile("train_config.json")
        data = config_file.read()
        train_config = TrainConfig.parse_raw(data)

    return train_config


def extract_query_json(
    img: str, query_file_path: str = "/opt/pht_train/query.json"
) -> bytes:
    """
    Extract query.json file from the specified image and return it as a dictionary
    :param img: docker image identifier
    :param query_file_path: path of the query file inside the image
    :return: dictionary containing the  security values stored inside the train:config.json
    """
    try:
        with extract_archive(img, query_file_path) as query_archive:
            query_file = query_archive.extractfile("query.json")
            data = query_file.read()

    except Exception:
        logger.warning(f"Could not extract query.json from train image: {img}")
        data = None
    return data


def files_from_archive(tar_archive: tarfile.TarFile):
    """
    Extracts only the actual files from the given tarfile

    :param tar_archive: the tar archive from which to extract the files
    :return: List of file object extracted from the tar archive
    """

    file_members = []
    # Find the actual files in the archive
    for member in tar_archive.getmembers():
        if member.isreg():  # extract the actual files from the archive
            file_members.append(member)

    files = []
    file_names = []
    for file_member in file_members:
        files.append(tar_archive.extractfile(file_member))
        # Extract the file names without the top level directory from the file members
        file_names.append("/".join(file_member.name.split("/")[1:]))

    return files, file_names


def result_files_from_archive(tar_archive: tarfile.TarFile):
    """
    Extracts the result files from the given archive returning the files as well as the director structure contained
    in the tar archive for later reconstruction

    :param tar_archive: the tar archive from which to extract the files
    :return: List of file object extracted from the tar archive
    """

    file_members = []
    for member in tar_archive.getmembers():
        if member.isreg():  # skip if the TarInfo is not files
            file_members.append(member)

    files = []
    for file_member in file_members:
        files.append(tar_archive.extractfile(file_member))
    return files, file_members, tar_archive.getmembers()


def extract_archive(img: str, extract_path: str) -> tarfile.TarFile:
    """
    Extracts a file or folder at the given path from the given docker image

    :param img: identifier of the img to extract the file from
    :param extract_path: path of the file or directory to extract from the container
    :return: tar archive containing the extracted path
    """
    client = docker.from_env(timeout=TIMEOUT)
    container = client.containers.create(img)
    stream, stat = container.get_archive(extract_path)
    file_obj = BytesIO()
    for i in stream:
        file_obj.write(i)
    file_obj.seek(0)
    tar = tarfile.open(mode="r", fileobj=file_obj)
    container.remove()
    return tar


def add_archive(img: str, archive: BytesIO, path: str):
    """
    Adds a given tar archive to a given docker image at the specified path
    :param img:  identifier of the image <repository>:<tag>
    :param archive: tar archive to be added to the image
    :param path: path at which the tar archive will be added inside the image

    :return:
    """

    client = docker.from_env(timeout=TIMEOUT)
    container = client.containers.create(img)
    container.put_archive(path, archive)
    container.wait()
    # Get repository and tag for committing the container to an image
    repository, tag = img.split(":")
    container.commit(repository=repository, tag=tag)
    container.wait()
    container.remove()


def display_archive_content(tar_archive: tarfile.TarFile):
    """
    Displays the content of the given tar archive

    :param tar_archive: the tar archive to display the content of
    """
    logger.debug("Displaying archive content: ")
    for member in tar_archive.getmembers():
        name = member.name
        size = member.size
        file_preview = tar_archive.extractfile(member).read(100)
        logger.debug(f"Name: {name}, Size: {size}, Preview: {file_preview}")


def rebase_train_image(base_image: str, train_image: str):
    """
    Rebase the given image on the given base image

    :param base_image: the base image to rebase the new image on
    :param latest_image: the image to rebase
    """
    client = docker.from_env(timeout=TIMEOUT)

    latest_container = client.containers.create(train_image)
    base_container = client.containers.create(base_image)

    src_archive, state = latest_container.get_archive("/opt")
    logger.debug(f"Rebase copy state: {state}")
    base_container.put_archive("/", src_archive)
    base_container.wait()

    repo = repository_from_image(train_image)
    base_container.commit(repository=repo, tag=TrainTags.LATEST.value)
    base_container.wait()

    # remove the containers
    latest_container.remove()
    base_container.remove()


def repository_from_image(img: str) -> str:
    """
    Extracts the repository from the given image identifier

    :param img: the image identifier
    :return: the repository of the given image
    """

    split = img.split(":")
    if len(split) == 1:
        return img
    elif len(split) == 2:
        return split[0]
    else:
        return ":".join(split[:-1])
