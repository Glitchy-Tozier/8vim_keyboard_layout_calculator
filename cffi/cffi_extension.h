typedef struct Bigram {
	int letter1AsciiCode;
	int letter2AsciiCode;
	double frequency;
} BigramC;

/*
 * Calculate score for given layout.
 *
 * @param[in] layout Layout of interest.
 * @param[in] layout_length Byte count of layout.
 * @param[in] bigrams Array of bigrams needed to calculate the layout score.
 * @param[in] bigrams_count Count of bigrams.
 * @param[in] score_list Nested array of scores for letter placements.
 * @return Score for the given layout.
 */
double test_single_layout(char* layout, int layout_length, BigramC* bigrams,
                          int bigrams_count, double score_list[][32]);

/*
 * Sort layouts by score in ascending order and store the top `nr_of_best`
 * layouts in `top_layouts` and the corresponding scores in `top_scores`.
 *
 * @param[in]  layouts Pointer to unsorted array of layouts.
 * @param[in]  layout_count Number of layouts (and corresponding scores).
 * @param[in]  scores Array of scores.
 * @param[in]  nr_of_best Number of best layouts to keep.
 * @param[in]  letters_per_layer Letters per layer, usually 8.
 * @param[out] top_layouts Pointer to array to store best layouts (sorted).
 * @param[out] top_scores Pointer to array to store best scores (sorted).
 */
void get_top_scores(char** layouts, long layout_count, double* scores, int nr_of_best,
                    int letters_per_layer, char** top_layouts, double* top_scores);
