# gibberishpy

gibberishpy is a Python-based application designed to analyze and identify gibberish in a given string. The application leverages the principles of Markov Chains, a mathematical system that undergoes transitions from one state to other on a state space, to calculate both additive and multiplicative probabilities. gibberishpy allow users to build their own model with custom txt file.


## Usage Examples

Build Model
-----------

    from gibberishpy.scanner import GibberishScanner
    
    
    if __name__ == "__main__":
        scanner = GibberishScanner()
        scanner.build_model(corpus_path="path/to//corpus.txt", n_gram_size=2)
        scanner.save_model("transition_matrix_2d.tm", encoding="utf-8")

Scan Gibberish
--------------

    from gibberishpy.scanner import GibberishScanner
    
    
    if __name__ == "__main__":
        scanner = GibberishScanner()
        scanner.load_model(path="transition_matrix_2d.tm")
        additive_cum_proba, multiplicative_cum_proba = scanner.scan("ldfjgnkdfjnd")
        print(additive_cum_proba)
        print(multiplicative_cum_proba)
    
        # 0.00022810218978102192
        # 0.0
