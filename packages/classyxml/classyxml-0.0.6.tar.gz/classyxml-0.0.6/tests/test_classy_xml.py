import os
import pytest
from classy_xml import ClassyXml, XmlElement


@pytest.fixture
def classy_xml_test_fixture():
    filepath = os.path.split(__file__)[0]
    test_xml = os.path.join(filepath, "test.xml")
    return ClassyXml(test_xml)


@pytest.fixture
def classy_xml_empty_fixture():
    return ClassyXml()


@pytest.fixture
def classy_xml_countries_fixture():
    filepath = os.path.split(__file__)[0]
    test_xml = os.path.join(filepath, "countries.xml")
    return ClassyXml(test_xml)


@pytest.fixture
def classy_xml_modify_and_save_fixture():
    return ClassyXml()


def test_basic_element_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.basic_element) == 1


def test_basic_element_text(classy_xml_test_fixture):
    assert classy_xml_test_fixture.basic_element.text == "basic_element_text"


def test_multi_element_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.multi_element) == 2


def test_multi_element_0_text(classy_xml_test_fixture):
    assert classy_xml_test_fixture.multi_element[0].text == "multi_element_text_0"


def test_multi_element_1_text(classy_xml_test_fixture):
    assert classy_xml_test_fixture.multi_element[1].text == "multi_element_text_1"


def test_empty_element_with_attributes_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.empty_element_with_attributes) == 1


def test_empty_element_with_attributes_text(classy_xml_test_fixture):
    assert classy_xml_test_fixture.empty_element_with_attributes.text is None


def test_empty_element_with_attributes_attributes(classy_xml_test_fixture):
    assert classy_xml_test_fixture.empty_element_with_attributes.name == "attr_name"
    assert classy_xml_test_fixture.empty_element_with_attributes.value == "attr_value"


def test_empty_multi_element_with_attributes_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.empty_multi_element_with_attributes) == 2


def test_empty_multi_element_with_attributes_text(classy_xml_test_fixture):
    assert classy_xml_test_fixture.empty_multi_element_with_attributes[0].text is None
    assert classy_xml_test_fixture.empty_multi_element_with_attributes[1].text is None


def test_empty_multi_element_with_attributes_attributes(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.empty_multi_element_with_attributes[0].name
        == "attr_0_name"
    )
    assert (
        classy_xml_test_fixture.empty_multi_element_with_attributes[0].value
        == "attr_0_value"
    )
    assert (
        classy_xml_test_fixture.empty_multi_element_with_attributes[1].name
        == "attr_1_name"
    )
    assert (
        classy_xml_test_fixture.empty_multi_element_with_attributes[1].value
        == "attr_1_value"
    )


def test_basic_element_with_attributes_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.basic_element_with_attributes) == 1


def test_basic_element_with_attributes_text(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.basic_element_with_attributes.text
        == "basic_element_with_attributes_text"
    )


def test_basic_element_with_attributes_attributes(classy_xml_test_fixture):
    assert classy_xml_test_fixture.basic_element_with_attributes.name == "attr_name"
    assert classy_xml_test_fixture.basic_element_with_attributes.value == "attr_value"


def test_multi_element_with_attributes_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.multi_element_with_attributes) == 2


def test_multi_element_with_attributes_text(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.multi_element_with_attributes[0].text
        == "multi_element_with_attributes_text_0"
    )
    assert (
        classy_xml_test_fixture.multi_element_with_attributes[1].text
        == "multi_element_with_attributes_text_1"
    )


def test_multi_element_with_attributes_attributes(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.multi_element_with_attributes[0].name == "attr_0_name"
    )
    assert (
        classy_xml_test_fixture.multi_element_with_attributes[0].value == "attr_0_value"
    )
    assert (
        classy_xml_test_fixture.multi_element_with_attributes[1].name == "attr_1_name"
    )
    assert (
        classy_xml_test_fixture.multi_element_with_attributes[1].value == "attr_1_value"
    )


def test_basic_nested_element_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.basic_nested_element) == 1


def test_basic_nested_element__basic_element_child_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.basic_nested_element.basic_element_child) == 1


def test_basic_nested_element__basic_element_child_text(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.basic_nested_element.basic_element_child.text
        == "basic_element_child_text"
    )


def test_basic_nested_element__multi_element_child_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.basic_nested_element.multi_element_child) == 2


def test_basic_nested_element__multi_element_child_text(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_child[0].text
        == "multi_element_child_text_0"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_child[1].text
        == "multi_element_child_text_1"
    )


