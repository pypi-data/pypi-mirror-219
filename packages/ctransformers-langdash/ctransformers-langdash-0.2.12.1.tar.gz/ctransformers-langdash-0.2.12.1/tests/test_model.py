from ctransformers import AutoModelForCausalLM


class TestModel:
    def test_generate(self, lib):
        llm = AutoModelForCausalLM.from_pretrained("marella/gpt-2-ggml", lib=lib)
        response = llm("AI is going to", seed=5, max_new_tokens=3)
        assert response == " be a big"

        token = llm.sample()
        logits = llm.logits
        value = logits[token]
        logits[token] -= 1
        assert logits[token] == llm.logits[token] == value - 1
        llm.logits[token] *= 2
        assert logits[token] == llm.logits[token] == (value - 1) * 2

        assert llm.eos_token_id == 50256
        assert llm.vocab_size == 50257
        assert llm.context_length == 1024

    def test_load_save_state(self, lib):
        llm = AutoModelForCausalLM.from_pretrained("marella/gpt-2-ggml", lib=lib)
        llm.eval(llm.tokenize("The quick brown fox"))

        old_logits = list(llm.logits)
        state = llm.clone_state()
        old_predict = llm(" jumps over", seed=3, max_new_tokens=5)

        llm.reset()
        llm.set_state(state)
        assert list(llm.logits) == old_logits
        new_predict = llm(" jumps over", seed=3, max_new_tokens=5)
        assert old_predict == new_predict


if __name__ == "__main__":
    TestModel().test_load_save_state("local")