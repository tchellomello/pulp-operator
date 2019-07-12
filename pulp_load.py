#https://github.com/pulp/pulpcore/blob/master/.travis/test_bindings.py
from pulpcore.client.pulpcore import (ApiClient as CoreApiClient, ArtifactsApi, Configuration,
                                      Repository, RepositoriesApi, RepositoriesVersionsApi,
                                      TasksApi, Upload, UploadCommit, UploadsApi)
from pulpcore.client.pulp_file import (ApiClient as FileApiClient, ContentFilesApi,
                                       FileContent, DistributionsFileApi,
                                       FileDistribution, PublicationsFileApi,
                                       RemotesFileApi, FileRemote, RepositorySyncURL,
                                       FilePublication)

from pulpcore.client.pulpcore.exceptions import ApiException

from pprint import pprint
from time import sleep
import hashlib
import os
import requests
from tempfile import NamedTemporaryFile
import sys
import random


def monitor_task(task_href):
    """Polls the Task API until the task is in a completed state.
    Prints the task details and a success or failure message. Exits on failure.
    Args:
        task_href(str): The href of the task to monitor
    Returns:
        list[str]: List of hrefs that identify resource created by the task
    """
    completed = ['completed', 'failed', 'canceled']
    task = tasks.read(task_href)
    while task.state not in completed:
        sleep(2)
        task = tasks.read(task_href)
    pprint(task)
    if task.state == 'completed':
        print("The task was successfful.")
        return task.created_resources
    else:
        print("The task did not finish successfully.")
        exit()


def upload_file_in_chunks(file_path):
    """Uploads a file using the Uploads API
    The file located at 'file_path' is uploaded in chunks of 200kb.
    Args:
        file_path (str): path to the file being uploaded to Pulp
    Returns:
        upload object
    """
    size = os.stat(file_path).st_size
    chunk_size = 200000
    offset = 0
    sha256hasher = hashlib.new('sha256')

    upload = uploads.create(Upload(size=size))

    with open(file_path, 'rb') as full_file:
        while True:
            chunk = full_file.read(chunk_size)
            if not chunk:
                break
            actual_chunk_size = len(chunk)
            content_range = 'bytes {start}-{end}/{size}'.format(start=offset,
                                                                end=offset+actual_chunk_size-1,
                                                                size=size)
            with NamedTemporaryFile() as file_chunk:
                file_chunk.write(chunk)
                upload = uploads.update(upload_href=upload.href,
                                        file=file_chunk.name,
                                        content_range=content_range)
            offset += chunk_size
            sha256hasher.update(chunk)
        uploads.commit(upload.href, UploadCommit(sha256=sha256hasher.hexdigest()))
    return upload





# Configure HTTP basic authorization: basic
configuration = Configuration()
configuration.username = 'admin'
configuration.password = 'password'
configuration.host = 'http://omg.tatu.home:32120'
configuration.safe_chars_for_path_param = '/'

core_client = CoreApiClient(configuration)
file_client = FileApiClient(configuration)

# Create api clients for all resource types
artifacts = ArtifactsApi(core_client)
repositories = RepositoriesApi(core_client)
repoversions = RepositoriesVersionsApi(core_client)
filecontent = ContentFilesApi(file_client)
filedistributions = DistributionsFileApi(core_client)
filepublications = PublicationsFileApi(file_client)
fileremotes = RemotesFileApi(file_client)
tasks = TasksApi(core_client)
uploads = UploadsApi(core_client)


def randString(length=6):
    your_letters='abcdefghi'
    return ''.join((random.choice(your_letters) for i in range(length)))


# Create a File Remote
remote_url = 'http://myapps-service.default.svc.cluster.local/ISOs/PULP_MANIFEST'

reponame = randString()
remote_data = FileRemote(name=reponame, url=remote_url)
file_remote = fileremotes.create(remote_data)
pprint(file_remote)

# Create a Repository
repository_data = Repository(name=reponame)
repository = repositories.create(repository_data)
pprint(repository)
#sys.exit(1)

# Sync a Repository
repository_sync_data = RepositorySyncURL(repository=repository.href)
sync_response = fileremotes.sync(file_remote.href, repository_sync_data)

pprint(sync_response)
#sys.exit(1)

# Monitor the sync task
created_resources = monitor_task(sync_response.task)

repository_version_1 = repoversions.read(created_resources[0])
pprint(repository_version_1)


####
#sys.exit(1)


# Create an artifact from a local file
with open(f'{reponame}_test_bindings.py', 'w') as fd:
    fd.write(reponame)

file_path = os.path.join(f'{reponame}_test_bindings.py')
try:
    artifact = artifacts.create(file=file_path)
    pprint(artifact)
except ApiException as err:
    pprint(err)

# Create a FileContent from the artifact
file_data = FileContent(relative_path=f'{reponame}.tar.gz', artifact=artifact.href)
filecontent = filecontent.create(file_data)
pprint(filecontent)

# Add the new FileContent to a repository version
repo_version_data = {'add_content_units': [filecontent.href]}
repo_version_response = repoversions.create(repository.href, repo_version_data)

# Monitor the repo version creation task
created_resources = monitor_task(repo_version_response.task)

repository_version_2 = repoversions.read(created_resources[0])
pprint(repository_version_2)

# Create a publication from the latest version of the repository
publish_data = FilePublication(repository=repository.href)
publish_response = filepublications.create(publish_data)

# Monitor the publish task
created_resources = monitor_task(publish_response.task)
publication_href = created_resources[0]

distribution_data = FileDistribution(name=f'{reponame}_baz25', base_path=f'{reponame}_foo25', publication=publication_href)
distribution = filedistributions.create(distribution_data)
pprint(distribution)

# remote file
os.remove(f'{reponame}_test_bindings.py')
