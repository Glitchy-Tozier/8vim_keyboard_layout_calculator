typedef struct Bigram {
	int letter1AsciiCode;
	int letter2AsciiCode;
	double frequency;
} Bigram;

double test_single_layout(char* layout, int layout_length, Bigram* bigrams,
                          int bigrams_count, double* score_list);
