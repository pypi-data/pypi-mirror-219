from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize

cc = SmoothingFunction()


def bleu(reference, hypothesis):
    if isinstance(reference, str):
        reference = [word_tokenize(reference)]
    elif isinstance(reference, list):
        reference = [word_tokenize(r) for r in reference]

    hypothesis = word_tokenize(hypothesis)
    bleu_score = sentence_bleu(reference, hypothesis, smoothing_function=cc.method4)

    return bleu_score


rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)


def rouge(reference, hypothesis):
    if isinstance(reference, str):
        return rouge_scorer.score(reference, hypothesis)
    elif isinstance(reference, list):
        return rouge_scorer.score_multi(reference, hypothesis)


def meteor(reference, hypothesis):
    r = word_tokenize(reference)
    h = word_tokenize(hypothesis)
    meteor_score_value = meteor_score([r], h)
    return meteor_score_value


def load_entailment_model(model_type, args=None):
    if args is None:
        args = {}
    if model_type == '':
        pass
    elif model_type == '':
        pass
    else:
        raise ValueError(f'Unknown entailment model type')
