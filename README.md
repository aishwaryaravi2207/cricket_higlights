# 🏏 CricketMatchSummarizer  
**Generating Engaging Cricket Match Articles using Local Language Models**

---

## 📘 Introduction

In today’s fast-paced world, staying updated with daily sports events can be overwhelming, especially in sports like cricket with multiple games occurring simultaneously. Our project leverages **Large Language Models (LLMs)** to automatically generate **article-style summaries** of cricket matches from live commentary.  

We explore the capability of **Retrieval-Augmented Generation (RAG)** techniques—particularly **MapReduce** and **STRUM-LLM (Google Research, 2024)**—to produce easy-to-read, accurate, and engaging summaries that give readers a comprehensive overview of each match.  

---

## 🧠 Motivation

While existing systems provide live commentary, few generate coherent, human-like articles summarizing matches. Our goal is to:  

1. **Summarize matches** efficiently using local LLMs.  
2. **Reduce information overload** for fans by providing short, descriptive articles.  
3. **Enable near real-time generation** of post-match reports.  

---

## 📚 Related Work

Research in automatic sports summarization has evolved from extractive summarization to transformer-based generation models:  
- **Aires (2016)** — Early graph-based NLG for cricket summaries.  
- **Zhang et al. (2016)** — Used LexRank for extractive summarization pre-transformer era.  
- **Huang et al. (2020)** — Introduced *SportSum* and *SportsSum 2.0*, combining transformers (BERTScore, BART) for article-style summaries.  
- **Gallotta et al. (2024)** — Demonstrated live commentary generation using LLMs.  

Our work builds on these foundations using a **multi-step LLM pipeline** with both extractive and contrastive summarization to generate article-quality cricket summaries.

---

## ⚙️ Methodology

Our system is divided into **six core stages**:

1. **Dataset Retrieval**  
   - Commentary data retrieved via the *Cricbuzz API* in JSON format.  
   - Converted to CSV using Python scripts for easy preprocessing and visualization.  

2. **Preprocessing & Refinement**  
   - Cleaned data using Regex to remove unwanted tokens.  
   - Structured data into:
     - `commentaries.csv`
     - `highlights.csv`
     - `match_info.csv`
     - `scorecard_batting.csv` & `scorecard_bowling.csv`

3. **Chunking**  
   - Due to limited model context lengths (~2–8K tokens), commentary is split into **pre-match**, **innings**, and **post-match** chunks.  
   - Optimal chunk size: **1500 tokens** to balance context and performance.  

4. **Extraction & Contrast (STRUM-LLM)**  
   - Inspired by **Google Research’s STRUM-LLM** (2024).  
   - Utilizes **extractive contrastive summarization**:  
     - Generates multiple pointwise summaries per chunk.  
     - Contrasts them to extract unique, high-value information.  
   - Combines with **MapReduce** logic to reduce computational cost.  

5. **Article Generation**  
   - Generates articles using **Llama 3 (8B)** model with structured prompts:
     - Introduction → Body → Conclusion  
     - Approx. 500–800 words  
     - Emphasizes readability, match flow, and performance highlights.  

6. **Revision & Refinement**  
   - Refines hallucinations and factual inconsistencies using **data-informed revision**.  
   - Injects scorecard and match info to guide the LLM toward factual correctness.  

---

## 🧩 Model Architecture

| Step | Model Used | Purpose |
|------|-------------|----------|
| Extraction | Dolphin-phi (4-bit) | Chunk-wise summarization |
| Contrast | Dolphin-phi (4-bit) | Extractive contrastive merging |
| Generation | **Llama 3 (8B, quantized)** | Article-style summarization |
| Revision | **Llama 3 (8B, quantized)** | Factual correction & style refinement |

**Why Llama 3 (8B)?**  
Compared to Mistral 7B, Llama 3 (8B) showed:
- Higher adherence to format.  
- Fewer hallucinations.  
- Greater coherence and cricket-specific understanding.  

---

## 🧪 Prompt Engineering Overview

### 🔹 Extraction
You are a cricket journalist. Extract concise key points from the provided commentary.

Format:

Point 1

Point 2

Point 3


### 🔹 Contrast

Combine two point summaries into one, keeping only unique information.
Generate a single concise list.


### 🔹 Generation

Task: Write an engaging, factual cricket article (500–800 words) using provided summaries.
Follow this format:
Title:
Introduction:
Body:
Conclusion:


### 🔹 Revision

Revise the article to improve flow, coherence, and factual accuracy.
Ensure 600–900 words, better transitions, and enhanced readability.


---

## 💻 Implementation Details

- **Language:** Python  
- **Environment:** Local quantized LLMs using `transformers` & `bitsandbytes`  
- **Data Source:** Cricbuzz API  
- **Token Limit per Chunk:** ~1500  
- **Libraries Used:**  
  - `pandas`, `regex`, `json`, `matplotlib`  
  - `transformers`, `accelerate`, `bitsandbytes`  
- **Model Quantization:** 4-bit (to reduce memory footprint)  

---

## 🚧 Constraints & Limitations

### ⚠️ Hallucination  
- Common in generative models (e.g., incorrect player names, scores, or teams).  
- Mitigated via *revision prompts* and *data-informed regeneration*.  

### ⚙️ Compute Constraints  
- Running large models locally required **quantization** for feasible inference.  
- Trade-off: Slight precision loss vs. significant memory efficiency.  

### 🧱 Ethical Concerns  
- Risk of misinformation due to hallucinations.  
- Must verify facts before publication.  
- Need for transparency in AI-generated journalism.  

---

## 🧾 Example Output (Excerpt)

> **Thrilling Finish as Gujarat Titans Seal Victory**  
> In a nail-biting encounter, Gujarat Titans clinched victory in the final over, thanks to a stellar performance by Shubman Gill, who was named Man of the Match...  

---

## 🧩 Future Work

- Implement live summarization during matches.  
- Integrate factual consistency checks using structured scorecard data.  
- Develop a web interface for on-demand match summaries.  

---

## 👥 Contributors

| Name | Role |
|------|------|
| *[Your Name]* | Research, Implementation, Prompt Engineering, Report Writing |
| Team Members | Model Evaluation, Data Pipeline Setup |

---

## 📜 References

- Google Research (2024). *STRUM-LLM: Extractive Contrastive Summarization for Decision Support*  
- Huang et al. (2020). *SportsSum: Transformer-based Sports Commentary Summarization*  
- Aires (2016). *Graph-based Natural Language Generation for Sports Summaries*  
- Zhang et al. (2016). *LexRank-based Extractive Summarization for Cricket Commentary*  

---

## 🏁 Conclusion

Our project demonstrates the potential of **local quantized LLMs** in automating the generation of **sports journalism-style articles** from raw commentary. By combining **STRUM-LLM**, **MapReduce**, and thoughtful **prompt engineering**, we achieve coherent, context-aware cricket summaries while addressing challenges like hallucination and compute constraints.
