typedef struct Bigram {
	int letter1AsciiCode;
	int letter2AsciiCode;
	double frequency;
} BigramC;

double test_single_layout(char* layout, int layout_length, BigramC* bigrams,
                          int bigrams_count, double score_list[][32]);

void get_top_scores(char** layouts, long layout_count, double* scores, int nr_of_best,
                    int letters_per_layer, char** top_layouts, double* top_scores);
