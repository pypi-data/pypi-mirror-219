from .utils import *
from gensim.models.keyedvectors import KeyedVectors
import random


def da_w2v_vi(proportion, vi_model_path, keep_old=False):
    def wrap(sentences, *args):
        word_vectors = KeyedVectors.load(vi_model_path)
        
        da_pairs = []
        for i in range(len(sentences)):
            ttokens = custom_tokenize(sentences[i][1])
            stokens = custom_tokenize(sentences[i][0])
            n_words_replace = int(len(stokens)*proportion)
            alg_positions = random.sample(range(len(stokens)), n_words_replace)
            for alg_pos in alg_positions:
                vi_token = stokens[alg_pos]
                synonym_token = vi_token
                if vi_token in word_vectors.key_to_index:
                    synonym_token = word_vectors.similar_by_word(vi_token)[0][0]
                stokens[alg_pos] = synonym_token
            t_out_str = ' '.join(ttokens)
            s_out_str = ' '.join(stokens)
            da_pairs.append([s_out_str, t_out_str])
        if keep_old:
            da_pairs.extend(sentences)
        return da_pairs
    return wrap

def da_w2v_ba(proportion, ba_model_path, keep_old=False):
    def wrap(sentences, *args): 
        word_vectors = KeyedVectors.load(ba_model_path)  
        da_pairs = []
        for i in range(len(sentences)):
            ttokens = custom_tokenize(sentences[i][1])
            stokens = custom_tokenize(sentences[i][0])
            n_words_replace = int(len(ttokens)*proportion)
            alg_positions = random.sample(range(len(ttokens)), n_words_replace)
            for alg_pos in alg_positions:
                ba_token = ttokens[alg_pos]
                synonym_token = ba_token
                if ba_token in word_vectors.key_to_index:
                    synonym_token = word_vectors.similar_by_word(ba_token)[0][0]
                ttokens[alg_pos] = synonym_token
            t_out_str = ' '.join(ttokens)
            s_out_str = ' '.join(stokens)
            da_pairs.append([s_out_str, t_out_str])
        if keep_old:
            da_pairs.extend(sentences)
        return da_pairs
    return wrap