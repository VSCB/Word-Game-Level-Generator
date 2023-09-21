import pandas as pd

def parse_distribution(dist_str):
    """Parse a distribution string ("2x3, 3x4, 2x5") into a dictionary."""
    parts = dist_str.split(", ")
    return {int(part.split("x")[1]): int(part.split("x")[0]) for part in parts}

def get_correct_and_extra_words(row, distribution):
    """Split words into 'correct' and 'extra' based on the distribution."""
    correct, extra = [], []
    for length, required_count in distribution.items():
        words_of_length = row[f"{length}-letter words"].split(", ")
        correct.extend(words_of_length[:required_count])
        extra.extend(words_of_length[required_count:])
    return ", ".join(correct), ", ".join(extra)

def format_word(word):
    """Format word into comma-separated uppercase characters."""
    return ', '.join(list(word.upper()))

def load_used_words(file_path):
    """Load the used words from a file and return a list of them."""
    with open(file_path, 'r') as file:
        return [line.strip().replace(', ', '').replace(',', '').lower() for line in file.readlines()]

def satisfies_distribution(row, distribution, used_words):
    """Check if a row from the Excel satisfies the given distribution and doesn't have used words."""
    for length, required_count in distribution.items():
        col_name = f"{length}-letter words"
        if col_name in row and isinstance(row[col_name], str):
            words = row[col_name].split(", ")
            # Check for used words
            for word in words:
                if word.lower() in used_words:
                    return False
            actual_count = len(words)
            if actual_count < required_count:
                return False
        else:
            return False
    return True

def main():
    # Load the words from the Excels
    df = pd.read_excel("five_letter_word_lists.xlsx")
    df = df.dropna(subset=['3-letter words', '4-letter words', '5-letter words'])  # Drop rows with NaN values
    six_df = pd.read_excel("six_letter_word_lists.xlsx")
    six_df = six_df.dropna(subset=['3-letter words', '4-letter words', '5-letter words', '6-letter words'])  # Drop rows with NaN values

    # Load distributions
    with open("distribution.txt", 'r') as file:
        distributions = file.readlines()

    # Load used words
    used_words = load_used_words("used.txt")

    results = []
    for dist_str in distributions:
        dist = parse_distribution(dist_str.strip())

        # Choose the appropriate dataframe based on the distribution
        current_df = six_df if 6 in dist else df

        for _, row in current_df.iterrows():
            if satisfies_distribution(row, dist, used_words):
                row['base_word'] = format_word(row['base_word'])  # Format base_word
                for col in [f'{i}-letter words' for i in range(3, 7) if i in dist]:
                    row[col] = row[col].upper()
                correct, extra = get_correct_and_extra_words(row, dist)
                row["correct words"] = correct
                row["extra words"] = extra
                results.append(row)
                current_df.drop(_, axis=0, inplace=True)  # Remove the used row
                break

    if results:
        result_df = pd.DataFrame(results)
        result_df.to_excel("satisfied_distributions.xlsx", index=False)
    else:
        print("No word could satisfy any distribution.")

if __name__ == "__main__":
    main()
