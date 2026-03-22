import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cohere_integration as ci


class DummyGen:
    def __init__(self, text):
        self.text = text


class DummyMsgContent:
    def __init__(self, text):
        self.text = text


class DummyMessage:
    def __init__(self, text):
        self.content = [DummyMsgContent(text)]


class DummyResponse:
    def __init__(self, text):
        self.message = DummyMessage(text)
        self.generations = [DummyGen(text)]


class DummyClient:
    def __init__(self, response):
        self._response = response

    def chat(self, **kwargs):
        return self._response


def test_call_cohere_generate_subtasks_parses_list(monkeypatch):
    expected = ['[Plan] -> A', '[Design] -> B', '[Execute] -> C']
    monkeypatch.setattr(ci, '_get_cohere_client', lambda: DummyClient(DummyResponse(str(expected))))

    result = ci.call_cohere_generate_subtasks('Generate a plan')

    assert result == expected


def test_call_cohere_generate_subtasks_rejects_short_list(monkeypatch):
    monkeypatch.setattr(ci, '_get_cohere_client', lambda: DummyClient(DummyResponse("['One']")))

    with pytest.raises(ValueError, match='between 3 and 5'):  # ensures contract enforcement
        ci.call_cohere_generate_subtasks('Too short')


def test_call_cohere_generate_subtasks_rejects_non_list(monkeypatch):
    class FakeResponse:
        def __init__(self):
            self.generations = [DummyGen("{'a': 1}")]
            self.message = DummyMessage("{'a': 1}")

    monkeypatch.setattr(ci, '_get_cohere_client', lambda: DummyClient(FakeResponse()))

    with pytest.raises(ValueError, match='not a list'):
        ci.call_cohere_generate_subtasks('Invalid format')


def test_get_cohere_client_requires_api_key(monkeypatch):
    monkeypatch.delenv('COHERE_API_KEY', raising=False)

    with pytest.raises(EnvironmentError, match='COHERE_API_KEY environment variable must be set'):
        ci._get_cohere_client()


def test_get_cohere_client_import_error(monkeypatch):
    import builtins as bl
    real_import = bl.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == 'cohere':
            raise ImportError('cohere not installed')
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(bl, '__import__', fake_import)

    with pytest.raises(ImportError, match='Cohere SDK is required for AI tasks'):
        ci._get_cohere_client()


def test_call_cohere_generate_subtasks_output_style(monkeypatch):
    class OutputResponse:
        def __init__(self, text):
            self.message = DummyMessage(text)
            self.output = [type('X', (), {'content': [DummyMsgContent(text)]})()]

    monkeypatch.setattr(ci, '_get_cohere_client', lambda: DummyClient(OutputResponse("['A', 'B', 'C']")))

    result = ci.call_cohere_generate_subtasks('Use output-style result')
    assert result == ['A', 'B', 'C']


def test_call_cohere_generate_subtasks_dict_style(monkeypatch):
    class DictResponse(dict):
        def __init__(self, value):
            super().__init__(value)
            self.message = DummyMessage('ignored')

    payload = DictResponse({'output': [{'text': "['A', 'B', 'C']"}]})
    monkeypatch.setattr(ci, '_get_cohere_client', lambda: DummyClient(payload))

    result = ci.call_cohere_generate_subtasks('Use dict-style result')
    assert result == ['A', 'B', 'C']


def test_call_cohere_generate_subtasks_invalid_syntax(monkeypatch):
    monkeypatch.setattr(ci, '_get_cohere_client', lambda: DummyClient(DummyResponse("[A, B, C]")))

    with pytest.raises(ValueError, match='Cohere response is not a valid Python list'):
        ci.call_cohere_generate_subtasks('Bad syntax')

