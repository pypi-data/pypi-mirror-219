#ifndef CTRANSFORMERS_MODELS_LLM_H_
#define CTRANSFORMERS_MODELS_LLM_H_

#include "common.h"

// https://github.com/marella/train/blob/3c4ba1f59bf20e31f7ee5ea9a8f38e49440a93f7/train/state.py#L135-L175
class RingBuffer {
 public:
  void Init(const int capacity) {
    capacity_ = capacity;
    Clear();
  }

  void Add(const gpt_vocab::id token) {
    if (Size() < capacity_) {
      tokens_.push_back(token);
    } else {
      tokens_[pos_] = token;
    }
    pos_ = (pos_ + 1) % capacity_;
  }

  // Returns last n tokens.
  std::unordered_set<gpt_vocab::id> GetRecent(int n) const {
    const int size = Size();
    n = std::min(size, n);
    std::unordered_set<gpt_vocab::id> result;
    if (n == 0) {
      return result;
    }
    const int start = (pos_ - n + size) % size;
    if (start < pos_) {
      result.insert(tokens_.begin() + start, tokens_.begin() + pos_);
    } else {
      result.insert(tokens_.begin() + start, tokens_.end());
      result.insert(tokens_.begin(), tokens_.begin() + pos_);
    }
    return result;
  }

  void Clear() {
    tokens_.clear();
    pos_ = 0;
  }

  int Size() const { return tokens_.size(); }

  size_t SerializeBytes() {
    size_t nbytes = 0;
    nbytes += sizeof(capacity_);
    nbytes += sizeof(pos_);
    nbytes += sizeof(size_t); // tokens_.size()
    nbytes += tokens_.size() * sizeof(gpt_vocab::id);
    return nbytes;
  }

  void Serialize(void *data) {
    uint8_t *data_bytes = static_cast<uint8_t *>(data);

    memcpy(data_bytes, &capacity_, sizeof(capacity_));
    data_bytes += sizeof(capacity_);

    memcpy(data_bytes,&pos_, sizeof(pos_));
    data_bytes += sizeof(pos_);

    size_t tokens_size = tokens_.size();
    memcpy(data_bytes, &tokens_size, sizeof(tokens_size));
    data_bytes += sizeof(tokens_size);
    memcpy(data_bytes, tokens_.data(), tokens_size * sizeof(gpt_vocab::id));
    data_bytes += tokens_size * sizeof(gpt_vocab::id);
  }

  void Deserialize(void *data) {
    uint8_t *data_bytes = static_cast<uint8_t *>(data);

    memcpy(&capacity_, data_bytes, sizeof(capacity_));
    data_bytes += sizeof(capacity_);

    memcpy(&pos_, data_bytes, sizeof(pos_));
    data_bytes += sizeof(pos_);

    size_t tokens_size;
    memcpy(&tokens_size, data_bytes, sizeof(tokens_size));
    data_bytes += sizeof(tokens_size);
    tokens_.resize(tokens_size, 0);
    memcpy(tokens_.data(), data_bytes, tokens_size * sizeof(gpt_vocab::id));
    data_bytes += tokens_size * sizeof(gpt_vocab::id);
  }

 private:
  int capacity_;
  std::vector<gpt_vocab::id> tokens_;
  int pos_ = 0;
};

class LLM {
 public:
  virtual ~LLM(){};

  bool Init(const std::string &filename, const int context_length,
            const int gpu_layers) {
    if (initialized_) {
      return false;
    }
    if (!Load(filename, context_length, gpu_layers)) {
      return false;
    }
    previous_tokens_.Init(ContextLength());
    return initialized_ = true;
  }

  virtual std::vector<gpt_vocab::id> Tokenize(const std::string &text) const {
    return gpt_tokenize(vocab_, text);
  }

  virtual const std::string &Detokenize(const gpt_vocab::id id) const {
    const auto it = vocab_.id_to_token.find(id);
    if (it == vocab_.id_to_token.end()) {
      return kEmptyString;
    }
    return it->second;
  }

  bool BatchEval(const std::vector<gpt_vocab::id> &tokens, int batch_size,
                 const int threads) {
    batch_size = std::min(ContextLength(), batch_size);
    const int size = tokens.size();
    for (int start = 0; start < size; start += batch_size) {
      const int end = std::min(start + batch_size, (int)tokens.size());
      const std::vector<gpt_vocab::id> batch(tokens.begin() + start,
                                             tokens.begin() + end);
      if (!EvalInternal(batch, threads)) {
        return false;
      }
    }
    return true;
  }

  virtual std::vector<float> &Logits() { return logits_; }

  virtual const std::vector<float> &Embeddings() const { return embeddings_; }

  virtual gpt_vocab::id Sample(const int top_k, const float top_p,
                               const float temperature,
                               const float repetition_penalty,
                               int last_n_tokens, int seed) const {
    if (logits_.empty()) {
      return EosToken();
    }
    if (last_n_tokens < 0) {
      last_n_tokens = ContextLength();
    }
    if (seed < 0) {
      seed = time(nullptr);
    }
    std::mt19937 rng(seed);

    std::unordered_set<gpt_vocab::id> recent_tokens;
    if (repetition_penalty != 1.0f) {
      recent_tokens = previous_tokens_.GetRecent(last_n_tokens);
    }

    return gpt_sample_top_k_top_p(
        vocab_, logits_.data() + (logits_.size() - VocabSize()), top_k, top_p,
        temperature, repetition_penalty, recent_tokens, rng);
  }

