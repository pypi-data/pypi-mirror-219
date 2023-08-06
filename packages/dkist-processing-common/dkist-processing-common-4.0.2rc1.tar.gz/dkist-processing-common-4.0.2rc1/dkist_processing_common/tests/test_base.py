from random import shuffle

import pytest

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase


class Task(WorkflowTaskBase):
    def run(self) -> None:
        pass


@pytest.fixture
def base_task(tmp_path, recipe_run_id):
    with Task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        yield task
    task.scratch.purge()
    task.constants._purge()


@pytest.fixture
def tags_and_expected_generic_name() -> (list[str], str):
    tags = [
        Tag.input(),
        Tag.output(),
        Tag.intermediate(),
        Tag.frame(),
        Tag.calibrated(),
        Tag.debug(),
        Tag.task("FOO"),
        Tag.dsps_repeat(2),
        Tag.cs_step(4),
        Tag.modstate(5),
        Tag.workflow_task("BAR"),
        Tag.movie(),
        "ZZZ",
    ]
    shuffle(tags)
    expected_base_name = (
        f"{StemName.debug.value}_"
        f"{StemName.input.value}_"
        f"{StemName.intermediate.value}_"
        f"{StemName.calibrated.value}_"
        f"{StemName.output.value}_"
        f"{StemName.workflow_task.value.replace('_', '-')}-BAR_"
        f"{StemName.task.value}-FOO_"
        f"{StemName.dsps_repeat.value.replace('_', '-')}-2_"
        f"{StemName.cs_step.value.replace('_', '-')}-4_"
        f"{StemName.modstate.value}-5_"
        f"{StemName.movie.value}_"
        f"ZZZ"
    )
    return tags, expected_base_name


def test_apm_spans(base_task):
    """
    Given: A WorkflowTaskBase task
    When: Calling the task-specific apm_steps with weird inputs
    Then: Errors happen when they're supposed to and not when they're not supposed to
    """
    with pytest.raises(RuntimeError):
        with base_task.apm_processing_step("foo", span_type="bar"):
            pass

    with base_task.apm_task_step("foo", labels={"foo": "bar"}):
        pass


def test_tags(base_task):
    """
    Given: A WorkflowTaskBase task
    When: Creating, querying, and removing tags
    Then: The correct action is performed
    """
    path = base_task.scratch.workflow_base_path / "foo"
    path.touch()

    # Test assignment
    base_task.tag(path, ["tag1", "tag2"])
    assert list(base_task.read(["tag1", "tag2"])) == [path]

    # Test query
    assert sorted(base_task.tags(path)) == sorted(["tag1", "tag2"])

    # Test removal
    base_task.remove_tags(path, "tag1")
    assert base_task.tags(path) == ["tag2"]


def test_build_generic_tag_filename(base_task, tags_and_expected_generic_name):
    """
    Given: A WorkflowTaskBase task
    When: Constructing a default filename from a set of tags
    Then: The correct filename is returned
    """
    tags, expected_name = tags_and_expected_generic_name

    built_name = base_task._build_generic_tag_filename(tags)
    assert built_name.startswith(expected_name)
    assert built_name.endswith(".dat")


@pytest.mark.parametrize(
    "other_tags",
    [
        pytest.param("A", id="single"),
        pytest.param(["A", "B"], id="list"),
    ],
)
def test_write_workflow_task_tag(base_task, other_tags: str | list[str]):
    """
    :Given: A WorkflowTaskBase task and tags to write with
    :When: Writing a file with given tags
    :Then: Written file is tagged with a workflow task class tag in addition to given tags
    """
    # When
    path = base_task.write(
        data=b"123",
        tags=other_tags,
    )
    path = base_task.scratch.workflow_base_path / path
    # Then
    tags = base_task.tags(path)
    assert Tag.workflow_task(base_task.__class__.__name__) in tags
