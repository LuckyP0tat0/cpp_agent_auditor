from datasets import load_dataset

def get_code_snippet() -> str:

    print("Загрузка датасета...")

    ds = load_dataset("claudios/DiverseVul", split="test")


    vuln_ds = ds.filter(lambda x: x["target"] == 1)

    code = vuln_ds[0]["func"]

    return code
