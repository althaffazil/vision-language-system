from datasets import load_dataset

def stream_ok_vqa(split="train"):
    dataset = load_dataset(
        "lmms-lab/OK-VQA",
        split=split,
        streaming=True
    )
    return dataset
