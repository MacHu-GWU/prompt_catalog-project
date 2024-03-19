# -*- coding: utf-8 -*-

import typing as T
import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
import sqlalchemy.orm as orm


def new_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class Base(orm.DeclarativeBase):
    def to_repr(self, fields: list[str]) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(f"{field}={getattr(self, field)!r}" for field in fields),
        )


prompt_and_tag = sa.Table(
    "prompt_and_tag",
    Base.metadata,
    sa.Column("prompt_id", sa.ForeignKey("prompts.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
)


class Prompt(Base):
    """
    todo: add docstring
    """

    __tablename__ = "prompts"

    # fmt: off
    id: orm.Mapped[str] = orm.mapped_column(sa.String, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    description: orm.Mapped[T.Optional[str]] = orm.mapped_column(sa.String, nullable=True)
    body: orm.Mapped[T.Optional[str]] = orm.mapped_column(sa.String, nullable=True)
    group_id: orm.Mapped[str] = orm.mapped_column(sa.ForeignKey("prompt_groups.id"), nullable=False)
    create_at: orm.Mapped[datetime] = orm.mapped_column(sa.String)
    update_at: orm.Mapped[datetime] = orm.mapped_column(sa.String)

    group: orm.Mapped["PromptGroup"] = orm.relationship(back_populates="prompts")
    tags: orm.Mapped[list["Tag"]] = orm.relationship(secondary=prompt_and_tag, back_populates="prompts")
    # fmt: on

    def __repr__(self) -> str:
        return self.to_repr(["id", "name"])

    @classmethod
    def new(
        cls,
        name: str,
        description: T.Optional[str] = None,
        body: T.Optional[str] = None,
        group_id: T.Optional[str] = None,
    ):
        utc_now = get_utc_now()
        if group_id is None:
            group_id = "default"
        return cls(
            id=new_uuid(),
            name=name,
            description=description,
            body=body,
            create_at=utc_now,
            update_at=utc_now,
            group_id=group_id,
        )

    def update(
        self,
        name: T.Optional[str] = None,
        description: T.Optional[str] = None,
        body: T.Optional[str] = None,
        group_id: T.Optional[str] = None,
    ) -> "Prompt":
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if body is not None:
            self.body = body
        if group_id is not None:
            self.group_id = group_id
        self.update_at = get_utc_now()
        return self


class PromptGroup(Base):
    """
    todo: add docstring
    """

    __tablename__ = "prompt_groups"

    # fmt: off
    id: orm.Mapped[str] = orm.mapped_column(sa.String, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    description: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    create_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)
    update_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)

    prompts: orm.Mapped[list["Prompt"]] = orm.relationship(back_populates="group")
    # fmt: on

    def __repr__(self) -> str:
        return self.to_repr(["id", "name"])

    @classmethod
    def new(
        cls,
        name: str,
        description: T.Optional[str] = None,
    ):
        utc_now = get_utc_now()
        return cls(
            id=new_uuid(),
            name=name,
            description=description,
            create_at=utc_now,
            update_at=utc_now,
        )

    def update(
        self,
        name: T.Optional[str] = None,
        description: T.Optional[str] = None,
    ) -> "PromptGroup":
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.update_at = get_utc_now()
        return self


class Tag(Base):
    """
    todo: add docstring
    """

    __tablename__ = "tags"

    # fmt: off
    id: orm.Mapped[str] = orm.mapped_column(sa.String, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    description: orm.Mapped[T.Optional[str]] = orm.mapped_column(sa.String, nullable=True)
    create_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)
    update_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)

    prompts: orm.Mapped[list["Prompt"]] = orm.relationship(secondary=prompt_and_tag, back_populates="tags")
    # fmt: on

    def __repr__(self) -> str:
        return self.to_repr(["id", "name"])

    @classmethod
    def new(
        cls,
        name: str,
        description: T.Optional[str] = None,
    ):
        utc_now = get_utc_now()
        return cls(
            id=new_uuid(),
            name=name,
            description=description,
            create_at=utc_now,
            update_at=utc_now,
        )

    def update(
        self,
        name: T.Optional[str] = None,
        description: T.Optional[str] = None,
    ) -> "Tag":
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.update_at = get_utc_now()
        return self


class Element(Base):
    """
    todo: add docstring
    """

    __tablename__ = "elements"

    # fmt: off
    id: orm.Mapped[str] = orm.mapped_column(sa.String, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True, nullable=False)
    description: orm.Mapped[T.Optional[str]] = orm.mapped_column(sa.String, nullable=True)
    create_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)
    update_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)

    choices: orm.Mapped[list["ElementChoice"]] = orm.relationship(back_populates="element")
    # fmt: on

    def __repr__(self) -> str:
        return self.to_repr(["id", "name"])

    @classmethod
    def new(
        cls,
        name: str,
        description: T.Optional[str] = None,
    ):
        utc_now = get_utc_now()
        return cls(
            id=new_uuid(),
            name=name,
            description=description,
            create_at=utc_now,
            update_at=utc_now,
        )

    def update(
        self,
        name: T.Optional[str] = None,
        description: T.Optional[str] = None,
    ) -> "Element":
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.update_at = get_utc_now()
        return self


class ElementChoice(Base):
    """
    todo: add docstring
    """

    __tablename__ = "element_choices"

    # fmt: off
    id: orm.Mapped[str] = orm.mapped_column(sa.String, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True, nullable=False)
    description: orm.Mapped[T.Optional[str]] = orm.mapped_column(sa.String, nullable=True)
    body: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False)
    create_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)
    update_at: orm.Mapped[datetime] = orm.mapped_column(sa.String, nullable=False)
    element_id: orm.Mapped[str] = orm.mapped_column(sa.ForeignKey("elements.id"), nullable=False)

    element: orm.Mapped["Element"] = orm.relationship(back_populates="choices")
    # fmt: on

    def __repr__(self) -> str:
        return self.to_repr(["id", "name"])

    @classmethod
    def new(
        cls,
        element_id: str,
        name: str,
        body: str,
        description: T.Optional[str] = None,
    ):
        utc_now = get_utc_now()
        return cls(
            id=new_uuid(),
            name=name,
            description=description,
            body=body,
            create_at=utc_now,
            update_at=utc_now,
            element_id=element_id,
        )

    def update(
        self,
        name: T.Optional[str] = None,
        description: T.Optional[str] = None,
        body: T.Optional[str] = None,
    ) -> "ElementChoice":
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if body is not None:
            self.body = body
        self.update_at = get_utc_now()
        return self
