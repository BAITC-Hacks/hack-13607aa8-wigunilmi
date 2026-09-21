import re
from difflib import SequenceMatcher

def load_faq(filepath="faq.txt"):
    faqs = []
    with open(filepath, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            q, a = "", ""
            for line in lines:
                if line.startswith("Вопрос:"):
                    q = line.replace("Вопрос:", "").strip()
                elif line.startswith("Ответ:"):
                    a = line.replace("Ответ:", "").strip()
            if q and a:
                faqs.append({"question": q, "answer": a})
    return faqs

def get_words(text):
    return set(re.findall(r'\w+', text.lower()))

def find_best_answer(user_query, faqs, threshold=0.20):
    user_words = get_words(user_query)
    if not user_words:
        return "не знаю"

    best_score = 0.0
    best_answer = "не знаю"

    for item in faqs:
        q_words = get_words(item["question"])
        
        # Пересечение ключевых слов
        intersection = user_words.intersection(q_words)
        word_score = len(intersection) / max(len(user_words), 1)

        # Сходство последовательностей символов
        seq_score = SequenceMatcher(None, user_query.lower(), item["question"].lower()).ratio()

        # Итоговый метрический балл
        score = max(word_score, seq_score)

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score < threshold:
        return "не знаю"

    return best_answer

def main():
    try:
        faqs = load_faq()
    except FileNotFoundError:
        print("Ошибка: Файл faq.txt не найден.")
        return

    print("--- FAQ-бот запущен. Задайте вопрос (или введите 'выход' для завершения) ---")

    while True:
        try:
            user_input = input("\nВы: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input.lower() in ["выход", "exit", "quit"]:
            print("Бот: До свидания!")
            break

        answer = find_best_answer(user_input, faqs)
        print(f"Бот: {answer}")

if __name__ == "__main__":
    main()