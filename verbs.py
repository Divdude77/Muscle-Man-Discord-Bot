import nltk

# Some nltk requirements
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def verb_check(text):
    data = [list(i) for i in nltk.pos_tag(nltk.word_tokenize(text))]

    # Catch all pings and reformat them
    for i in range(len(data)):
        try:
            if data[i][0].isnumeric() and len(data[i][0]) == 18 and data[i-1][0] == "@" and data[i-2][0] == "<" and data[i+1][0] == ">":
                data[i-2:i+2] = [[f"<@{data[i][0]}>", "NN"]]
            if data[i][0] == "everyone" and data[i-1][0] == "@":
                data[i-1:i+1] = [["@everyone", "NN"]]
        except IndexError:
            pass

    # Convert all upper case statements to lower case
    for i in range(len(data)):
        if data[i][1] not in ["NN"]:
            data[i][0] = data[i][0].lower()

    # Check for abbreviations/slang not recognized by nltk
    for i in range(len(data)):
        if data[i][0] == "ur":
            data[i:i+1] = [["u", "PRP"], ["r", "VBP"]]
        if data[i][0] == "im":
            data[i:i+1] = [["i", "PRP"], ["am", "VBP"]]
        if data[i][0] == "ive":
            data[i:i+1] = [["i", "PRP"], ["ve", "VBP"]]
        if data[i][0] == "ik":
            data[i:i+1] = [["i", "PRP"], ["know", "VBP"]]
        if data[i][0] in ["i", "u"]:
            data[i][1] = "PRP"
        if data[i][0] in ["suck", "sucks"]:
            data[i][1] = "VBP"
        if data[i][0] == "r":
            data[i][1] = "VBP"
        if data[i][0] in ["me", "i"]:
            data[i][0] = "you"
        if data[i][0] == "my":
            data[i][0] = "your"
        if data[i][0] == "mine":
            data[i][0] = "yours"
        if data[i][0] == "myself":
            data[i][0] = "yourself"

    # Change grammar for verbs to match "my mom"
    for j in range(len(data)):
        try:
            print("in")
            if data[j][1] in ["PRP", "NNP", "NN", "WP"] and data[j+1][1] in ["VBP", "VBZ", "VBD", "VBN", "MD", "VBG"]:
                if data[j+1][0] in ["am", "are", "'m", "'re", "r", "'s"]:
                    data[j+1][0] = "is"
                elif data[j+1][0] in ["have", "ve", "'ve"]:
                    data[j+1][0] = "has"
                if data[j+1][0][-1] == "o":
                    data[j+1][0] += "es"
                if data[j+1][0] == "'ll":
                    data[j+1][0] = "will"
                elif data[j+1][0][-2:] == "ss":
                    data[j+1][0] += "es"
                elif data[j+1][0][-1] != "s":
                    if data[j+1][1] == "VBP" and data[j+1][1] != "MD":
                        data[j+1][0] += "s"
                try:
                    if data[j+2][0] == "n't":
                        data[j+2][0] = "not"
                except IndexError:
                    pass
                del data[:j+1]
                output = ""
                for k in [i[0] for i in data]:
                    output += k + " "
                return True, output.strip()
            else:
                continue
        except IndexError:
            pass
    else:
        return False, None
