typedef struct Bigram {
	int letter1AsciiCode;
	int letter2AsciiCode;
	double frequency;
} Bigram;

double test_single_layout(char* layout, int layout_length, Bigram* bigrams,
                          int bigrams_count, double* score_list);

void get_top_scores(char** layouts, long layout_count, double* scores, int nr_of_best,
                    int letters_per_layer, char** top_layouts, double* top_scores);
