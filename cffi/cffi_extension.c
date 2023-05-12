#include "cffi_extension.h"

double test_single_layout(char* layout, int layout_length, Bigram* bigrams,
                          int bigrams_count, double* score_list)
{
	int ascii_array[256] = {0};
	for (int j = 0; j < layout_length; j++) {
		ascii_array[(unsigned char)layout[j]] = j;
	}

	double score = 0.0;
	for (int i = 0; i < bigrams_count; i++) {
		Bigram bigram = bigrams[i];
		int row = ascii_array[bigram.letter1AsciiCode];
		int column = ascii_array[bigram.letter2AsciiCode];
		score += bigram.frequency * score_list[row*32 + column];
	}
	return score;
}
