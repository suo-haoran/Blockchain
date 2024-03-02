from metadata.sample_metadata import Metadata

def test_json_dump():
    meta = Metadata("123", "456", "789", [{"123": "456"}])
    print(meta)