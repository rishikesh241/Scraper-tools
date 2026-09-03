import json
import os
import re
import zipfile


COUNTER_NOTES = {
    10: {
        "verified_option": "D",
        "orig_community": "C",
        "note": "OPTION D IS CORRECT (counters Community Vote C). Because labels are provided as integer indices (0, 1, 2) rather than one-hot encoded vectors, Sparse categorical cross-entropy is the required multi-class loss function.",
    },
    18: {
        "verified_option": "C",
        "orig_community": "D",
        "note": "OPTION C IS CORRECT (counters Community Vote D). To prevent data leakage in time-dependent customer lifetime value (LTV) predictions, pass the transaction timestamp column as the time column so AutoML Tables splits data chronologically.",
    },
    28: {
        "verified_option": "AD",
        "orig_community": "AD",
        "note": "OPTIONS A AND D ARE CORRECT (Multi-Select: Choose two). Using Dataset.interleave reads sharded TFRecord files in parallel, and Dataset.prefetch overlaps CPU preprocessing with TPU execution to resolve input-bound bottlenecks.",
    },
    40: {
        "verified_option": "CE",
        "orig_community": "CE",
        "note": "OPTIONS C AND E ARE CORRECT (Multi-Select: Choose two). Enabling early stopping halts unpromising trials early, and running iterative rounds with narrowed parameter ranges and fewer trials significantly reduces tuning time without compromising effectiveness.",
    },
    69: {
        "verified_option": "A",
        "orig_community": "B",
        "note": "OPTION A IS CORRECT (counters Community Votes B/D). Treating 'non-compliant photo' (violation) as the positive class, accepting a non-compliant photo is a False Negative. Minimizing False Negatives (maximizing Recall on violations) prevents policy-violating photos from being accepted.",
    },
    80: {
        "verified_option": "C",
        "orig_community": "B",
        "note": "OPTION C IS CORRECT (counters Community Vote B). App Engine provides the secure API gateway, Cloud Bigtable supplies single-digit millisecond reads/writes for real-time user navigation context, and AI Platform Prediction serves the model within the 300ms latency SLA.",
    },
    85: {
        "verified_option": "D",
        "orig_community": "C",
        "note": "OPTION D IS CORRECT (counters Community Tie C). Using human moderator decisions on flagged comments to calculate precision and estimate recall continuously validates model quality against ground truth.",
    },
    94: {
        "verified_option": "B",
        "orig_community": "C",
        "note": "OPTION B IS CORRECT (counters Community Tie C). Per Google's Rules of ML, when starting without labeled historical failure data, first use a simple heuristic (z-scores on resource spikes) to generate baseline labels and bootstrap a supervised classifier.",
    },
    96: {
        "verified_option": "B",
        "orig_community": "D",
        "note": "OPTION B IS CORRECT (counters Community Vote D). Training on 3 million high-resolution X-ray images on a single P100 GPU is compute-bound; scaling to a Cloud TPU v3-32 pod slice provides 32 TPU cores and 512 GB HBM to dramatically accelerate training without losing image detail.",
    },
    105: {
        "verified_option": "A",
        "orig_community": "D",
        "note": "OPTION A IS CORRECT (counters Community Vote D). Because propensity is evaluated over a two-week window and player data already resides in BigQuery, importing the model into BigQuery ML for batch inference and serving precomputed results via Cloud SQL minimizes latency and operational overhead.",
    },
    113: {
        "verified_option": "A",
        "orig_community": "D",
        "note": "OPTION A IS CORRECT (counters Community Vote D). A direct Pub/Sub BigQuery subscription streams real-time mobile user activity straight into BigQuery without requiring intermediate Spark or Dataflow processing pipelines.",
    },
    116: {
        "verified_option": "D",
        "orig_community": "B",
        "note": "OPTION D IS CORRECT (counters Community Vote B). Custom C++ TensorFlow operations without dedicated CUDA or XLA kernels execute on CPUs; using a 4-node n1-highcpu-96 cluster (384 vCPUs) avoids GPU/TPU fallback overhead while handling large batch and model sizes.",
    },
    138: {
        "verified_option": "D",
        "orig_community": "B",
        "note": "OPTION D IS CORRECT (counters Community Vote B). Running a TFLite logistic regression model directly on the mobile client adds <5ms latency and attaches the prediction to the initial purchase event, satisfying the strict <50ms pipeline stage budget.",
    },
    140: {
        "verified_option": "A",
        "orig_community": "C",
        "note": "OPTION A IS CORRECT (counters Community Tie C). Tokenizing sensitive customer fields via cryptographic hashing masks PII irreversibly while preserving deterministic token equality so ML models can still learn predictive patterns across all attributes.",
    },
    141: {
        "verified_option": "C",
        "orig_community": "B",
        "note": "OPTION C IS CORRECT (counters Community Vote B). With a 90% renewal / 10% cancellation class imbalance, achieving 99% accuracy on the difficult 10% minority churn class and 82% on renewals indicates strong minority-class recall ready for production.",
    },
    149: {
        "verified_option": "BD",
        "orig_community": "BD",
        "note": "OPTIONS B AND D ARE CORRECT (Multi-Select: Choose two). When additional data cannot be collected for an underrepresented subgroup, modifying the objective function to apply higher error penalties and resampling the dataset are the two standard mitigations.",
    },
    163: {
        "verified_option": "B",
        "orig_community": "D",
        "note": "OPTION B IS CORRECT (counters Community Tie D). BigQuery is an analytical OLAP warehouse with hundreds of milliseconds of query overhead; replacing it with a low-latency NoSQL database (e.g., Cloud Bigtable or Memorystore) meets the sub-100ms real-time feature lookup requirement.",
    },
    169: {
        "verified_option": "BC",
        "orig_community": "B",
        "note": "OPTIONS B AND C ARE CORRECT (Multi-Select: Choose two). Decreasing the classification score threshold increases recall (reducing false negatives), and adding more positive (fraud) examples to the training set improves minority-class representation.",
    },
    200: {
        "verified_option": "C",
        "orig_community": "A",
        "note": "OPTION C IS CORRECT (counters Community Tie A). Document AI Custom Extractor supports fine-tuning on custom scanned PDF forms to extract unstructured handwritten feedback fields with higher accuracy than generic OCR.",
    },
    202: {
        "verified_option": "C",
        "orig_community": "D",
        "note": "OPTION C IS CORRECT (counters Community Tie D). Cloud Dataproc is Google Cloud's managed Apache Spark service, allowing rapid cluster provisioning and autoscaling with minimal operational overhead when migrating on-premises Spark workloads.",
    },
    222: {
        "verified_option": "B",
        "orig_community": "D",
        "note": "OPTION B IS CORRECT (counters Community Vote D). Deploying both models behind a single Vertex AI endpoint and passing a monitoring-config-from-file specification monitors both models within a single configuration, minimizing operational overhead.",
    },
    260: {
        "verified_option": "C",
        "orig_community": "B",
        "note": "OPTION C IS CORRECT (counters Community Vote B). log_time_series_metrics is better suited to log step-wise loss values (which requires associating a Vertex AI TensorBoard instance), log_metrics is used to log summary metrics, and assign_input_artifact tracks preprocessed data.",
    },
    263: {
        "verified_option": "B",
        "orig_community": "C",
        "note": "OPTION B IS BEST (counters Community Vote C). Use BigQuery to scale numerical features and let TensorFlow perform one-hot encoding during training. One-hot encoding should not be done in BigQuery because it creates a new column for every unique input value, which balloons dataset size, drives up storage costs, and makes exporting data expensive and slow.",
    },
    264: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT (counters AI Answer C). Churn prediction is always a binary prediction and hence requires a classification model rather than a regression model. Random forest is better suited for tabular data and provides clearer explanations on driving factors using built-in feature importance scores.",
    },
    265: {
        "verified_option": "A",
        "orig_community": "A",
        "note": "OPTION A IS CORRECT. Create a text dataset on Vertex AI for entity extraction, create 2 entities (ingredient and measurement), label them, and extract.",
    },
    269: {
        "verified_option": "DE",
        "orig_community": "D",
        "note": "OPTIONS D AND E ARE CORRECT (Multi-Select: Choose two). Collecting a stratified sample ensures proportional representation of sensitive demographics during training, and disaggregated fairness testing verifies equitable model performance across categories.",
    },
    277: {
        "verified_option": "D",
        "orig_community": "C",
        "note": "COUNTER NOTE (Option D vs Option C): Option D is the quickest/easiest multi-region endpoint setup, whereas for a bank with stricter security requirements, Option C (deploying to Vertex AI private endpoints in us-central1 and asia-southeast1) is preferred when private network isolation is required.",
    },
    286: {
        "verified_option": "B",
        "orig_community": "A",
        "note": "OPTION B IS CORRECT (counters Community Vote A). Use the Cloud Vision API as it needs no model training and can automatically annotate general objects in images. Train an AutoML Vision model only when customizations are required for objects that fall outside general pre-trained detection capabilities.",
    },
    289: {
        "verified_option": "B",
        "orig_community": "B",
        "note": "OPTION B IS CORRECT. Use the TRANSFORM clause in the CREATE MODEL statement so that feature preprocessing is embedded directly into the model and applied automatically during prediction.",
    },
    290: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT (counters AI Answer A). Run 1 hypertuning job for 100 trials where both learning_rate and num_hidden_layers are conditional hyperparameters under training_method. If learning_rate is left non-conditional, trials using linear_regression will wastefully tune a DNN-only learning_rate parameter and reduce efficiency.",
    },
    291: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT. Use feature attribution drift monitoring with a 0.1 sampling rate. Feature drift occurs when the statistical distribution of input features changes over time (e.g., average age shifts), whereas feature attribution drift occurs when the importance/interaction of features in making predictions changes. A 0.1 sampling rate analyzes 10% of incoming data, balancing statistical drift detection accuracy with lower cost.",
    },
    295: {
        "verified_option": "A",
        "orig_community": "A",
        "note": "OPTION A IS CORRECT (Linear Regression with one-hot encoding and linear combinations). Counter-note on Boosted Trees (Option B): Boosted trees excel at capturing complex non-linear patterns without extensive manual feature engineering like one-hot encoding, whereas Option A is chosen here as the standard baseline with explicit feature engineering.",
    },
    299: {
        "verified_option": "D",
        "orig_community": "C",
        "note": "COUNTER NOTE (Option D vs Option C/A): AutoSxS (Option D) is used to compare 2 LLMs side-by-side using LLM-as-a-Judge. However, if customizations are needed to calculate domain-specific evaluation metrics from pre-existing batch outputs in Cloud Storage, a custom Python / Vertex AI Pipelines component (Option C / A) is used.",
    },
    301: {
        "verified_option": "B",
        "orig_community": "B",
        "note": "OPTION B IS CORRECT. To minimize operational overhead, use Vertex Explainable AI (AutoML Tables is deprecated). Shapley values (from game theory) quantify each feature's contribution to a prediction; Sampled Shapley uses random sampling approximations for speed; Integrated Gradients is an interpretability technique specifically for deep learning models.",
    },
    303: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT. Vertex AI Agent Builder is built specifically for semantic search with minimal effort to integrate movie metadata, avoiding the complexity of building a custom Vector Search backend.",
    },
    305: {
        "verified_option": "A",
        "orig_community": "A",
        "note": "OPTION A IS CORRECT. Use Vertex AI Pipelines and the Vertex AI SDK when model artifact and lineage tracking are needed—lineage is tracked automatically without error-prone manual Vertex ML Metadata code. (Vertex AI Experiments compares runs/hyperparameters; Vertex ML Metadata stores lineage/history; Vertex AI Managed Datasets register datasets and log lineage automatically.)",
    },
    307: {
        "verified_option": "C",
        "orig_community": "D",
        "note": "COUNTER NOTE (Option C vs Option D): Option C (training on AutoML Vision and deploying to an endpoint integrated with the upload process) automatically blocks explicit uploads inline and automates feature engineering/hyperparameter tuning compared to building from scratch. Option D (Cloud Vision API) provides pre-trained detection without retraining, but as written only reports classifications to moderators for manual review rather than preventing uploads.",
    },
    311: {
        "verified_option": "B",
        "orig_community": "C",
        "note": "OPTION B (Colab Enterprise) IS CORRECT. Colab Enterprise brings the Google Colab interface to Google Cloud, enabling real-time multi-user collaboration on notebooks and easy GPU attachment. Vertex AI Workbench (Option C) is a single-user development environment not designed for real-time collaboration.",
    },
    313: {
        "verified_option": "C",
        "orig_community": "C",
        "note": "OPTION C IS CORRECT (counters AI Answer A). Setting up a Dataproc cluster with Spark and Jupyter notebooks is the fastest and most robust option for prototyping Spark models on massive datasets.",
    },
    318: {
        "verified_option": "D",
        "orig_community": "A",
        "note": "OPTION D IS CORRECT (counters Community Vote A). Enable request-response logging for the Vertex AI endpoint, set up alerts using Cloud Logging, and review feature attributions in the Google Cloud console when an alert is received. Request-response logging is required for Model Monitoring, and using the Cloud Console view avoids custom TensorFlow Data Validation (TFDV) overhead.",
    },
    319: {
        "verified_option": "D",
        "orig_community": "B",
        "note": "OPTION D IS CORRECT (counters Community & AI Vote B). To get full, granular control over the underlying GKE infrastructure components when deploying Gemma, manually deploying with a custom YAML manifest (Option D) is preferred over Model Garden deployment options (Option B).",
    },
    320: {
        "verified_option": "C",
        "orig_community": "C",
        "note": "OPTION C IS CORRECT. Vertex AI TensorBoard is a managed service to track, visualize, and compare model training in real time (including execution graphs, metrics, images, and text), paired with Vertex AI Experiments for tracking iterations.",
    },
    325: {
        "verified_option": "A",
        "orig_community": "A",
        "note": "OPTION A IS CORRECT. To troubleshoot a significant drop in production AUC compared to training, monitor training/serving skew (and feature attribution drift). A significant difference between the training data distribution and live production data causes model performance to degrade.",
    },
    327: {
        "verified_option": "C",
        "orig_community": "C",
        "note": "OPTION C IS CORRECT (counters AI Answer A). Fine-tune Llama 3 from Model Garden on Vertex AI Pipelines using the custom dataset. Prompt engineering (Option A) is limited by context window size; BERT (Option B) is for text understanding/classification rather than generation; and Gemini 1.5 Flash (Option D) cannot be hosted on a custom VM.",
    },
    329: {
        "verified_option": "B",
        "orig_community": "C",
        "note": "OPTION B IS CORRECT (counters Community Vote C; noted as Q325 in older numbering). Gathering user examples as question-and-answer pairs and performing supervised fine-tuning (SFT) is the best and most scalable approach to align response verbosity.",
    },
    330: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT. Use Vertex AI Experiments to track and compare model artifacts/versions, and Vertex AI managed datasets for dataset versioning. Vertex ML Metadata (Option C) records lineage and history only, whereas Managed Datasets directly store and manage dataset versions.",
    },
    339: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT. BigQuery ML allows importing a pre-trained TensorFlow model directly from Cloud Storage using the CREATE MODEL statement without needing format conversion.",
    },
    341: {
        "verified_option": "B",
        "orig_community": "B",
        "note": "OPTION B IS CORRECT. Use the Agent Platform supervised fine-tuning (SFT) service with a dataset of valid MechScript examples. Foundational LLMs have zero pre-training knowledge of private internal DSLs like MechScript; SFT updates model weights to internalize unseen syntax and grammar without exhausting context window limits.",
    },
    342: {
        "verified_option": "C",
        "orig_community": "C",
        "note": "OPTION C IS CORRECT. When out-of-memory (OOM) errors occur on a single instance with pandas, use the Agent Platform SDK to create a Ray on Agent Platform (Vertex AI) cluster, update the script to use Ray Data for distributed processing across nodes, and submit the job to the cluster.",
    },
    344: {
        "verified_option": "B",
        "orig_community": "B",
        "note": "OPTION B IS CORRECT. Pretraining an open foundation LLM on one trillion tokens requires reserving B200 GPUs (a4-highgpu-8g), using Managed Lustre for ultra-high-throughput parallel storage, and orchestrating with Slurm via Cluster Toolkit.",
    },
    351: {
        "verified_option": "A",
        "orig_community": "A",
        "note": "OPTION A IS CORRECT (counters AI Answer C). Fine-tune the latest Llama model from Model Garden on Agent Platform Serverless Training. Prompt engineering (Option C) is inefficient for a large corpus of author styles, BERT (Option D) cannot generate text, and Gemini Flash (Option B) cannot be self-hosted on a custom VM.",
    },
    373: {
        "verified_option": "D",
        "orig_community": "D",
        "note": "OPTION D IS CORRECT. Gathering user examples of question-and-answer pairs with appropriate verbosity and performing supervised fine-tuning (SFT) in Agent Platform is the scalable solution (matches Q329 counter-note).",
    },
}

