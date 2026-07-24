#PII Redaction Tool

This project uses a regex-based Python script to detect and redact PII from a DOCX document. It replaces emails, phone numbers, names, company names, addresses, SSNs, credit card numbers, dates of birth, and IP addresses with fake alternatives.

The approach is simple and easy to extend by adding new regex patterns and replacement values. A tradeoff is that name and company detection can produce false positives on capitalized phrases, while unusual PII formats may be missed.

1) Overview
This project implements a regex-based PII redaction tool in Python. It reads a plain-text ticket log / prospectus, detects common PII types (full names, email addresses, phone numbers, company names, physical addresses, SSNs, credit card numbers, dates of birth, and IP addresses), and writes a redacted version to a DOCX file.

2) Approach
Detection relies on dedicated regular expressions for structured PII (emails, phones, SSNs, credit cards, IPs, DOBs) and simple heuristic patterns for names, company names, and addresses. Each detected PII token is replaced with a fixed fake alternative (e.g., "John Doe", "john.doe@example.com") while preserving the surrounding text. The script logs all detected PII tokens to CSV files ("pii_hits.csv", "eval_hits.csv") for evaluation.

3) Trade-offs
Because the tool is regex-based, it works well for clearly formatted PII but may miss edge cases (e.g., unusual address formats, single-word names, or company names without common suffixes) and can sometimes redact non-PII capitalized phrases that look like names or organizations. Order or ticket numbers are not treated as PII in this implementation. Extending the tool to new PII types only requires adding a new regex pattern and replacement template.

4) How to Run
1. Install dependencies: `\pip install -r requirements.txt`.
2. Place input text in `input.txt`.
3. Run `python redactor.py` to generate `redacted_output.docx` and `pii_hits.csv`.
4. For evaluation, create `eval_input.txt` and `eval_labels.csv`, run the redactor to produce `eval_hits.csv`, then run `python evaluate.py` to compute precision, recall, accuracy, and F1.