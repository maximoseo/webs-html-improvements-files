import unittest

from n8n_template_extractor import extract_html_nodes, identify_domain, sanitize_filename_part


class N8NTemplateExtractorTests(unittest.TestCase):
    def test_extracts_html_from_supported_node_types_and_preserves_expressions(self):
        workflow = {
            'name': 'Example',
            'nodes': [
                {'name': 'HTML', 'type': 'n8n-nodes-base.html', 'parameters': {'html': '<h1>{{$json.title}}</h1>'}},
                {'name': 'Code', 'type': 'n8n-nodes-base.code', 'parameters': {'jsCode': "return '<table>{{$json.price}}</table>';"}},
                {'name': 'Set', 'type': 'n8n-nodes-base.set', 'parameters': {'values': {'string': [{'name': 'body', 'value': '<html>{{$node["A"].json.x}}</html>'}]}}},
                {'name': 'Function', 'type': 'n8n-nodes-base.function', 'parameters': {'functionCode': "const x = '<table>{{ $env.URL }}</table>';"}},
                {'name': 'Email', 'type': 'n8n-nodes-base.emailSend', 'parameters': {'html': '<p>{{$workflow.name}}</p>'}},
            ],
        }
        nodes = extract_html_nodes(workflow)
        self.assertEqual(len(nodes), 5)
        combined = '\n'.join(n['html_content'] for n in nodes)
        self.assertIn('{{$json.title}}', combined)
        self.assertIn('{{$node["A"].json.x}}', combined)
        self.assertIn('{{ $env.URL }}', combined)
        self.assertIn('{{$workflow.name}}', combined)

    def test_identifies_domain_from_tags_urls_and_name(self):
        workflow = {
            'name': 'Newsletter for maximo-seo.ai',
            'tags': [{'name': 'client'}, {'name': 'topsun.co.il'}],
            'nodes': [{'parameters': {'url': 'https://blog.example.com/path'}}],
        }
        info = identify_domain(workflow)
        self.assertIn('blog.example.com', info['domains_found'])
        self.assertIn('topsun.co.il', info['domains_found'])
        self.assertIn(info['primary_domain'], info['domains_found'])

    def test_sanitize_filename_part(self):
        self.assertEqual(sanitize_filename_part('My Workflow: שלום / test'), 'my-workflow-test')
        self.assertEqual(sanitize_filename_part(''), 'untitled')


if __name__ == '__main__':
    unittest.main()
