from google import genai
import os
import dotenv
dotenv.load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

class legal_sys:
    def __init__(self):
        self.client = client
        self.model = "gemini-2.5-flash"
        

    def summarize_document(self, document, total_words):    

        system_prompt = f"""You are a legal summarisation expert. You are given a legal document and you need to summarise it in a structured format under the headings provided.
Summarise the following legal document in a structured format under these headings:
1. Case Name & Citation & Classification of the case (Civil, Criminal, etc.)
2. Facts / Background
3. Legal Issues
4. Arguments of Parties  (Petitioner's and Respondent's Arguments)
5. Court's Analysis & Reasoning
6. Decision & Conclusion

If the document is not legal, say "The document is not legal."
Keep the summary to approximately {total_words} words not more than that. Use headings and sub-headings. Use clear, concise language. Avoid unnecessary legalese—only use legal terms when essential."""

        user_prompt = f"""Here is the text of the document:
{document.strip()}"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                system_instruction=system_prompt
            )
            # Handle different response formats
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                return response.candidates[0].content.parts[0].text
            else:
                return str(response)
        except TypeError as e:
            # Fallback if system_instruction is not supported
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt
            )
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                return response.candidates[0].content.parts[0].text
            else:
                return str(response)
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    # def classify_document(self, document):
    #     response = self.client.models.generate_content(
    #     return response.text)


def calculate_optimal_summary(
    total_pages,
    compression_ratio=0.20,   # Default: 10% of original
    words_per_page=300,       # Average words per page
    words_per_sentence=17,    # Avg. sentence length
    chars_per_word=5          # Average characters per word (excluding spaces)
):
    # Summary pages
    summary_pages = total_pages * compression_ratio

    # Total words
    total_words = summary_pages * words_per_page

    # Total sentences
    total_sentences = total_words / words_per_sentence

    # Character counts
    chars_no_spaces = total_words * chars_per_word
    chars_with_spaces = total_words * (chars_per_word + 1)

    # Per page stats
    per_page = {
        "words_per_page": words_per_page,
        "sentences_per_page": round(words_per_page / words_per_sentence, 2),
        "chars_per_page_no_spaces": words_per_page * chars_per_word,
        "chars_per_page_with_spaces": words_per_page * (chars_per_word + 1),
    }

    # Summary totals
    summary_totals = {
        "summary_pages": round(summary_pages, 2),
        "total_words": round(total_words),
        "total_sentences": round(total_sentences),
        "chars_no_spaces": round(chars_no_spaces),
        "chars_with_spaces": round(chars_with_spaces),
        "original_pages": total_pages,
    }

    return summary_totals
