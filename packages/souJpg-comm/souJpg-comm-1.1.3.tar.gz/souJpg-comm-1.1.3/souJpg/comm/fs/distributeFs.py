import glob
import os
import shutil
import traceback

from loguru import logger as logger1
from minio import Minio
from souJpg import gcf

from souJpg.comm.utils import singleton


class DistributeFs:
    def __init__(self):
        pass

    def upload(self, localFilePath=None, remoteFilePath=None, deleteLocal=True):
        pass

    def uploadFolder(
        self, localFolderPath=None, remoteFolderPath=None, deleteLocal=True
    ):
        pass

    def download(self, localFilePath=None, remoteFilePath=None):
        pass

    def downloadFoler(self, localFolderPath=None, remoteFolderPath=None):
        pass

    def ls(self, remoteFolderPath=None, pattern=None):
        pass

    def checkFileExist(self, remoteFilePath=None):
        pass

    def close(self):
        pass

    def cleanLocalFile(self, localFilePath=None):
        try:
            os.remove(localFilePath)

            logger1.info("delete temporary local file: {}", localFilePath)

        except BaseException as e:
            logger1.info(str(e))

    def cleanLocalFolder(self, localFolderPath=None):
        try:
            shutil.rmtree(localFolderPath, ignore_errors=True)

            logger1.info("delete temporary local folder: {}", localFolderPath)

        except BaseException as e:
            logger1.info(str(e))


@singleton
class MinioFs(DistributeFs):
    def __init__(self):
        self.minioClient = Minio(
            gcf.minio_server,
            access_key=gcf.minio_access_key,
            secret_key=gcf.minio_secret_key,
            secure=False,
        )

    def parseRemoteFilePath(self, remoteFilePath=None):
        ss = remoteFilePath.split("/")
        bucketName = ss[0]

        fileName = "/".join(ss[1:])
        return bucketName, fileName

    def upload(self, localFilePath=None, remoteFilePath=None, deleteLocal=True):
        """

        :param localFilePath:
        :param remoteFilePath: bucketName/subFolderName/fileName
        :param deleteLocal:
        :return:
        """
        bucketName, fileName = self.parseRemoteFilePath(remoteFilePath=remoteFilePath)
        try:
            self.minioClient.fput_object(bucketName, fileName, localFilePath)
            if deleteLocal:
                os.remove(localFilePath)
                print("delete local file:%s " % localFilePath)
        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def uploadFolder(
        self, localFolderPath=None, remoteFolderPath=None, deleteLocal=True
    ):
        """

        :param localFolderPath:
        :param remoteFolderPath: bucketName/subFolderName/
        :param deleteLocal:
        all the files within localFolderPath will be saved to remote folder subFolderName
        :return:
        """
        bucketName, subFolderName = self.parseRemoteFilePath(
            remoteFilePath=remoteFolderPath
        )
        try:
            for local_file in glob.glob(localFolderPath + "/**"):
                if not os.path.isfile(local_file):
                    fileName = os.path.basename(local_file)
                    remoteFolderPath_ = "/".join([remoteFolderPath, fileName])
                    self.uploadFolder(
                        localFolderPath=local_file,
                        remoteFolderPath=remoteFolderPath_,
                        deleteLocal=False,
                    )

                else:
                    fileName = os.path.basename(local_file)
                    fileName = "/".join([subFolderName, fileName])
                    self.minioClient.fput_object(bucketName, fileName, local_file)

            if deleteLocal:
                os.remove(localFolderPath)
                print("delete local file:%s " % localFolderPath)
        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def download(self, localFilePath=None, remoteFilePath=None):
        bucketName, fileName = self.parseRemoteFilePath(remoteFilePath=remoteFilePath)
        try:
            self.minioClient.fget_object(bucketName, fileName, localFilePath)

        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def downloadFoler(self, localFolderPath=None, remoteFolderPath=None):
        logger1.info("download {}, to {}", remoteFolderPath, localFolderPath)
        bucketName, folderName = self.parseRemoteFilePath(
            remoteFilePath=remoteFolderPath
        )

        try:
            objects = self.minioClient.list_objects(
                bucketName,
                prefix=folderName,
                recursive=True,
            )

            for obj in objects:
                fileName = obj.object_name
                ss = fileName.split("/")
                subFolderName = os.sep.join(ss[0 : len(ss) - 1])
                fileName_ = ss[-1]
                os.makedirs(localFolderPath + os.sep + subFolderName, exist_ok=True)
                self.minioClient.fget_object(
                    bucketName, fileName, localFolderPath + os.sep + fileName
                )

        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def ls(self, remoteFolderPath=None, pattern=None):
        pass

    def checkFileExist(self, remoteFilePath=None):
        pass

    def close(self):
        pass


