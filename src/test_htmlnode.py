import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # props_to_html tests
    def test_multiple_props(self):
        node = HTMLNode("a", "Click", None, {"class": "button"})
        result = node.props_to_html()
        self.assertEqual(result, ' class="button"')

    def test_with_none(self):
        node = HTMLNode("b", "Click", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_with_empty_dict(self):
        node = HTMLNode("c", "Click", None, {})
        result = node.props_to_html()
        self.assertEqual(result, "")

    # to_html tests
    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_to_html_val_error(self):
        node = LeafNode("i", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_raw_val(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # ParentNode tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
