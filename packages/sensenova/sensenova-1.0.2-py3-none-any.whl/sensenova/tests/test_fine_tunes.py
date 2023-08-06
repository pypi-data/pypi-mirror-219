import json
from tempfile import NamedTemporaryFile

import sensenova


def test_finetune_create():
    result = sensenova.FineTune.create(
        hyperparams= {
            "learning_rate": 0.0001,
            "lora_alpha": 32,
            "lora_dropout": 0.05,
            "lora_rank": 8,
            "lr_scheduler_type": "cosine",
            "max_steps": 10,
            "modules_to_save": "embed_tokens,lm_head",
            "save_steps": 10,
            "warmup_ratio": 0.03,
            "weight_decay": 0
        },
        model="nova-ptc-xs-v1",
        suffix="wz",
        training_file="12d1ba23-427c-42ad-af1a-d0b927b8e3b7"
    )
    print(result)


def test_finetune_list():
    resp = sensenova.FineTune.list()
    print(resp)

def test_finetune_cancel(id):
    resp = sensenova.FineTune.cancel(id)
    print(resp)


if __name__ == "__main__":
    id = 'ft-a3afd31f335447ac8157d8471789a11c'
    # test_finetune_list()
    # test_finetune_create()
    test_finetune_list()
    # res = sensenova.FineTune.retrieve(id=id)
    # print(res)
    # test_finetune_cancel(id=id)
    print(sensenova.FineTune.delete(sid=id))
    # test_finetune_list()
