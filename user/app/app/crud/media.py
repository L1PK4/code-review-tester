import os
import uuid
from typing import Generic, Type, TypeVar

from app import deps
from app.crud.base import ModelType
from app.services.storage.base_storage import BaseStorage
from botocore.client import BaseClient
from fastapi import UploadFile
from sqlalchemy.orm import Session

ModelAttachmentType = TypeVar("ModelAttachmentType", bound="BaseModel")


class MixinContent:

    def __init__(self, model: Type[ModelType]):
        self._content_column: str = "cover"
        self._storage: BaseStorage = deps.get_storage()
        self.model = model

    def change_content(
            self,
            db: Session,
            *,
            obj: ModelType | None = None,
            content: UploadFile | None = None,
            content_path: str | None = None,
            content_column: str | None = None
    ) -> int:
        """Изменить контент сущности

        При  :doc:`content == None` удаляет контент

        Args:
            db (Session): Сессия БД
            obj (ModelType | None, optional): Объект бд. По умолчанию None.
            content (UploadFile | None, optional): Контент. По умолчанию None.
            content_path (str | None, optional): Путь к объекту в сервисе.
            content_column (str | None, optional): Название столбца. По умолчанию _content_column.

        Returns:
            int: 0 - Выполнено
                -1 - сервис не отвечает
        """
        if content_column is None:
            content_column = self._content_column

        old_content = getattr(obj, content_column, None)
        new_url = None
        if content is not None:
            if content_path is None:
                content_path = self.model.__name__.lower() + '/' + content_column + '/'

            name = content_path + uuid.uuid4().hex + \
                os.path.splitext(content.filename)[1]  # type: ignore

            new_url = self._storage.load(
                name,
                content.file.read(),
                content_type=content.content_type
            )
            if new_url is None:
                return -1

        setattr(obj, content_column, new_url)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        if old_content is not None:
            self._storage.remove(old_content)
        return 0


class MixinAttachment(Generic[ModelType, ModelAttachmentType]):
    s3_bucket_name: str | None = None
    s3_client: BaseClient | None = None

    def __init__(self, model: Type[ModelType], model_attachment: Type[ModelAttachmentType]):
        self._attachment_column: str = 'url'
        self._storage: BaseStorage = deps.get_storage()
        self.model = model
        self._attachment_foreign_key: str = self.model.__name__.lower() + '_id'
        self.model_attachment = model_attachment

    def add_attachment(
            self,
            db: Session,
            *,
            attachment: UploadFile,
            obj: ModelType | None = None,
            content_path: str | None = None,
            attachment_column: str | None = None,
            attachment_foreign_key: str | None = None
    ) -> ModelAttachmentType | None:
        if attachment_column is None:
            attachment_column = self._attachment_column
        if attachment_foreign_key is None:
            attachment_foreign_key = self._attachment_foreign_key

        if content_path is None:
            content_path = self.model.__name__.lower() + '/' + attachment_column + '/'
        name = content_path + uuid.uuid4().hex + \
            os.path.splitext(attachment.filename)[1]

        new_url = self._storage.load(
            name,
            attachment.file.read(),
            content_type=attachment.content_type
        )
        if new_url is None:
            return None

        attachment_obj = self.model_attachment()

        if obj is not None:
            setattr(attachment_obj, attachment_foreign_key, obj.id)
        setattr(attachment_obj, attachment_column, new_url)
        db.add(attachment_obj)
        db.commit()
        db.refresh(attachment_obj)

        return attachment_obj

    def get_attachment(
            self,
            db: Session,
            *,
            attachment_id: int
    ) -> ModelAttachmentType | None:
        attachment = db.query(self.model_attachment) \
            .get(attachment_id)
        return attachment

    def delete_attachment(
            self,
            db: Session,
            *,
            attachment: ModelAttachmentType
    ) -> None:
        db.delete(attachment)
        db.commit()
