#include "cffi_extension.h"
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

double
test_single_layout(char* layout, int layout_length, BigramC* bigrams,
                   int bigrams_count, double score_list[][32]) {
	// ascii_array is a map:
	// index/key = numeric value of a character; value = position
	int ascii_array[256] = {0};
	for (int j = 0; j < layout_length; j++) {
		ascii_array[(unsigned char)layout[j]] = j;
	}

	// calculate score: sum of the scores for every bigram
	double score = 0.0;
	for (int i = 0; i < bigrams_count; i++) {
		BigramC bigram = bigrams[i];
		int row = ascii_array[bigram.letter1AsciiCode];
		int column = ascii_array[bigram.letter2AsciiCode];
		score += bigram.frequency * score_list[row][column];
	}
	return score;
}

// a pair of a layout and its score
typedef struct ScoredLayout {
	char* layout;
	double score;
} ScoredLayout;

static int
cmplayoutp(const void *p1, const void *p2) {
	return ((ScoredLayout*)p1)->score > ((ScoredLayout*)p2)->score;
}

static double
average(double* array, long count) {
	double sum = 0.0;
	for (long i = 0; i < count; i++) {
		sum += array[i];
	}
	return sum / (double)count;
}

// calculate average of all array entries i for which indices[i] is true
static double
average_of_selected(double* array, long count, bool* indices, long selection_count) {
	double sum = 0.0;
	for (long i = 0; i < count; i++) {
		if (indices[i])
			sum += array[i];
	}
	return sum / (double)selection_count;
}

void
get_top_scores(char** layouts, long layout_count, double* scores, int nr_of_best,
               int letters_per_layer, char** top_layouts, double* top_scores) {
	// Returns the best [whatever you set "nrOfBestPermutations" to] layouts with their scores.
	// The LAST items of those lists should be the best ones.

	// Make sure we don't try to get more scores than actually exist
	if (nr_of_best > layout_count)
		nr_of_best = layout_count;

	// create array indices_to_keep on the heap because it's to large for the stack
	// (for some function calls)
	long array_size = sizeof(bool) * layout_count;
	bool* indices_to_keep = malloc(array_size);
	memset(indices_to_keep, true, array_size);

	// BEFORE sorting the lists, make sure they're not unnecessarily large
	long score_count = layout_count;
	long new_length = score_count;
	int max_needed = nr_of_best*3;
	if (max_needed < letters_per_layer*2)
		max_needed = letters_per_layer*2;
	if (score_count > max_needed) {
		while (score_count > max_needed) {
			// calculate average of all values in the first iteration and
			// average of all remaining values in the following iterations
			double mean;
			if (score_count == layout_count)
				mean = average(scores, layout_count);
			else
				mean = average_of_selected(scores, layout_count, indices_to_keep, new_length);
			// Get all indices & scores that are above the mean of the remaining scores.
			// This more than halves remaining scores.
			for (long i = 0; i < layout_count; i++) {
				if (indices_to_keep[i] && scores[i] < mean) {
					indices_to_keep[i] = false;
					new_length--;
				}
			}
			if (new_length == score_count)
				// If scores aren't filtered anymore, stop the loop
				break;
			score_count = new_length;
		}
	}

	// create array of layout/score pairs on the heap to store the remaining layouts
	// sorted in ascending order
	ScoredLayout* scored_layouts = calloc(new_length, sizeof(ScoredLayout));
	// Do this after the loop has finished.
	// Get the remaining (best) scores using the filtered indices.
	int j = 0;
	for (long i = 0; i < layout_count; i++) {
		if (indices_to_keep[i]) {
			scored_layouts[j].layout = layouts[i];
			scored_layouts[j].score = scores[i];
			j++;
		}
	}
	free(indices_to_keep);

	// Sort scores & indices. This is way faster thanks to the above while-loop
	qsort(scored_layouts, new_length, sizeof(ScoredLayout), cmplayoutp);

	// copy only the `nr_of_best` best layouts and scores to the output parameters
	// `top_layouts` and `top_scores`
	for (int i = 0; i < nr_of_best; i++) {
		int j = new_length - nr_of_best + i;
		top_layouts[i] = scored_layouts[j].layout;
		top_scores[i] = scored_layouts[j].score;
	}
}
