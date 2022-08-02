import nltk

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
        if data[i][0].isupper():
            data[i][0] = data[i][0].lower()

    # Check for abbreviations/slang not recognized by nltk
    if len(data) > 1:
        if data[0][0] == "ur":
            data[:1] = [["u", "PRP"], ["r", "VBP"]]
        if data[0][0] == "im":
            data[:1] = [["i", "PRP"], ["r", "VBP"]]
        if data[0][0] == "ive":
            data[:1] = [["i", "PRP"], ["ve", "VBP"]]
        if data[0][0] == "ik":
            data[:1] = [["i", "PRP"], ["know", "VBP"]]
        if data[0][0] in ["i", "u"]:
            data[0][1] = "PRP"
        if data[1][0] in ["suck", "sucks"]:
            data[1][1] = "VBP"
        if data[1][0] in ["r"]:
            data[1][1] = "VBP"

        # Change grammar for verbs to match "my mom"
        if data[0][1] in ["PRP", "NNP", "NN", "WP"] and data[1][1] in ["VBP", "VBZ", "VBD", "VBN", "MD", "VBG"]:
            if data[1][0] in ["am", "are", "'m", "'re", "r", "'s"]:
                data[1][0] = "is"
            elif data[1][0] in ["have", "ve", "'ve"]:
                data[1][0] = "has"
            if data[1][0][-1] == "o":
                data[1][0] += "es"
            if data[1][0] == "'ll":
                data[1][0] = "will"
            elif data[1][0][-1] != "s":
                if data[1][1] == "VBP" and data[1][1] != "MD":
                    data[1][0] += "s"
            try:
                if data[2][0] == "n't":
                    data[2][0] = "not"
            except IndexError:
                pass
            output = ""
            for j in [i[0] for i in data[1:]]:
                output += j + " "
            return True, output.strip()
        else:
            return False, None
    else:
        return False, None
