from typing import List

from pos_tagger import PosTagger
from training import HMM
from pprint import pprint


def make_default_emissions(pos_list):

    # vit = {pos: 1 / len(pos_list) for pos in pos_list}

    vit = {}

    vit["PROPN"] = 1

    return vit


class ViterbiTagger(PosTagger):
    def __init__(self, hmm: HMM):
        self.transition = hmm.transition
        self.emission = hmm.emission

    def pos_tag(self, tokens: List[str]):
        emissions = self.emission
        transitions = self.transition
        default_emissions = make_default_emissions(transitions.keys())

        # pprint(transitions)
        # pprint(emissions)

        viterbi_matrix = [
            {
                pos: em_value * transitions["Q0"][pos]
                for pos, em_value in emissions.get(
                    tokens[0], default_emissions
                ).items()
            }
        ]
        pprint(viterbi_matrix)

        for token in tokens[1:]:
            previus_column = len(viterbi_matrix) - 1

            for previus_pos, previus_value in viterbi_matrix[
                previus_column
            ].items():

                viterbi_matrix = [
                    {
                        pos: em_value
                        * transitions[previus_pos][pos]
                        * previus_value
                        for pos, em_value in emissions.get(
                            token, default_emissions
                        ).items()
                    }
                ]

        # viterbi_matrix = [
        #     {
        #         pos: em_value * transitions[previus_pos][pos] * previus_value
        #         for pos, em_value in emissions.get(token, default_emissions).items()  # transition_qualcosa
        #     }
        # ]

        # pprint(transitions)
        # pprint(emissions)
        # for value in transitions.get["Qf"]("NOUN") : print(value)
        # for key,value in emissions.get(tokens[0]).items() : print(key,value)
        # pprint(transitions)
        # print(transitions["X"]["ADJ"])
        # for value in emissions.get(tokens[0]).values(): print(value)
        # print(emissions.get(tokens[0]).values())


if __name__ == "__main__":
    from training import hmm_ud_english
    from sentences import tokenized_sentences as sentences

    tagger = ViterbiTagger(hmm_ud_english())
    tagger.pos_tag(sentences[1])
