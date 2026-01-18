from pathlib import Path
import faker

faker = faker.Faker(locale="ru_RU")
DEFAULT_PATH = Path(__file__).parent / "test.txt"
DEFAULT_SECOND_PATH = Path(__file__).parent / "test2.txt"

def generate_test_file():
    with open(DEFAULT_PATH, "w", encoding="utf-8") as f:
        for i in range(100):
            f.write(faker.word() + "\n")
            
    with open(DEFAULT_SECOND_PATH, "w", encoding="utf-8") as f:
        for i in range(10):
            f.write(faker.word() + "\n")

if __name__ == "__main__":
    generate_test_file()
    print(f"Test file generated at {DEFAULT_PATH}")
