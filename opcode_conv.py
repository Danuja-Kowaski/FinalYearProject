from pyevmasm import disassemble_hex
from opcodes import opcode_seq
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from tensorflow.keras.models import model_from_json
from pathlib import Path
import numpy as np


# Enter the bytecode to disassemble


def convert_to_op(bytecode):
    opcodes = disassemble_hex(bytecode)
    print(opcodes)
    opcode_names = [line.split()[0] for line in opcodes.split('\n') if line.strip()]
    opcode_values = []
    for opcode in opcode_names:
        if opcode in opcode_seq:
            opcode_values.append(int(opcode_seq[opcode], 16))
        else:
            print(f"Opcode value not found for opcode name {opcode}")
    opcode_values = [opcode_seq[op] for op in opcode_names]
    opcode_values_str = " ".join([str(val) for val in opcode_values])
    print(opcode_values_str)
    return opcode_values_str


def preprocess(contract):
    try:
        if not contract:
            raise ValueError("Input contract is empty.")
        print("Converting opcodes")
        contract = [contract]
        tokenizer = Tokenizer(num_words=151)
        tokenizer.fit_on_texts(contract)
        contract = tokenizer.texts_to_sequences(contract)
        # Pad the sequences to a fixed length
        max_length = 5000  # 3000
        contract = pad_sequences(contract, maxlen=max_length, padding='post')
        print("Completed preprocessing.")
        return contract
    except Exception as e:
        print(f"Error: {e}")
        return None


def load_model():
    try:
        f = Path("cnn_model2_structure.json")
        if not f.exists():
            raise FileNotFoundError("Model structure file not found.")
        model_structure = f.read_text()
        model = model_from_json(model_structure)
        if not Path("cnn_model2_weights.h5").exists():
            raise FileNotFoundError("Model weights file not found.")
        model.load_weights("cnn_model2_weights.h5")
        print("Loaded model.")
        return model
    except Exception as e:
        print(f"Error: {e}")
        return None