  virtual bool IsEosToken(const gpt_vocab::id token) const {
    if (token == EosToken()) {
      return true;
    }
    // Handle special tokens in StarChat and Dolly V2.
    if (!vocab_.special_tokens.empty()) {
      const std::string &text = Detokenize(token);
      return text == "<|end|>" || text == "### End";
    }
    return false;
  }

  virtual gpt_vocab::id EosToken() const {
    const auto it = vocab_.token_to_id.find("<|endoftext|>");
    if (it != vocab_.token_to_id.end()) {
      return it->second;
    }
    return 0;
  }

  virtual int VocabSize() const { return vocab_.id_to_token.size(); }

  int ContextLength() const { return n_ctx_; }

  void Reset() {
    logits_.clear();
    previous_tokens_.Clear();
  }

  virtual size_t GetModelStateSize() { return 0; }
  virtual void CloneModelState(void *data) {}
  virtual void SetModelState(void *data) {}

  size_t GetStateSize() {
    size_t model_state_size = GetModelStateSize();
    if (model_state_size == 0)
      return 0;

    size_t nbytes = 0;
    nbytes += sizeof(size_t);
    nbytes += logits_.size() * sizeof(float);
    nbytes += sizeof(size_t);
    nbytes += previous_tokens_.SerializeBytes();
    nbytes += sizeof(size_t);
    nbytes += model_state_size;
    return nbytes;
  }

  void SetState(void *data) {
    uint8_t *data_bytes = static_cast<uint8_t*>(data);
    size_t field;

    memcpy(&field, data_bytes, sizeof(field));
    logits_.resize(field, 0.);
    data_bytes += sizeof(field);
    memcpy(logits_.data(), data_bytes, logits_.size() * sizeof(float));
    data_bytes += logits_.size() * sizeof(float);

    memcpy(&field, data_bytes, sizeof(field));
    data_bytes += sizeof(field);
    previous_tokens_.Deserialize(data_bytes); 
    data_bytes += field;

    memcpy(&field, data_bytes, sizeof(field));
    data_bytes += sizeof(field);
    SetModelState(data_bytes);
    data_bytes += field;
  }

  void CloneState(void *data) {
    uint8_t *data_bytes = static_cast<uint8_t*>(data);
    size_t field;

    field = logits_.size();
    memcpy(data_bytes, &field, sizeof(field));
    data_bytes += sizeof(field);
    memcpy(data_bytes, logits_.data(), logits_.size() * sizeof(float));
    data_bytes += logits_.size() * sizeof(float);

    field = previous_tokens_.SerializeBytes();
    memcpy(data_bytes, &field, sizeof(field));
    data_bytes += sizeof(field);
    previous_tokens_.Serialize(data_bytes); 
    data_bytes += field;

    field = GetModelStateSize();
    memcpy(data_bytes, &field, sizeof(field));
    data_bytes += sizeof(field);
    CloneModelState(data_bytes);
    data_bytes += field;
  }

 protected:
  const std::string kEmptyString = "";
  int n_ctx_ = -1;
  gpt_vocab vocab_;
  size_t mem_per_token_ = 0;
  std::vector<float> logits_;
  std::vector<float> embeddings_;
  RingBuffer previous_tokens_;

  virtual bool Load(const std::string &filename, const int context_length,
                    const int gpu_layers) = 0;

  virtual bool Eval(const std::vector<gpt_vocab::id> &tokens, const int threads,
                    const int n_past) = 0;

 private:
  bool initialized_ = false;

  bool EvalInternal(const std::vector<gpt_vocab::id> &tokens, int threads) {
    if (threads < 0) {
      // https://github.com/ggerganov/llama.cpp/blob/cc45a7feb8412e84ff292207621412fffc0d3d51/examples/common.cpp#L67-L68
      const int n = std::thread::hardware_concurrency();
      threads = n > 0 ? (n <= 4 ? n : n / 2) : 4;
    }
    threads = std::max(threads, 1);
    const int n_past =
        std::min(ContextLength() - (int)tokens.size(), previous_tokens_.Size());
    if (!Eval(tokens, threads, n_past)) {
      return false;
    }
    for (const gpt_vocab::id token : tokens) {
      previous_tokens_.Add(token);
    }
    return true;
  }
};

#define REGISTER_LLM(_name)                                                \
  class _name##_llm : public LLM {                                         \
   public:                                                                 \
    virtual ~_name##_llm() {                                               \
      if (model_.ctx != nullptr) {                                         \
        ggml_free(model_.ctx);                                             \
      }                                                                    \
    }                                                                      \
                                                                           \
    size_t GetModelStateSize() override {                                  \
      return _name##_get_state_size(model_);                               \
    }                                                                      \
    void CloneModelState(void *data) override {                            \
      return _name##_clone_state(model_, data);                            \
    }                                                                      \
    void SetModelState(void *data) override {                              \
      return _name##_set_state(model_, data);                              \
    }                                                                      \
                                                                           \
   protected:                                                              \
    bool Load(const std::string &filename, const int context_length,       \
              const int gpu_layers) override {                             \
      if (context_length > 0) {                                            \
        model_.hparams.n_ctx = context_length;                             \
      }                                                                    \
      if (!_name##_model_load(filename, model_, vocab_)) {                 \
        return false;                                                      \
      }                                                                    \
      n_ctx_ = model_.hparams.n_ctx;                                       \
      return true;                                                         \
    }                                                                      \
                                                                           \
    bool Eval(const std::vector<gpt_vocab::id> &tokens, const int threads, \
              const int n_past) override {                                 \
      return _name##_eval(model_, threads, n_past, tokens, logits_,        \
                          mem_per_token_);                                 \
    }                                                                      \
                                                                           \
   private:                                                                \
    _name##_model model_;                                                  \
  }

#endif
