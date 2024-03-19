# -*- coding: utf-8 -*-

from rich import print as rprint
import sqlalchemy as sa
import sqlalchemy.orm as orm

from prompt_catalog.core.model import (
    Base,
    Prompt,
    PromptGroup,
    Tag,
    Element,
    ElementChoice,
)


def test():
    engine = sa.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    default_group = PromptGroup.new(name="default")
    productivity_tag = Tag.new(name="productivity")
    creative_tag = Tag.new(name="creative")

    summarize_prompt = Prompt.new(name="summarize", group_id=default_group.id)
    summarize_prompt.tags = [productivity_tag]

    brain_storm_prompt = Prompt.new(name="brain_storm", group_id=default_group.id)
    brain_storm_prompt.tags = [creative_tag]

    instruction_element = Element.new(name="instruction")

    instruction_element_choice_1 = ElementChoice.new(
        element_id=instruction_element.id,
        name="instruction_choice_1",
        body="instruction_choice_1_body_v1",
    )
    instruction_element_choice_2 = ElementChoice.new(
        element_id=instruction_element.id,
        name="instruction_choice_2",
        body="instruction_choice_2_body_v1",
    )
    instruction_element_choice_1.update(body="instruction_choice_1_body_v2")
    instruction_element_choice_2.update(body="instruction_choice_2_body_v2")

    with orm.Session(engine) as ses:
        # --- insert
        ses.add(default_group)

        ses.add(productivity_tag)
        ses.add(creative_tag)

        ses.add(summarize_prompt)
        ses.add(brain_storm_prompt)

        ses.add(instruction_element)
        ses.add(instruction_element_choice_1)
        ses.add(instruction_element_choice_2)
        ses.commit()

        # --- select
        group = ses.get(PromptGroup, default_group.id)
        assert group.name == "default"
        assert len(group.prompts) == 2

        prompt = ses.get(Prompt, summarize_prompt.id)
        assert prompt.name == "summarize"
        assert len(prompt.tags) == 1
        assert prompt.tags[0].name == "productivity"

        tag = ses.get(Tag, productivity_tag.id)
        assert tag.name == "productivity"
        assert len(tag.prompts) == 1
        assert tag.prompts[0].name == "summarize"

        element = ses.get(Element, instruction_element.id)
        assert element.name == "instruction"
        assert len(element.choices) == 2
        choice = element.choices[0]
        assert choice.create_at != choice.update_at


if __name__ == "__main__":
    from prompt_catalog.tests import run_cov_test

    run_cov_test(__file__, "prompt_catalog.core.model", preview=False)