def test_basic_nested_element__empty_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.basic_nested_element.empty_element_with_attributes_child
        )
        == 1
    )


def test_basic_nested_element__empty_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_element_with_attributes_child.text
        is None
    )


def test_basic_nested_element__empty_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_element_with_attributes_child.name
        == "child_attr_name"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_element_with_attributes_child.value
        == "child_attr_value"
    )


def test_basic_nested_element__empty_multi_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child
        )
        == 2
    )


def test_basic_nested_element__empty_multi_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child[
            0
        ].text
        is None
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child[
            1
        ].text
        is None
    )


def test_basic_nested_element__empty_multi_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child[
            0
        ].name
        == "child_attr_0_name"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child[
            0
        ].value
        == "child_attr_0_value"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child[
            1
        ].name
        == "child_attr_1_name"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.empty_multi_element_with_attributes_child[
            1
        ].value
        == "child_attr_1_value"
    )


def test_basic_nested_element__basic_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.basic_nested_element.basic_element_with_attributes_child
        )
        == 1
    )


def test_basic_nested_element__basic_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.basic_element_with_attributes_child.text
        == "basic_element_with_attributes_child_text"
    )


def test_basic_nested_element__basic_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.basic_element_with_attributes_child.name
        == "child_attr_name"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.basic_element_with_attributes_child.value
        == "child_attr_value"
    )


def test_basic_nested_element__multi_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child
        )
        == 2
    )


def test_basic_nested_element__multi_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child[
            0
        ].text
        == "multi_element_with_attributes_child_text_0"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child[
            1
        ].text
        == "multi_element_with_attributes_child_text_1"
    )


def test_basic_nested_element__multi_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child[
            0
        ].name
        == "child_attr_0_name"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child[
            0
        ].value
        == "child_attr_0_value"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child[
            1
        ].name
        == "child_attr_1_name"
    )
    assert (
        classy_xml_test_fixture.basic_nested_element.multi_element_with_attributes_child[
            1
        ].value
        == "child_attr_1_value"
    )


def test_multi_nested_element_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.multi_nested_element) == 2


def test_multi_nested_element__basic_element_child_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.multi_nested_element[0].basic_element_child) == 1
    assert len(classy_xml_test_fixture.multi_nested_element[1].basic_element_child) == 1


def test_multi_nested_element__basic_element_child_text(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.multi_nested_element[0].basic_element_child.text
        == "basic_element_child_0_text"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1].basic_element_child.text
        == "basic_element_child_1_text"
    )


def test_multi_nested_element__multi_element_child_length(classy_xml_test_fixture):
    assert len(classy_xml_test_fixture.multi_nested_element[0].multi_element_child) == 2
    assert len(classy_xml_test_fixture.multi_nested_element[1].multi_element_child) == 2


def test_multi_nested_element__multi_element_child_text(classy_xml_test_fixture):
    assert (
        classy_xml_test_fixture.multi_nested_element[0].multi_element_child[0].text
        == "multi_element_child_0_text_0"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0].multi_element_child[1].text
        == "multi_element_child_0_text_1"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1].multi_element_child[0].text
        == "multi_element_child_1_text_0"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1].multi_element_child[1].text
        == "multi_element_child_1_text_1"
    )


def test_multi_nested_element__empty_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                0
            ].empty_element_with_attributes_child
        )
        == 1
    )
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                1
            ].empty_element_with_attributes_child
        )
        == 1
    )


def test_multi_nested_element__empty_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[
            0
        ].empty_element_with_attributes_child.text
        is None
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            1
        ].empty_element_with_attributes_child.text
        is None
    )


def test_multi_nested_element__empty_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[
            0
        ].empty_element_with_attributes_child.name
        == "child_0_attr_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            0
        ].empty_element_with_attributes_child.value
        == "child_0_attr_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            1
        ].empty_element_with_attributes_child.name
        == "child_1_attr_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            1
        ].empty_element_with_attributes_child.value
        == "child_1_attr_value"
    )


def test_multi_nested_element__empty_multi_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                0
            ].empty_multi_element_with_attributes_child
        )
        == 2
    )
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                1
            ].empty_multi_element_with_attributes_child
        )
        == 2
    )


def test_multi_nested_element__empty_multi_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .empty_multi_element_with_attributes_child[0]
        .text
        is None
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .empty_multi_element_with_attributes_child[1]
        .text
        is None
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .empty_multi_element_with_attributes_child[0]
        .text
        is None
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .empty_multi_element_with_attributes_child[1]
        .text
        is None
    )