_DIVIDER = "═" * 60


def clean_str(s: str) -> str:
    if not s:
        return ""
    s = (
        s.replace("\xa0", " ")
        .replace("ג€", '"')
        .replace("`˜", "'")
        .replace("ֳ—", "×")
    )
    s = re.sub(r'"instances"\s+\[\[', '"instances": [[', s)
    return re.sub(r"\s+", " ", s).strip()


def format_option_letters(letters: str, options: dict) -> str:
    if not letters:
        return "Not available"
    parts = []
    for ch in letters:
        if ch in options:
            parts.append(f"{ch}. {options[ch]}")
        else:
            parts.append(ch)
    return "\n  ".join(parts)


def format_final_question(q: dict, index: int) -> str:
    q_no = q.get("question_no", "")
    m_qnum = re.search(r"question\s+(\d+)", q_no, re.I)
    qnum = int(m_qnum.group(1)) if m_qnum else index

    lines = [
        _DIVIDER,
        f"QUESTION #{index}    {q_no}",
        _DIVIDER,
        "",
        f"Question:\n{q.get('question', '(not found)')}",
        "",
    ]

    options = q.get("options", {})
    if options:
        lines.append("Options:")
        for letter, text in options.items():
            lines.append(f"  {letter}. {text}")
        lines.append("")

    vote_counts = q.get("vote_counts", {})
    if vote_counts:
        lines.append("Community Votes:")
        for letter, count in sorted(vote_counts.items()):
            lines.append(f"  {letter} → {count} vote(s)")
        lines.append("")

    most_voted = q.get("most_voted", "")
    community_answer = format_option_letters(most_voted, options) if most_voted else q.get("community_answer", "")
    counter = COUNTER_NOTES.get(qnum)

    if counter:
        v_opt = counter["verified_option"]
        v_full = format_option_letters(v_opt, options)
        lines.append(f"Most Accepted / Verified Answer:\n  {v_full}")
        orig_comm = counter.get("orig_community") or most_voted
        if orig_comm and orig_comm != v_opt:
            orig_text = "; ".join(
                f"{ch}. {options.get(ch, '')}".strip() for ch in orig_comm
            )
            lines.append(f"  (Original Community Most Voted: {orig_text})")
        lines.append("")
        lines.append(f"Counter / Study Note:\n  {counter['note']}")
        lines.append("")
    elif community_answer:
        lines.append(f"Most Accepted Answer:\n  {community_answer}")
        lines.append("")

    discussion = q.get("discussion", [])
    if discussion:
        lines.append("Discussion:")
        for i, comment in enumerate(discussion, 1):
            if len(comment) > 120:
                comment = comment[:117] + "..."
            lines.append(f"  {i}. {comment}")
        lines.append("")

    lines.append(f"URL: {q.get('url', '')}")
    lines.append("")
    return "\n".join(lines)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    dest_dir = os.path.join(base_dir, "PMLE practice")
    final_dir = os.path.abspath(os.path.join(base_dir, "..", "Final output"))
    os.makedirs(dest_dir, exist_ok=True)

    # 1. Load & clean PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.json
    scraper_json_path = os.path.join(base_dir, "PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.json")
    with open(scraper_json_path, "r", encoding="utf-8") as f:
        pmle_qs = json.load(f)

    num_qs = len(pmle_qs)

    for i, q in enumerate(pmle_qs):
        qid = i + 1
        q["question"] = clean_str(q.get("question", ""))
        if qid == 12 and "[sampleXML/xmlfile-8_1.png]" not in q["question"]:
            q["question"] = q["question"].replace(
                "You have trained", "[sampleXML/xmlfile-8_1.png] You have trained"
            )
        if qid == 62:
            q["options"] = {
                "A": "Drop feature A if more than 15% of values are missing. Otherwise, use feature A as-is.",
                "B": "Compute the mode of feature A and then use it to replace the missing values in feature A.",
                "C": "Replace the missing values with the values of the feature with the highest Pearson correlation with feature A.",
                "D": "Add an additional class to categorical feature A for missing values. Create a new binary feature that indicates whether feature A is missing.",
            }
        elif qid == 22:
            q["options"] = {
                "A": 'data = json.dumps({"signature_name": "seving_default", "instances": [[\'ab\', \'bc\', \'cd\']]})',
                "B": 'data = json.dumps({"signature_name": "serving_default", "instances": [[\'a\', \'b\', \'c\', \'d\', \'e\', \'f\']]})',
                "C": 'data = json.dumps({"signature_name": "serving_default", "instances": [[\'a\', \'b\', \'c\'], [\'d\', \'e\', \'f\']]})',
                "D": 'data = json.dumps({"signature_name": "serving_default", "instances": [[\'a\', \'b\'], [\'c\', \'d\'], [\'e\', \'f\']]})',
            }
        else:
            q["options"] = {k: clean_str(v) for k, v in q.get("options", {}).items()}

        is_multi = qid in (28, 40, 149, 169, 269)
        q["is_multi"] = is_multi

        if qid == 344 and not q.get("vote_counts"):
            q["vote_counts"] = {"B": 1}
            q["most_voted"] = "B"

        if is_multi:
            vc = q.get("vote_counts", {})
            if len(vc) >= 2:
                top2 = sorted(k for k, _ in sorted(vc.items(), key=lambda kv: (-kv[1], kv[0]))[:2])
                q["most_voted"] = "".join(top2)

        mv = q.get("most_voted", "")
        q["community_answer"] = format_option_letters(mv, q["options"])
        cn = COUNTER_NOTES.get(qid)
        if cn:
            q["verified_answer"] = cn["verified_option"]
            q["counter_note"] = cn["note"]
        else:
            q["verified_answer"] = mv
            q.pop("counter_note", None)

    with open(scraper_json_path, "w", encoding="utf-8") as f:
        json.dump(pmle_qs, f, ensure_ascii=False, indent=2)

    # 2. Write both PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.txt files
    scraper_txt_path = os.path.join(base_dir, "PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.txt")
    final_txt_path = os.path.join(final_dir, "PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.txt")

    txt_content = "".join(format_final_question(q, i) + "\n" for i, q in enumerate(pmle_qs, 1))
    with open(scraper_txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)
    if os.path.exists(final_dir):
        with open(final_txt_path, "w", encoding="utf-8") as f:
            f.write(txt_content)
    print(f"Successfully updated '{scraper_txt_path}' and '{final_txt_path}' with {len(COUNTER_NOTES)} verified study notes.")

    # 3. Update PMLE practice/questions.json
    transformed = []
    topics_count = {}

    for i, q in enumerate(pmle_qs):
        qid = i + 1
        m_topic = re.search(r"topic\s+(\d+)", q.get("question_no", ""), re.I)
        m_qnum = re.search(r"question\s+(\d+)", q.get("question_no", ""), re.I)

        topic = f"Topic {m_topic.group(1)}" if m_topic else "Topic 1"
        q_num = m_qnum.group(1) if m_qnum else str(qid)

        topics_count[topic] = topics_count.get(topic, 0) + 1

        counter = COUNTER_NOTES.get(qid)
        correct_opt = counter["verified_option"] if counter else (q.get("most_voted") or "Unknown")

        tq = q.copy()
        tq["id"] = qid
        tq["topic"] = topic
        tq["topic_q_num"] = q_num
        tq["correct_option"] = correct_opt
        if counter:
            disc = [d for d in tq.get("discussion", []) if not d.startswith("[VERIFIED STUDY NOTE]")]
            disc.insert(0, f"[VERIFIED STUDY NOTE] {counter['note']}")
            tq["discussion"] = disc
        transformed.append(tq)

    with open(os.path.join(dest_dir, "questions.json"), "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)

    # 4. Synchronize Final output/pmle_simulator.html, pmle_simulator_2.html, and Final output/questions.json
    sim1_path = os.path.join(final_dir, "pmle_simulator.html")
    sim2_path = os.path.join(final_dir, "pmle_simulator_2.html")
    final_qjson_path = os.path.join(final_dir, "questions.json")

    if os.path.exists(sim1_path) and os.path.exists(sim2_path) and os.path.exists(final_qjson_path):
        with open(sim1_path, "r", encoding="utf-8") as f:
            sim1_html = f.read()
        with open(sim2_path, "r", encoding="utf-8") as f:
            sim2_html = f.read()
        with open(final_qjson_path, "r", encoding="utf-8") as f:
            final_qjson = json.load(f)

        sim1_qs = json.loads(re.search(r"const RAW_QUESTIONS = (\[.*?\]);\n", sim1_html, re.DOTALL).group(1))

        # Update each question across sim1_qs and final_qjson
        for i in range(num_qs):
            qid = i + 1
            sq = pmle_qs[i]
            s1 = sim1_qs[i]
            fq = final_qjson[i]

            verified_str = sq["verified_answer"]
            verified_list = list(verified_str)
            orig_comm_str = COUNTER_NOTES[qid]["orig_community"] if qid in COUNTER_NOTES else sq["most_voted"]
            orig_comm_list = list(orig_comm_str) if orig_comm_str else verified_list

            # Clean scenario & options
            s1["scenario"] = sq["question"]
            s1["options"] = sq["options"]
            s1["is_multi"] = sq["is_multi"]
            s1["verified_answer"] = verified_str
            s1["website_answer"] = orig_comm_str or verified_str

            # Format votes string
            vc = sq.get("vote_counts", {})
            if vc:
                s1["votes"] = ", ".join(f"{k}: {v}" for k, v in sorted(vc.items(), key=lambda kv: (-kv[1], kv[0])))

            # Update explanation if in COUNTER_NOTES
            cn = COUNTER_NOTES.get(qid)
            if cn:
                if qid in (263, 277, 311, 329):
                    s1["explanation"]["rationale"] = cn["note"]
                elif cn["note"] not in s1["explanation"].get("rationale", ""):
                    s1["explanation"]["rationale"] = f"{cn['note']} — {s1['explanation'].get('rationale', '')}"

                if orig_comm_str and orig_comm_str != verified_str:
                    s1["explanation"]["website_note"] = (
                        f"Verified Answer ({verified_str}) overrides Original Community Plurality ({orig_comm_str}). {cn['note']}"
                    )
                else:
                    s1["explanation"]["website_note"] = (
                        f"Verified Google Cloud certification standard matches option ({verified_str}). {cn['note']}"
                    )
                # Ensure distractors dict marks verified option(s) as Correct
                for opt_k, opt_v in sq["options"].items():
                    if opt_k in verified_list:
                        curr_d = s1["explanation"].get("distractors", {}).get(opt_k, "")
                        if not curr_d.startswith("Correct."):
                            s1["explanation"].setdefault("distractors", {})[opt_k] = f"Correct. {cn['note']}"
                    else:
                        curr_d = s1["explanation"].get("distractors", {}).get(opt_k, "")
                        if curr_d.startswith("Correct."):
                            s1["explanation"]["distractors"][opt_k] = curr_d.replace("Correct.", "Counter-note / Alternative:", 1)

            # Sync Final output/questions.json entry
            fq["question"] = sq["question"]
            fq["options"] = sq["options"]
            fq["is_multi"] = sq["is_multi"]
            fq["correct_option"] = verified_list
            fq["gemini_correct_option"] = verified_list
            fq["community_option"] = orig_comm_list
            if s1.get("image"):
                fq["image"] = s1["image"]

            # Ensure gemini_rationale is rich and never "Validation pending or failed."
            curr_rat = fq.get("gemini_rationale", "")
            if qid == 22:
                s1["explanation"]["rationale"] = (
                    "Option D is correct because the signature name is properly spelled as 'serving_default' (unlike Option A) "
                    "and the SavedModel SignatureDef specifies inputs['text'] with shape (-1, 2)—meaning a dynamic batch size (-1 rows) "
                    "with exactly 2 elements per instance (2 columns), which matches [['a', 'b'], ['c', 'd'], ['e', 'f']]."
                )
                fq["gemini_rationale"] = s1["explanation"]["rationale"]
            elif cn:
                if not curr_rat or "pending" in curr_rat.lower() or qid in (85, 138, 202, 263, 264, 277, 290, 311, 313, 319, 327, 329, 351):
                    fq["gemini_rationale"] = s1["explanation"]["rationale"]
                elif cn["note"] not in curr_rat:
                    fq["gemini_rationale"] = f"{cn['note']} {curr_rat}"
            elif not curr_rat or "pending" in curr_rat.lower() or qid in (166, 201, 207, 250):
                fq["gemini_rationale"] = s1["explanation"]["rationale"]

            # Prepend [VERIFIED STUDY NOTE] to discussion in Final output/questions.json
            disc = [d for d in fq.get("discussion", []) if not d.startswith("[VERIFIED STUDY NOTE]")]
            if cn:
                disc.insert(0, f"[VERIFIED STUDY NOTE] {cn['note']}")
            fq["discussion"] = disc

        # Write updated Final output/questions.json
        with open(final_qjson_path, "w", encoding="utf-8") as f:
            json.dump(final_qjson, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated '{final_qjson_path}'.")

        # Embed updated RAW_QUESTIONS into both pmle_simulator.html and pmle_simulator_2.html
        raw_q_json_str = json.dumps(sim1_qs, ensure_ascii=False)
        sim1_updated = re.sub(
            r"const RAW_QUESTIONS = \[.*?\];\n",
            lambda _: f"const RAW_QUESTIONS = {raw_q_json_str};\n",
            sim1_html,
            count=1,
            flags=re.DOTALL,
        )
        sim2_updated = re.sub(
            r"const RAW_QUESTIONS = \[.*?\];\n",
            lambda _: f"const RAW_QUESTIONS = {raw_q_json_str};\n",
            sim2_html,
            count=1,
            flags=re.DOTALL,
        )
        with open(sim1_path, "w", encoding="utf-8") as f:
            f.write(sim1_updated)
        with open(sim2_path, "w", encoding="utf-8") as f:
            f.write(sim2_updated)
        print(f"Successfully synchronized '{sim1_path}' and '{sim2_path}'.")

        # 5. Rebuild Final output/Google_PMLE_Practice_App.zip
        zip_path = os.path.join(final_dir, "Google_PMLE_Practice_App.zip")
        zip_files = [
            "index.html",
            "app.js",
            "README.md",
            "questions.json",
            "PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.txt",
            "pmle_simulator_2.html",
            "PMLE_Rapid_Revision_Cheat_Sheet.md",
            "PMLE_Patterns_and_Core_Concepts_Guide.md",
        ]
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for fname in zip_files:
                fpath = os.path.join(final_dir, fname)
                if os.path.exists(fpath):
                    zf.write(fpath, arcname=fname)
        print(f"Successfully rebuilt '{zip_path}' with {len(zip_files)} files.")

    print(f"Successfully updated PMLE practice app in '{dest_dir}' directory with {num_qs} questions.")


if __name__ == "__main__":
    main()
