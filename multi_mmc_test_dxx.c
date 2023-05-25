#include "utils.h"
#include <unistd.h>

#define MAX_ENTRIES 100000

// Section 6.3.9 - MultiMMC Prediction Estimate
/* This implementation of the MultiMMC test is a based on NIST's really cleaver implementation,
 * which interleaves the predictions and updates. This makes optimization much easier.
 * It's opaque why it works correctly (in particular, the first few symbols are added in a different
 * order than in the reference implementation), but once the initialization is performed, the rest of the
 * operations are done in the correct order.
 * The general observations that explains why this approach works are that
 * 1) each prediction that could succeed (i.e., ignoring some of the early predictions that must fail due
 *    to lack of strings of the queried length) must occur only after all the correct (x,y) tuples for that
 *    length have been processed. One is free to reorder otherwise.
 * 2) If there is a distinct string of length n, then this induces corresponding unique strings of all
 *    lengths greater than n. We track all string lengths independently (thus conceptually, we
 *    could run out of a short-string length prior to a long string length, thus erroneously not add
 *    some long string to the dictionary after no longer looking for a string to the dictionary when
 *    we should have), this can't happen in practice because we add strings from shortest to longest.
 */
extern "C" double multi_mmc_test(uint8_t *data, long len, int alph_size, const int verbose, const char *label, uint8_t *predictions,  bool *predicted){
	int winner, cur_winner;
	int entries[D_MMC];
	long i, d, N, C, run_len, max_run_len;
	long scoreboard[D_MMC] = {0};
	array<uint8_t, D_MMC> x;

	array<map<array<uint8_t, D_MMC>, PostfixDictionary>, D_MMC> M;

	if(len < 3){	
		printf("\t*** Warning: not enough samples to run multiMMC test (need more than %d) ***\n", 3);
		return -1.0;
	}

	//Step 1
	N = len-2;

	//Step 3
	//scoreboard is initilized above.
	winner = 0;
	
	C = 0;
	run_len = 0;
	max_run_len = 0;

	// initialize MMC counts
	// this performs step 4.a and 4.b for the () case
	memset(x.data(), 0, D_MMC);
	for(d = 0; d < D_MMC; d++){
		if(d < N){
			memcpy(x.data(), data, d+1);
			(M[d][x]).incrementPostfix(data[d+1], true);
			entries[d] = 1;
		}
	}

   // uint8_t dummyPrediction = 0;
   // for(i=0; i<2; i++) {
   //    write(3, &dummyPrediction, 1);
   // }

	// perform predictions
	//i is the index of the new symbol to be predicted
	for (i = 2; i < len; i++){
		bool found_x = false;
		cur_winner = winner;
		memset(x.data(), 0, D_MMC);

      uint8_t bestPrediction = 0;
      predicted[i] = false;

		for(d = 0; (d < D_MMC) && (i-2 >= d); d++) {
			map<array<uint8_t, D_MMC>, PostfixDictionary>::iterator curp;
			// check if x has been previously seen as a prefix. If the prefix x has not occurred,
			// then do not make a prediction for current d and larger d's
			// as well, since it will not occur for them either. In other words,
			// prediction is NULL, so do not update the scoreboard.
			// Note that found_x is uninitialized on the first round, but for that round d==0.
			if((d == 0) || found_x) {
				//Get the prediction
				//predict S[i] by using the prior d+1 symbols and the current state
				//We need the d-tuple prior to S[i], that is (S[i-d-1], ..., S[i-1])

				//This populates the curp for the later increment

				memcpy(x.data(), data+i-d-1, d+1);
				curp = M[d].find(x);
				if(curp == M[d].end()) found_x = false;
				else found_x = true;
			}

			if(found_x){
				long predictCount;
				// x has occurred, find max (x,y) pair across all y's
				// Check to see if the current prediction is correct.
            uint8_t curPrediction = (curp->second).predict(predictCount);
				if(curPrediction == data[i]){
					// prediction is correct, update scoreboard and winner
					if(++scoreboard[d] >= scoreboard[winner]) winner = d;
					if(d == cur_winner){
                  bestPrediction = curPrediction;
                  predicted[i] = true;
						C++;
						if(++run_len > max_run_len) max_run_len = run_len;
					}
				}
				else if(d == cur_winner) {
					//This prediction was wrong;
					//If the best predictor was previously d, zero the run length counter
					run_len = 0;
				}

				//Now check to see in (x,y) needs to be counted or (x,y) added to the dictionary
				if((curp->second).incrementPostfix(data[i], entries[d] < MAX_ENTRIES)) {
					//We had to make a new entry. Count this.
					entries[d]++;
				}
			} else if(entries[d] < MAX_ENTRIES) {
				//We didn't find the x prefix, so (x,y) surely can't have occurred.
				//We're allowed to make a new entry. Do so.
				//curp isn't populated here, because it wasn't found
				memcpy(x.data(), data+i-d-1, d+1);
				(M[d][x]).incrementPostfix(data[i], true);
				entries[d]++;
			}
		}

      // for debug purposes, write predictions to predictions
      // write(3, &bestPrediction, 1);
      predictions[i] = bestPrediction;
	}

	return(predictionEstimate(C, N, max_run_len, alph_size, "MultiMMC", verbose, label));
}