def test_multi_nested_element__empty_multi_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .empty_multi_element_with_attributes_child[0]
        .name
        == "child_0_attr_0_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .empty_multi_element_with_attributes_child[0]
        .value
        == "child_0_attr_0_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .empty_multi_element_with_attributes_child[1]
        .name
        == "child_0_attr_1_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .empty_multi_element_with_attributes_child[1]
        .value
        == "child_0_attr_1_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .empty_multi_element_with_attributes_child[0]
        .name
        == "child_1_attr_0_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .empty_multi_element_with_attributes_child[0]
        .value
        == "child_1_attr_0_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .empty_multi_element_with_attributes_child[1]
        .name
        == "child_1_attr_1_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .empty_multi_element_with_attributes_child[1]
        .value
        == "child_1_attr_1_value"
    )


def test_multi_nested_element__basic_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                0
            ].basic_element_with_attributes_child
        )
        == 1
    )
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                1
            ].basic_element_with_attributes_child
        )
        == 1
    )


def test_multi_nested_element__basic_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[
            0
        ].basic_element_with_attributes_child.text
        == "basic_element_with_attributes_child_0_text"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            1
        ].basic_element_with_attributes_child.text
        == "basic_element_with_attributes_child_1_text"
    )


def test_multi_nested_element__basic_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[
            0
        ].basic_element_with_attributes_child.name
        == "child_0_attr_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            0
        ].basic_element_with_attributes_child.value
        == "child_0_attr_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            1
        ].basic_element_with_attributes_child.name
        == "child_1_attr_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[
            1
        ].basic_element_with_attributes_child.value
        == "child_1_attr_value"
    )


def test_multi_nested_element__multi_element_with_attributes_child_length(
    classy_xml_test_fixture,
):
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                0
            ].multi_element_with_attributes_child
        )
        == 2
    )
    assert (
        len(
            classy_xml_test_fixture.multi_nested_element[
                1
            ].multi_element_with_attributes_child
        )
        == 2
    )


def test_multi_nested_element__multi_element_with_attributes_child_text(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .multi_element_with_attributes_child[0]
        .text
        == "multi_element_with_attributes_child_0_text_0"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .multi_element_with_attributes_child[1]
        .text
        == "multi_element_with_attributes_child_0_text_1"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .multi_element_with_attributes_child[0]
        .text
        == "multi_element_with_attributes_child_1_text_0"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .multi_element_with_attributes_child[1]
        .text
        == "multi_element_with_attributes_child_1_text_1"
    )


def test_multi_nested_element__multi_element_with_attributes_child_attributes(
    classy_xml_test_fixture,
):
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .multi_element_with_attributes_child[0]
        .name
        == "child_0_attr_0_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .multi_element_with_attributes_child[0]
        .value
        == "child_0_attr_0_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .multi_element_with_attributes_child[1]
        .name
        == "child_0_attr_1_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[0]
        .multi_element_with_attributes_child[1]
        .value
        == "child_0_attr_1_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .multi_element_with_attributes_child[0]
        .name
        == "child_1_attr_0_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .multi_element_with_attributes_child[0]
        .value
        == "child_1_attr_0_value"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .multi_element_with_attributes_child[1]
        .name
        == "child_1_attr_1_name"
    )
    assert (
        classy_xml_test_fixture.multi_nested_element[1]
        .multi_element_with_attributes_child[1]
        .value
        == "child_1_attr_1_value"
    )


def test_multi_nested_element__unique_element_child_existence(classy_xml_test_fixture):
    assert hasattr(
        classy_xml_test_fixture.multi_nested_element[0], "unique_element_child"
    )
    assert not hasattr(
        classy_xml_test_fixture.multi_nested_element[1], "unique_element_child"
    )


def test_classy_xml_add_element(classy_xml_empty_fixture):
    classy_xml_empty_fixture.test_element = XmlElement()
    assert isinstance(classy_xml_empty_fixture.test_element, XmlElement)


def test_classy_xml_remove_element(classy_xml_empty_fixture):
    classy_xml_empty_fixture.test_element = XmlElement()
    del classy_xml_empty_fixture.test_element
    assert not hasattr(classy_xml_empty_fixture, "test_element")


