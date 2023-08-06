import io
import json
from tempfile import NamedTemporaryFile
import sensenova


def test_knowledge_base_add_file(id, description="1Test client??"):
    result = sensenova.KnowledgeBase.add_file(id=id, description=description)
    print(result)
    return result["url"]


def test_knowledge_base_list():
    result = sensenova.KnowledgeBase.list()
    print(result)


def test_knowledge_base_retrieve(id="mrkd"):
    result = sensenova.KnowledgeBase.retrieve(id=id)
    print(result)


def test_knowledge_base_delete(id):
    result = sensenova.KnowledgeBase.delete(sid=id)
    print(result)


def test_knowledge_base_upload(url):
    payload = {
        "qa_lst": [
            {
                "std_q": "xxx",
                "simi_qs": ["xxx", "xxx"],
                "answer": "xxx",
            },
            {
                "std_q": "xxx",
                "simi_qs": ["xxx", "xxx"],
                "answer": "xxx",
            },
        ],
        "text_lst": [
            "xxx",
            "xxx"
        ]
    }

    result = sensenova.KnowledgeBase.upload_file(aoss_url=url, file=io.StringIO(json.dumps(payload, ensure_ascii=False)))
    print(result)


def test_knowledge_base_download(id="mrkd", file_id="1"):
    result = sensenova.KnowledgeBase.download(id=id, file_id=file_id)
    print(result.decode('utf-8'))


def test_knowledge_base_create(description="Test client"):
    result = sensenova.KnowledgeBase.create(description=description)
    print(result)


# test_knowledge_base_list()
if __name__ == "__main__":
    id = "sf88e224517394ba0aceb9917efefd123"
    file_id = "9cb27fb844d04ef9b16806843f63ca15"
    test_knowledge_base_list()
    # test_knowledge_base_delete(id=id)
    # test_knowledge_base_download(id=id)
    # test_knowledge_base_create()
    # url = test_knowledge_base_add_file(id=id, description="How are YOU!")
    # test_knowledge_base_upload(url)
    # test_knowledge_base_retrieve(id=id)
    # test_knowledge_base_delete(id=id)
    # test_knowledge_base_list()
    test_knowledge_base_download(id=id, file_id=file_id)
