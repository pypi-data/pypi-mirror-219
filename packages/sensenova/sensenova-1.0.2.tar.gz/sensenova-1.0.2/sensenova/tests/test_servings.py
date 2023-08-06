import json
import sensenova


def test_serving_create(model_id):
    result = sensenova.Serving.create(
        model=model_id,
        config={
            "run_time": 60
        }
    )
    print(result)


def test_serving_list():
    resp = sensenova.Serving.list()
    print(resp)


def test_serving_cancel(id):
    resp = sensenova.Serving.cancel(id)
    print(resp)


def test_serving_retrieve(id):
    resp = sensenova.Serving.retrieve(id)
    print(resp)


def test_serving_relaunch(id):
    resp = sensenova.Serving.relaunch(id)
    print(resp)


if __name__ == "__main__":
    id = "a0f0caee-1cfb-4a5c-b2ef-d041d80476cb"
    model_id = "llama-7b-test:wzh"
    # test_finetune_list()
    # test_serving_list()
    # test_serving_list()

    # test_serving_create(model_id)
    test_serving_cancel(id)
    # print(sensenova.Serving.delete(sid=id))
    test_serving_relaunch(id)
    # test_serving_retrieve(id)
    # test_serving_cancel()
    # test_serving_list()