def test_classy_xml_add_element_array(classy_xml_empty_fixture):
    classy_xml_empty_fixture.test_element_array = XmlElement()
    classy_xml_empty_fixture.test_element_array = XmlElement()
    assert isinstance(classy_xml_empty_fixture.test_element_array[0], XmlElement)
    assert isinstance(classy_xml_empty_fixture.test_element_array[1], XmlElement)
    assert len(classy_xml_empty_fixture.test_element_array) == 2


def test_classy_xml_remove_element_array(classy_xml_empty_fixture):
    classy_xml_empty_fixture.test_element_array = XmlElement()
    classy_xml_empty_fixture.test_element_array = XmlElement()
    del classy_xml_empty_fixture.test_element_array[0]
    assert isinstance(classy_xml_empty_fixture.test_element_array, XmlElement)
    assert len(classy_xml_empty_fixture.test_element_array) == 1


def test_xml_element_add_element(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    assert isinstance(classy_xml_empty_fixture.classy_element.xml_element, XmlElement)


def test_xml_element_remove_element(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    del classy_xml_empty_fixture.classy_element.xml_element
    assert not hasattr(classy_xml_empty_fixture.classy_element, "xml_element")


def test_xml_element_add_element_array(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    assert isinstance(
        classy_xml_empty_fixture.classy_element.xml_element[0], XmlElement
    )
    assert isinstance(
        classy_xml_empty_fixture.classy_element.xml_element[1], XmlElement
    )
    assert len(classy_xml_empty_fixture.classy_element.xml_element) == 2


def test_xml_element_remove_element_array(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    del classy_xml_empty_fixture.classy_element.xml_element[0]
    assert isinstance(classy_xml_empty_fixture.classy_element.xml_element, XmlElement)
    assert len(classy_xml_empty_fixture.classy_element.xml_element) == 1


def test_xml_element_add_text(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element.text = "test"
    assert classy_xml_empty_fixture.classy_element.xml_element.text == "test"


def test_xml_element_change_text(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element.text = "test"
    classy_xml_empty_fixture.classy_element.xml_element.text = "changed"
    assert classy_xml_empty_fixture.classy_element.xml_element.text == "changed"


def test_xml_element_remove_text(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element.text = "test"
    del classy_xml_empty_fixture.classy_element.xml_element.text
    assert classy_xml_empty_fixture.classy_element.xml_element.text is None


def test_xml_element_array_add_text(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element[0].text = "test"
    assert classy_xml_empty_fixture.classy_element.xml_element[0].text == "test"
    assert classy_xml_empty_fixture.classy_element.xml_element[1].text is None


def test_xml_element_array_remove_text(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element[0].text = "test_0"
    classy_xml_empty_fixture.classy_element.xml_element[1].text = "test_1"
    del classy_xml_empty_fixture.classy_element.xml_element[0].text
    assert classy_xml_empty_fixture.classy_element.xml_element[0].text is None
    assert classy_xml_empty_fixture.classy_element.xml_element[1].text == "test_1"


def test_xml_element_add_attribute(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element.name = "test_name"
    classy_xml_empty_fixture.classy_element.xml_element.value = 1
    assert classy_xml_empty_fixture.classy_element.xml_element.name == "test_name"
    assert classy_xml_empty_fixture.classy_element.xml_element.value == "1"


def test_xml_element_change_attribute(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element.name = "test_name"
    classy_xml_empty_fixture.classy_element.xml_element.name = "changed_name"
    assert classy_xml_empty_fixture.classy_element.xml_element.name == "changed_name"


def test_xml_element_remove_attribute(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element.value = "test"
    del classy_xml_empty_fixture.classy_element.xml_element.value
    assert not hasattr(classy_xml_empty_fixture.classy_element.xml_element, "value")


def test_xml_element_array_add_attribute(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element[0].name = "test_name_0"
    classy_xml_empty_fixture.classy_element.xml_element[1].name = "test_name_1"
    assert classy_xml_empty_fixture.classy_element.xml_element[0].name == "test_name_0"
    assert classy_xml_empty_fixture.classy_element.xml_element[1].name == "test_name_1"


def test_xml_element_array_change_attribute(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element[0].name = "test_name_0"
    classy_xml_empty_fixture.classy_element.xml_element[1].name = "test_name_1"
    classy_xml_empty_fixture.classy_element.xml_element[0].name = "test_name_0_changed"
    assert (
        classy_xml_empty_fixture.classy_element.xml_element[0].name
        == "test_name_0_changed"
    )
    assert classy_xml_empty_fixture.classy_element.xml_element[1].name == "test_name_1"


def test_xml_element_array_remove_attribute(classy_xml_empty_fixture):
    classy_xml_empty_fixture.classy_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element = XmlElement()
    classy_xml_empty_fixture.classy_element.xml_element[0].name = "test_name_0"
    classy_xml_empty_fixture.classy_element.xml_element[1].name = "test_name_1"
    del classy_xml_empty_fixture.classy_element.xml_element[0].name
    assert not hasattr(classy_xml_empty_fixture.classy_element.xml_element[0], "name")
    assert classy_xml_empty_fixture.classy_element.xml_element[1].name == "test_name_1"


def test_save_as(classy_xml_countries_fixture):
    filepath = os.path.split(__file__)[0]
    save_as_filename = os.path.join(filepath, "temp_countries.xml")
    classy_xml_countries_fixture.save_as(save_as_filename)
    with open(classy_xml_countries_fixture.xml_file) as file:
        countries_text = file.read()
    with open(save_as_filename) as file:
        temp_countries_text = file.read()
    os.remove(save_as_filename)
    assert countries_text == temp_countries_text


def test_modify_and_save_xml(classy_xml_empty_fixture):
    classy_xml_empty_fixture.country = XmlElement(attributes={"name": "Liechtenstein"})
    classy_xml_empty_fixture.country[0].rank = XmlElement(text=1)
    classy_xml_empty_fixture.country[0].year = XmlElement(text=2008)
    classy_xml_empty_fixture.country[0].gdppc = XmlElement(text=141100)
    classy_xml_empty_fixture.country[0].neighbor = XmlElement(
        attributes={"name": "Austria", "direction": "E"}
    )
    classy_xml_empty_fixture.country[0].neighbor = XmlElement(
        attributes={"name": "Switzerland", "direction": "W"}
    )

    classy_xml_empty_fixture.country = XmlElement()
    classy_xml_empty_fixture.country[1].name = "Singapore"
    classy_xml_empty_fixture.country[1].rank = XmlElement()
    classy_xml_empty_fixture.country[1].rank.text = 4
    classy_xml_empty_fixture.country[1].year = XmlElement()
    classy_xml_empty_fixture.country[1].year.text = 2011
    classy_xml_empty_fixture.country[1].gdppc = XmlElement()
    classy_xml_empty_fixture.country[1].gdppc.text = 59900
    classy_xml_empty_fixture.country[1].neighbor = XmlElement()
    classy_xml_empty_fixture.country[1].neighbor[0].name = "Malaysia"
    classy_xml_empty_fixture.country[1].neighbor[0].direction = "N"

    filepath = os.path.split(__file__)[0]
    gen_countries_filename = os.path.join(filepath, "countries_gen.xml")
    classy_xml_empty_fixture.save_as(gen_countries_filename)

    with open(gen_countries_filename) as file:
        countries_gen_text = file.read()
    os.remove(gen_countries_filename)

    filepath = os.path.split(__file__)[0]
    countries_filename = os.path.join(filepath, "countries.xml")
    with open(countries_filename) as file:
        countries_text = file.read()

    assert countries_gen_text == countries_text


def test_passing_xml_as_string():
    xml_str = """
        <root>
            <country name="Liechtenstein">
                <rank>1</rank>
                <year>2008</year>
                <gdppc>141100</gdppc>
                <neighbor name="Austria" direction="E"/>
                <neighbor name="Switzerland" direction="W"/>
            </country>
            <country name="Singapore">
                <rank>4</rank>
                <year>2011</year>
                <gdppc>59900</gdppc>
                <neighbor name="Malaysia" direction="N"/>
            </country>
        </root>
        """
    classy = ClassyXml(xml_str)
    assert hasattr(classy, "country")
    assert classy.country[0].name == "Liechtenstein"
    assert classy.country[0].rank.text == "1"
    assert classy.country[0].year.text == "2008"
    assert classy.country[0].gdppc.text == "141100"
    assert classy.country[0].neighbor[0].name == "Austria"
    assert classy.country[0].neighbor[0].direction == "E"
    assert classy.country[0].neighbor[1].name == "Switzerland"
    assert classy.country[0].neighbor[1].direction == "W"
    assert classy.country[1].name == "Singapore"
    assert classy.country[1].rank.text == "4"
    assert classy.country[1].year.text == "2011"
    assert classy.country[1].gdppc.text == "59900"
    assert classy.country[1].neighbor[0].name == "Malaysia"
    assert classy.country[1].neighbor[0].direction == "N"