def run_predictions(model, contract):
    try:
        category_labels = [0, 2, 1]
        # Make a prediction on the single input
        pre_contract = preprocess(contract)
        if pre_contract is None:
            raise ValueError("Failed to preprocess the contract.")
        print("Starting predictions")
        predictions = model.predict(pre_contract)
        print("Completed predictions")
        if len(predictions) == 0:
            raise ValueError("Failed to make predictions.")
        classindex = np.argmax(predictions)
        print(category_labels[classindex])
        print(predictions)
        return category_labels[classindex]
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    testde = "60 60 52 60 36 10 61 57 60 35 7c 90 04 63 16 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 5b 60 80 fd 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 73 16 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 0b 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 73 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 16 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 19 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 7e 19 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 7e 19 16 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 7e 19 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 0b 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 19 16 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 15 15 15 15 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 0b 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 73 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 60 80 80 35 90 60 01 90 91 90 50 50 61 56 5b 60 51 80 82 81 52 60 01 91 50 50 60 51 80 91 03 90 f3 5b 61 60 80 80 35 90 60 01 90 91 90 80 35 60 19 16 90 60 01 90 91 90 50 50 61 56 5b 00 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 83 90 91 90 91 61 0a 81 54 81 60 02 19 16 90 83 60 16 02 17 90 55 50 50 61 82 61 56 5b 82 60 01 60 83 60 16 60 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 60 80 83 60 01 60 84 73 16 73 16 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 60 0b 60 0b 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 90 54 90 61 0a 90 04 60 0b 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 61 0a 81 54 81 60 02 19 16 90 83 60 0b 60 16 02 17 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 60 0b 60 0b 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 60 0b 60 0b 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 73 16 73 16 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 60 90 54 90 61 0a 90 04 73 16 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 60 61 0a 81 54 81 73 02 19 16 90 83 73 16 02 17 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 73 16 73 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 73 16 73 16 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 60 80 83 60 01 60 84 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 54 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 81 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 60 80 83 60 01 60 84 60 16 60 16 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 60 16 60 16 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 90 54 90 61 0a 90 04 60 16 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 61 0a 81 54 81 60 02 19 16 90 83 60 16 02 17 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 60 16 60 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 60 16 60 16 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 01 60 83 90 91 90 91 50 90 60 19 16 90 55 50 61 82 61 56 5b 82 60 01 60 83 60 19 16 60 19 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 83 90 91 90 91 61 0a 81 54 81 60 02 19 16 90 83 7f 90 04 02 17 90 55 50 50 61 82 61 56 5b 82 60 01 60 83 7e 19 16 7e 19 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 60 80 83 60 01 60 84 7e 19 16 7e 19 16 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 54 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 81 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 60 80 83 60 01 60 84 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 7e 19 16 7e 19 16 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 90 54 90 61 0a 90 04 7f 02 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 61 0a 81 54 81 60 02 19 16 90 83 7f 90 04 02 17 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 7e 19 16 7e 19 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 7e 19 16 7e 19 16 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 60 80 83 60 01 60 84 60 0b 60 0b 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 60 80 83 60 01 60 84 60 19 16 60 19 16 81 52 60 01 90 81 52 60 01 60 20 54 11 90 50 92 91 50 50 56 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 01 60 83 90 91 90 91 50 55 50 61 82 61 56 5b 82 60 01 60 83 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 60 91 82 82 04 01 91 90 06 83 90 91 90 91 61 0a 81 54 81 60 02 19 16 90 83 60 0b 60 16 02 17 90 55 50 50 61 82 61 56 5b 82 60 01 60 83 60 0b 60 0b 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 01 60 83 90 91 90 91 50 55 50 61 82 61 56 5b 82 60 01 60 83 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 61 82 82 61 56 5b 15 15 61 57 7f 61 83 61 56 5b 10 15 15 61 57 fe 5b 81 60 01 80 54 80 60 01 82 81 61 91 90 61 56 5b 91 60 52 60 60 20 90 01 60 83 90 91 90 91 61 0a 81 54 81 73 02 19 16 90 83 73 16 02 17 90 55 50 50 61 82 61 56 5b 82 60 01 60 83 73 16 73 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 5b 50 50 56 5b 60 81 60 01 80 54 90 50 90 50 91 90 50 56 5b 60 80 61 84 84 61 56 5b 15 61 57 83 60 01 60 84 60 19 16 60 19 16 81 52 60 01 90 81 52 60 01 60 20 54 91 50 83 60 01 60 61 86 61 56 5b 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 54 90 50 80 84 60 01 60 84 03 81 54 81 10 15 15 61 57 fe 5b 90 60 52 60 60 20 90 01 81 60 19 16 90 55 50 83 60 01 80 54 80 91 90 60 90 03 61 91 90 61 56 5b 50 81 84 60 01 60 83 60 19 16 60 19 16 81 52 60 01 90 81 52 60 01 60 20 81 90 55 50 83 60 01 60 84 60 19 16 60 19 16 81 52 60 01 90 81 52 60 01 60 20 60 90 55 5b 50 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 60 01 60 90 04 81 60 01 60 90 04 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 60 01 60 90 04 81 60 01 60 90 04 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 60 01 60 90 04 81 60 01 60 90 04 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 60 01 60 90 04 81 60 01 60 90 04 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 60 01 60 90 04 81 60 01 60 90 04 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 60 01 60 90 04 81 60 01 60 90 04 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 81 54 81 83 55 81 81 15 11 61 57 81 83 60 52 60 60 20 91 82 01 91 01 61 91 90 61 56 5b 5b 50 50 50 56 5b 61 91 90 5b 80 82 11 15 61 57 60 81 60 90 55 50 60 01 61 56 5b 50 90 56 5b 90 56 5b 61 91 90 5b 80 82 11 15 61 57 60 81 60 90 55 50 60 01 61 56 5b 50 90 56 5b 90 56 5b 61 91 90 5b 80 82 11 15 61 57 60 81 60 90 55 50 60 01 61 56 5b 50 90 56 5b 90 56 00 a1 65 20 72 fd 15 02 96 6f"

    test = "60 60 52 36 15 61 57 63 7c 60 35 04 16 63 81 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 80 63 14 61 57 5b 5b 60 34 11 15 61 57 33 60 60 60 0a 03 16 7f 34 60 51 90 81 52 60 01 60 51 80 91 03 90 a2 5b 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 60 51 60 60 60 0a 03 90 91 16 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 60 60 0a 03 60 35 16 61 56 5b 60 51 90 15 15 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 60 60 60 0a 03 60 35 16 61 56 5b 60 51 90 15 15 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 60 60 0a 03 60 35 81 16 90 60 35 16 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 60 60 0a 03 60 35 16 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 35 15 15 60 35 15 15 61 56 5b 60 51 90 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 60 60 0a 03 60 35 81 16 90 60 35 16 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 60 51 90 15 15 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 60 51 90 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 60 51 60 60 60 0a 03 85 16 81 52 60 81 01 84 90 52 81 15 15 60 82 01 52 60 60 82 01 81 81 52 84 54 60 60 19 61 60 84 16 15 02 01 90 91 16 04 91 83 01 82 90 52 90 60 83 01 90 85 90 80 15 61 57 80 60 10 61 57 61 80 83 54 04 02 83 52 91 60 01 91 61 56 5b 82 01 91 90 60 52 60 60 20 90 5b 81 54 81 52 90 60 01 90 60 01 80 83 11 61 57 82 90 03 60 16 82 01 91 5b 50 50 95 50 50 50 50 50 50 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 61 56 5b 60 51 60 80 82 52 81 90 81 01 83 81 81 51 81 52 60 01 91 50 80 51 90 60 01 90 60 02 80 83 83 60 5b 83 81 10 15 61 57 80 82 01 51 81 84 01 52 5b 60 01 61 56 5b 50 50 50 50 90 50 01 92 50 50 50 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 60 35 60 35 15 15 60 35 15 15 61 56 5b 60 51 60 80 82 52 81 90 81 01 83 81 81 51 81 52 60 01 91 50 80 51 90 60 01 90 60 02 80 83 83 60 5b 83 81 10 15 61 57 80 82 01 51 81 84 01 52 5b 60 01 61 56 5b 50 50 50 50 90 50 01 92 50 50 50 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 60 60 0a 03 60 35 81 16 90 60 35 16 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 60 51 60 80 82 52 81 90 81 01 83 81 81 51 81 52 60 01 91 50 80 51 90 60 01 90 60 02 80 83 83 60 5b 83 81 10 15 61 57 80 82 01 51 81 84 01 52 5b 60 01 61 56 5b 50 50 50 50 90 50 01 92 50 50 50 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 61 56 5b 60 51 90 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 80 35 60 60 60 0a 03 16 90 60 80 35 91 90 60 90 60 35 90 81 01 90 83 01 35 80 60 60 82 01 81 90 04 81 02 01 60 51 90 81 01 60 52 81 81 52 92 91 90 60 84 01 83 83 80 82 84 37 50 94 96 50 61 95 50 50 50 50 50 50 56 5b 60 51 90 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 61 56 5b 60 51 90 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 61 56 5b 60 51 90 81 52 60 01 60 51 80 91 03 90 f3 5b 34 15 61 57 60 80 fd 5b 61 60 35 61 56 5b 00 5b 34 15 61 57 60 80 fd 5b 61 60 60 60 0a 03 60 35 16 60 60 35 16 61 56 5b 00 5b 60 80 54 82 90 81 10 61 57 fe 5b 90 60 52 60 60 20 90 01 60 5b 91 50 54 90 61 0a 90 04 60 60 60 0a 03 16 81 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 90 20 54 60 16 15 15 61 57 60 80 fd 5b 60 82 81 52 60 60 90 81 52 60 80 83 20 33 60 60 60 0a 03 81 16 85 52 92 52 90 91 20 54 83 91 90 60 16 15 15 61 57 60 80 fd 5b 60 84 81 52 60 81 90 52 60 90 20 60 01 54 84 90 60 16 15 61 57 60 80 fd 5b 60 85 81 52 60 60 90 81 52 60 80 83 20 60 60 60 0a 03 33 16 80 85 52 92 52 91 82 90 20 80 54 60 19 16 90 55 86 91 7f 90 51 60 51 80 91 03 90 a3 5b 5b 50 5b 50 50 5b 50 50 56 5b 60 60 52 60 90 81 52 60 90 20 54 60 16 81 56 5b 60 60 90 81 52 60 92 83 52 60 80 84 20 90 91 52 90 82 52 90 20 54 60 16 81 56 5b 61 61 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 81 20 54 90 91 90 60 16 15 15 61 57 60 80 fd 5b 60 60 51 90 81 01 60 52 80 60 81 52 60 01 7f 81 52 60 01 60 81 52 50 92 50 83 60 84 01 52 61 85 60 85 61 56 5b 91 50 83 60 60 60 0a 03 16 7f 83 60 51 90 81 52 60 01 60 51 80 91 03 90 a2 5b 5b 50 50 50 50 50 56 5b 61 61 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 81 20 54 90 91 90 60 16 15 15 61 57 60 80 fd 5b 60 80 51 90 81 01 60 52 60 81 52 7f 60 82 01 52 92 50 61 84 60 85 61 56 5b 91 50 7f 82 60 51 90 81 52 60 01 60 51 80 91 03 90 a1 5b 5b 50 50 50 50 56 5b 60 80 5b 60 54 81 10 15 61 57 83 80 15 61 57 50 60 81 81 52 60 81 90 52 60 90 20 60 01 54 60 16 15 5b 80 61 57 50 82 80 15 61 57 50 60 81 81 52 60 81 90 52 60 90 20 60 01 54 60 16 5b 5b 15 61 57 60 82 01 91 50 5b 5b 60 01 61 56 5b 5b 50 92 91 50 50 56 5b 61 61 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 81 20 54 90 91 90 60 16 15 15 61 57 60 80 fd 5b 60 60 51 90 81 01 60 52 80 60 81 52 60 01 7f 81 52 60 01 60 81 52 50 92 50 83 60 84 01 52 61 85 60 85 61 56 5b 91 50 83 60 60 60 0a 03 16 7f 83 60 51 90 81 52 60 01 60 51 80 91 03 90 a2 5b 5b 50 50 50 50 50 56 5b 60 80 80 5b 60 54 81 10 15 61 57 60 84 81 52 60 60 52 60 81 20 60 80 54 91 92 91 84 90 81 10 61 57 fe 5b 90 60 52 60 60 20 90 01 60 5b 90 54 60 60 60 0a 03 61 92 90 92 0a 90 04 16 81 52 60 81 01 91 90 91 52 60 01 60 20 54 60 16 15 61 57 60 82 01 91 50 5b 60 54 82 14 15 61 57 60 92 50 61 56 5b 5b 60 01 61 56 5b 5b 50 50 91 90 50 56 5b 60 80 5b 60 54 81 10 15 61 57 60 83 81 52 60 60 52 60 81 20 60 80 54 91 92 91 84 90 81 10 61 57 fe 5b 90 60 52 60 60 20 90 01 60 5b 90 54 60 60 60 0a 03 61 92 90 92 0a 90 04 16 81 52 60 81 01 91 90 91 52 60 01 60 20 54 60 16 15 61 57 60 82 01 91 50 5b 5b 60 01 61 56 5b 5b 50 91 90 50 56 5b 60 60 81 90 52 90 81 52 60 90 20 80 54 60 82 01 54 60 83 01 54 60 60 60 0a 03 90 92 16 92 90 91 60 90 91 01 90 60 16 84 56 5b 61 61 56 5b 60 80 54 80 60 02 60 01 60 51 90 81 01 60 52 80 92 91 90 81 81 52 60 01 82 80 54 80 15 61 57 60 02 82 01 91 90 60 52 60 60 20 90 5b 81 54 60 60 60 0a 03 16 81 52 60 90 91 01 90 60 01 80 83 11 61 57 5b 50 50 50 50 50 90 50 5b 90 56 5b 61 61 56 5b 61 61 56 5b 60 80 60 54 60 51 80 59 10 61 57 50 59 5b 90 80 82 52 80 60 02 60 01 82 01 60 52 5b 50 92 50 60 91 50 60 90 50 5b 60 54 81 10 15 61 57 85 80 15 61 57 50 60 81 81 52 60 81 90 52 60 90 20 60 01 54 60 16 15 5b 80 61 57 50 84 80 15 61 57 50 60 81 81 52 60 81 90 52 60 90 20 60 01 54 60 16 5b 5b 15 61 57 80 83 83 81 51 81 10 61 57 fe 5b 60 90 81 02 90 91 01 01 52 60 91 90 91 01 90 5b 5b 60 01 61 56 5b 87 87 03 60 51 80 59 10 61 57 50 59 5b 90 80 82 52 80 60 02 60 01 82 01 60 52 5b 50 93 50 87 90 50 5b 86 81 10 15 61 57 82 81 81 51 81 10 61 57 fe 5b 90 60 01 90 60 02 01 51 84 89 83 03 81 51 81 10 61 57 fe 5b 60 90 81 02 90 91 01 01 52 5b 60 01 61 56 5b 5b 50 50 50 94 93 50 50 50 50 56 5b 61 61 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 81 20 54 90 91 90 60 16 15 15 61 57 60 80 fd 5b 60 60 51 90 81 01 60 52 80 60 81 52 60 01 7f 81 52 60 01 60 81 52 50 92 50 83 60 84 01 52 61 85 60 85 61 56 5b 91 50 83 60 60 60 0a 03 16 7f 83 60 51 90 81 52 60 01 60 51 80 91 03 90 a2 5b 5b 50 50 50 50 50 56 5b 61 61 56 5b 61 61 56 5b 60 54 60 90 81 90 60 51 80 59 10 61 57 50 59 5b 90 80 82 52 80 60 02 60 01 82 01 60 52 5b 50 92 50 60 91 50 60 90 50 5b 60 54 81 10 15 61 57 60 85 81 52 60 60 52 60 81 20 60 80 54 91 92 91 84 90 81 10 61 57 fe 5b 90 60 52 60 60 20 90 01 60 5b 90 54 60 60 60 0a 03 61 92 90 92 0a 90 04 16 81 52 60 81 01 91 90 91 52 60 01 60 20 54 60 16 15 61 57 60 80 54 82 90 81 10 61 57 fe 5b 90 60 52 60 60 20 90 01 60 5b 90 54 90 61 0a 90 04 60 60 60 0a 03 16 83 83 81 51 81 10 61 57 fe 5b 60 60 60 0a 03 90 92 16 60 92 83 02 90 91 01 90 91 01 52 60 91 90 91 01 90 5b 5b 60 01 61 56 5b 81 60 51 80 59 10 61 57 50 59 5b 90 80 82 52 80 60 02 60 01 82 01 60 52 5b 50 93 50 60 90 50 5b 81 81 10 15 61 57 82 81 81 51 81 10 61 57 fe 5b 90 60 01 90 60 02 01 51 84 82 81 51 81 10 61 57 fe 5b 60 60 60 0a 03 90 92 16 60 92 83 02 90 91 01 90 91 01 52 5b 60 01 61 56 5b 5b 50 50 50 91 90 50 56 5b 60 54 81 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 90 20 54 60 16 15 15 61 57 60 80 fd 5b 60 82 81 52 60 81 90 52 60 90 20 54 82 90 60 60 60 0a 03 16 15 15 61 57 60 80 fd 5b 60 83 81 52 60 60 90 81 52 60 80 83 20 33 60 60 60 0a 03 81 16 85 52 92 52 90 91 20 54 84 91 90 60 16 15 61 57 60 80 fd 5b 60 85 81 52 60 60 81 81 52 60 80 84 20 60 60 60 0a 03 33 16 80 86 52 92 52 92 83 90 20 80 54 60 19 16 90 92 17 90 91 55 86 91 7f 90 51 60 51 80 91 03 90 a3 61 85 61 56 5b 5b 5b 50 50 5b 50 5b 50 50 56 5b 60 61 84 84 84 61 56 5b 90 50 61 81 61 56 5b 5b 93 92 50 50 50 56 5b 60 81 56 5b 60 54 81 56 5b 60 81 81 52 60 81 90 52 60 90 20 60 01 54 81 90 60 16 15 61 57 60 80 fd 5b 61 82 61 56 5b 15 61 57 60 82 81 52 60 81 90 52 60 90 81 90 20 60 81 01 80 54 60 19 16 60 90 81 17 90 91 55 81 54 90 82 01 54 60 60 60 0a 03 90 91 16 92 90 91 60 01 90 51 80 82 80 54 60 81 60 16 15 61 02 03 16 60 90 04 80 15 61 57 80 60 10 61 57 61 80 83 54 04 02 83 52 91 60 01 91 61 56 5b 82 01 91 90 60 52 60 60 20 90 5b 81 54 81 52 90 60 01 90 60 01 80 83 11 61 57 82 90 03 60 16 82 01 91 5b 50 50 91 50 50 60 60 51 80 83 03 81 85 87 61 5a 03 f1 92 50 50 50 15 61 57 81 7f 60 51 60 51 80 91 03 90 a2 61 56 5b 81 7f 60 51 60 51 80 91 03 90 a2 60 82 81 52 60 81 90 52 60 90 20 60 01 80 54 60 19 16 90 55 5b 5b 5b 5b 50 50 56 5b 61 61 56 5b 33 60 60 60 0a 03 81 16 60 90 81 52 60 60 52 60 81 20 54 90 91 90 60 16 15 15 61 57 60 80 fd 5b 60 60 51 90 81 01 60 52 80 60 81 52 60 01 7f 81 52 60 01 60 81 52 50 92 50 83 60 81 11 15 61 57 fe 5b 7f 02 83 60 81 51 81 10 61 57 fe 5b 90 60 01 01 90 7e 19 16 90 81 60 1a 90 53 50 61 85 60 85 61 56 5b 91 50 83 60 81 11 15 61 57 fe 5b 7f 83 60 51 90 81 52 60 01 60 51 80 91 03 90 a2 5b 5b 50 50 50 50 50 56 5b 60 83 60 60 60 0a 03 81 16 15 15 61 57 60 80 fd 5b 60 54 91 50 60 60 51 90 81 01 60 90 81 52 60 60 60 0a 03 87 16 82 52 60 80 83 01 87 90 52 81 83 01 86 90 52 60 60 84 01 81 90 52 85 81 52 90 81 90 52 20 81 51 81 54 73 19 16 60 60 60 0a 03 91 90 91 16 17 81 55 60 82 01 51 81 60 01 55 60 82 01 51 81 60 01 90 80 51 61 92 91 60 01 90 61 56 5b 50 60 82 01 51 60 91 90 91 01 80 54 60 19 16 91 15 15 91 90 91 17 90 55 50 60 80 54 60 01 90 55 81 7f 60 51 60 51 80 91 03 90 a2 5b 5b 50 93 92 50 50 50 56 5b 60 60 51 90 81 01 60 52 60 81 52 90 56 5b 60 60 51 90 81 01 60 52 60 81 52 90 56 5b 60 60 51 90 81 01 60 52 60 81 52 90 56 5b 82 80 54 60 81 60 16 15 61 02 03 16 60 90 04 90 60 52 60 60 20 90 60 01 60 90 04 81 01 92 82 60 10 61 57 80 51 60 19 16 83 80 01 17 85 55 61 56 5b 82 80 01 60 01 85 55 82 15 61 57 91 82 01 5b 82 81 11 15 61 57 82 51 82 55 91 60 01 91 90 60 01 90 61 56 5b 5b 50 61 92 91 50 61 56 5b 50 90 56 5b 61 91 90 5b 80 82 11 15 61 57 60 81 55 60 01 61 56 5b 50 90 56 5b 90 56 00 a1 65 20 52 60 51 1a fd 7f"
    model = load_model()
    pred = run_predictions(model, testde)
    print(pred)