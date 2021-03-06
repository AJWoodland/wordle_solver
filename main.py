import string

word_length = 5

def filter_exclude_list(word_list,exclude_list):
    #generates a new word list where any word containing an excluded letter is removed
    output_word_list =[]
    
    for word in word_list:
        letter_found = False
        for char in word:
            if char in exclude_list:
                letter_found = True
        if letter_found == False:
            output_word_list.append(word)
    return output_word_list


def filter_allowed_words(word_list,included_list,known_list):
    #return a new word list that accounts for all included letters and known letters in correct positions
    output_word_list =[]
    
    for word in word_list:
        letter_found = False
        letter_mismatch = False
        for char in word:
            if char in included_list:
                letter_found = True
        included_check = dict.fromkeys(included_list,0)

        for i in range(0,word_length):
            if word[i] == known_list[i]: #test for letter in correct space
                letter_found = True 
            if known_list[i] == 'null': #test if letter not known yet
                letter_found = True
                if word[i] in included_list: #check if letter is included list in a free position
                    included_check[word[i]] = 1
            elif word[i] != known_list[i]: #letter mismatch in known position and not null
                letter_mismatch = True
        if 0 in included_check.values() : #check that all included letters are present in the word
            letter_mismatch = True
        if letter_found == True and letter_mismatch == False:
            output_word_list.append(word)
    return output_word_list

def score_letters(word_list,zero_value_letters):
    #score letters based on the frequency they occur within the word list in general and in specific positions
    alphabet_string = string.ascii_lowercase
    alphabet_list = [char for char in alphabet_string]
    letter_freq = dict.fromkeys(alphabet_list,0)
    placement_freq = []
    
    for i in range (0,word_length):
        placement_freq.append(letter_freq.copy())
    for word in word_list:
        for char in alphabet_list: #going through every letter probably inefficient but means each letter only valued once if repeated
            if char not in zero_value_letters:
                if char in word:
                    letter_freq[char]=letter_freq[char]+1
                for i in range(0,word_length):
                    if word[i] == char:
                        placement_freq[i][char] += 1

    return letter_freq, placement_freq
    
def update_scores(word_list,scoring_word_list,zero_value_letters):
    letter_freq, placement_freq = score_letters(scoring_word_list,zero_value_letters)
    #print(letter_freq)
    #print(placement_freq)
    word_values,placement_values, word_count = score_all_words(word_list,letter_freq,placement_freq)
    return word_values,placement_values, word_count

def score_word(word,letter_score,placement_freq):
    score = 0
    placement_score = 0
    alphabet_string = string.ascii_lowercase
    alphabet_list = [char for char in alphabet_string]
    
    for char in alphabet_list: #going through every letter probably inefficient but means each letter only valued once if repeated
        if char in word:
            character_placement_value = 0
            char_score = letter_score[char]
            score = score + char_score    
            for i in range(0,word_length):
                if word[i] == char:
                    if placement_freq[i][char] > character_placement_value: #to avoid double counting of repeated letters, only highest value letter placement is counted
                        character_placement_value = placement_freq[i][char]
            placement_score = placement_score + character_placement_value

    return score, placement_score

def score_all_words(word_list,letter_score,placement_freq):
    #cycles through words to score based on letter values
    word_values = dict.fromkeys(word_list,0)
    placement_values = dict.fromkeys(word_list,0)
    scored_words = 0
    for word in word_list:
        score, placement_score = score_word(word,letter_score,placement_freq)
        word_values[word] = score
        placement_values[word] = placement_score
        if score > 0:
            scored_words = scored_words+1 #running count of useful words
    return word_values,placement_values, scored_words

def get_highest_score_word(word_values,placement_values):
    max_score = 0
    max_placement = 0
    
    for word,value in word_values.items():
        if value >= max_score:
            if placement_values[word] > max_placement:
                max_score = value
                best_word = word
        
    if max_score == 0:
        best_word = 'null'
    return best_word

def return_best_words(word_list,answers,exclusion_list,included_list,known_list):
    #given a list of possible guess words, possible solution words and all known letter data determine best guess and highest information guess
    answer_list_exclude_removed = filter_exclude_list(answers,exclusion_list)
    answer_possible_word_list = filter_allowed_words(answer_list_exclude_removed,included_list,known_list)
    
    #determine possible words based on words which fit 
    zero_value_letters = exclusion_list+known_list

    if len(included_list+exclusion_list)+word_length-known_list.count('null') > 0: #only do best guess once letters are excluded/known
        possible_scores, placement_scores, possible_count = update_scores(answer_possible_word_list,answer_possible_word_list,zero_value_letters)

        possible_best = get_highest_score_word(possible_scores,placement_scores)
        possible_value = possible_scores[possible_best]
        print("Best guess: ",possible_best," - ",possible_value)
        print(possible_count," possible answers")
        if possible_count <= 10:
            print('possible words:')
            for possible_word, possible_score in possible_scores.items():
                if possible_score > 0:
                    print(possible_word)
   
    zero_value_letters = exclusion_list+included_list+known_list
    unknown_scores, placement_scores, unknown_count = update_scores(word_list,answer_possible_word_list,zero_value_letters)    
    if unknown_count != 0:
        unknown_best = get_highest_score_word(unknown_scores,placement_scores)
        unknown_value = unknown_scores[unknown_best]
        print("Best new letter value: ",unknown_best," - ",unknown_value)
        if unknown_count <=10:
            print("value words")
            for unknown_word, score in unknown_scores.items():
                if score > 0:
                    print(unknown_word,' - ',score)
    else:
        print("all letters determined")

    
if __name__ == "__main__":
    
    #load word lists
    guessfile = open(r"wordle-allowed-guesses.txt",'r') 
    guesses = guessfile.read().splitlines()
    guessfile.close()

    answerfile = open(r"wordle-answers-alphabetical.txt",'r')
    answers = answerfile.read().splitlines()
    answerfile.close()

    combined_word_list = guesses + answers

    excludedstr = 'ralunk'
    includedstr = 'ots'

    #known_list = ['null']*word_length

    known_list = ['null','null','null','null','e']
    #known_list = ['null']*word_length

    exclusion_list = [char for char in excludedstr]
    included_list = [char for char in includedstr]

    return_best_words(combined_word_list,answers,exclusion_list,included_list,known_list)


#plans
#take account of knowledge of letter position
    #can determine value based on position rather than just existence

    #can account for knowledge that letters returned as being present but in wrong place are excluded from that position
    #requires new structure for included letters which also records position tested already

#determine array of best value words with same score
#pick either based on possibility of being answer
#or on determining location of letters

#determine value based on minimising number of remaining words
    #may only be feasible once initial guesses narrow down

#code a version of the game for testing, this would allow comparison of strategies,
    #max guesses/average guesses/number of words not got within 6 guesses.
    #code only initially
    #GUI for playability?


#graphical interface

#automate interaction with website? reading of page and filling in of letters



    