@singleton
class TecentOsFs(DistributeFs):
    def __init__(self):
        self.minioClient = Minio(
            gcf.minio_server,
            access_key=gcf.minio_access_key,
            secret_key=gcf.minio_secret_key,
            secure=False,
        )

    def parseRemoteFilePath(self, remoteFilePath=None):
        ss = remoteFilePath.split("/")
        bucketName = ss[0]

        fileName = "/".join(ss[1:])
        return bucketName, fileName

    def upload(self, localFilePath=None, remoteFilePath=None, deleteLocal=True):
        """

        :param localFilePath:
        :param remoteFilePath: bucketName/subFolderName/fileName
        :param deleteLocal:
        :return:
        """
        bucketName, fileName = self.parseRemoteFilePath(remoteFilePath=remoteFilePath)
        try:
            self.minioClient.fput_object(bucketName, fileName, localFilePath)
            if deleteLocal:
                os.remove(localFilePath)
                print("delete local file:%s " % localFilePath)
        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def uploadFolder(
        self, localFolderPath=None, remoteFolderPath=None, deleteLocal=True
    ):
        """

        :param localFolderPath:
        :param remoteFolderPath: bucketName/subFolderName/
        :param deleteLocal:
        all the files within localFolderPath will be saved to remote folder subFolderName
        :return:
        """
        bucketName, subFolderName = self.parseRemoteFilePath(
            remoteFilePath=remoteFolderPath
        )
        try:
            for local_file in glob.glob(localFolderPath + "/**"):
                if not os.path.isfile(local_file):
                    fileName = os.path.basename(local_file)
                    remoteFolderPath_ = "/".join([remoteFolderPath, fileName])
                    self.uploadFolder(
                        localFolderPath=local_file,
                        remoteFolderPath=remoteFolderPath_,
                        deleteLocal=False,
                    )

                else:
                    fileName = os.path.basename(local_file)
                    fileName = "/".join([subFolderName, fileName])
                    self.minioClient.fput_object(bucketName, fileName, local_file)

            if deleteLocal:
                os.remove(localFolderPath)
                print("delete local file:%s " % localFolderPath)
        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def download(self, localFilePath=None, remoteFilePath=None):
        bucketName, fileName = self.parseRemoteFilePath(remoteFilePath=remoteFilePath)
        try:
            self.minioClient.fget_object(bucketName, fileName, localFilePath)

        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def downloadFoler(self, localFolderPath=None, remoteFolderPath=None):
        logger1.info("download {}, to {}", remoteFolderPath, localFolderPath)
        bucketName, folderName = self.parseRemoteFilePath(
            remoteFilePath=remoteFolderPath
        )

        try:
            objects = self.minioClient.list_objects(
                bucketName,
                prefix=folderName,
                recursive=True,
            )

            for obj in objects:
                fileName = obj.object_name
                ss = fileName.split("/")
                subFolderName = os.sep.join(ss[0 : len(ss) - 1])
                fileName_ = ss[-1]
                os.makedirs(localFolderPath + os.sep + subFolderName, exist_ok=True)
                self.minioClient.fget_object(
                    bucketName, fileName, localFolderPath + os.sep + fileName
                )

        except Exception as err:
            logger1.info(str(err))

            error = traceback.format_exc()
            logger1.info(error)

    def ls(self, remoteFolderPath=None, pattern=None):
        pass

    def checkFileExist(self, remoteFilePath=None):
        pass

    def close(self):
        pass


if __name__ == "__main__":
    pass
