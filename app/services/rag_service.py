from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.query_router import QueryRouter
from app.services.session_service import SessionService


class RAGService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()
        self.retrieval_service = RetrievalService()
        self.session_service = SessionService()

    def answer(
        self,
        question: str,
        session_id: str | None = None
    ) -> dict:

        history = []

        if session_id:
            history = self.session_service.get_history(
                session_id
            )

        is_eatm_query = QueryRouter.is_eatm_query(
            question,
            history
        )

        # ---------------------------------
        # GENERAL ACADEMIC / GENERAL QUERY
        # ---------------------------------

        if not is_eatm_query:

            prompt = f"""
You are EATM Student Assistant, a professional
AI assistant designed to help students.

Answer the following general academic question
clearly and naturally.

Guidelines:
- Be accurate and easy to understand.
- Explain concepts in a student-friendly way.
- Use short paragraphs.
- Use bullet points when useful.
- Use simple examples when they improve understanding.
- Avoid unnecessary repetition.
- Do not mention the internal AI system.

STUDENT QUESTION:
{question}
"""

            answer = self.llm_service.generate(
                prompt
            )

            if session_id:
                self.session_service.add_message(
                    session_id,
                    "user",
                    question
                )

                self.session_service.add_message(
                    session_id,
                    "assistant",
                    answer
                )

            return {
                "answer": answer,
                "sources": [],
            }

        # ---------------------------------
        # EATM RAG
        # ---------------------------------

        query_embedding = self.embedding_service.embed(
            question
        )

        documents = self.retrieval_service.search(
            query_embedding
        )

        # ---------------------------------
        # NO RELEVANT INFORMATION
        # ---------------------------------

        if not documents:

            answer = (
                "I couldn't find this information "
                "in the available EATM knowledge base.\n\n"
                "You may want to check the official "
                "EATM website or contact the college "
                "administration for the latest details."
            )

            if session_id:
                self.session_service.add_message(
                    session_id,
                    "user",
                    question
                )

                self.session_service.add_message(
                    session_id,
                    "assistant",
                    answer
                )

            return {
                "answer": answer,
                "sources": [],
            }

        # ---------------------------------
        # BUILD CONTEXT
        # ---------------------------------

        context_parts = []

        for document in documents:

            context_parts.append(
                f"Source: "
                f"{document.get('title', 'Unknown')}\n"
                f"Category: "
                f"{document.get('category', 'Unknown')}\n"
                f"Content:\n"
                f"{document.get('content', '')}"
            )

        context = "\n\n---\n\n".join(
            context_parts
        )

        # ---------------------------------
        # CONVERSATION HISTORY
        # ---------------------------------

        history_text = ""

        if history:

            history_parts = []

            for message in history[-6:]:

                history_parts.append(
                    f"{message['role'].upper()}: "
                    f"{message['content']}"
                )

            history_text = "\n".join(
                history_parts
            )

        # ---------------------------------
        # GROUNDED RAG PROMPT
        # ---------------------------------

        prompt = f"""
You are EATM Student Assistant.

You are answering a student about Einstein
Academy of Technology and Management (EATM).

Use ONLY the provided EATM knowledge-base
context for EATM-specific facts.

IMPORTANT RULES:

1. Never invent EATM-specific information.

2. Never guess names, fees, timings, departments,
   facilities, staff, policies, dates or other
   college-specific details.

3. If the provided context does not contain the
   requested information, clearly say that the
   information is not available in the current
   knowledge base.

4. Give the student a useful and direct answer.

5. Keep the answer concise. Avoid unnecessary
   long explanations.

6. Organize answers using short headings and
   bullet points when appropriate.

7. Use emojis sparingly to improve readability.
   Examples:
   🏫 departments
   📚 library
   🏢 facilities
   🏠 hostel
   💼 placements
   🚌 transport
   🏃 sports

8. Do NOT use Markdown links.

9. Do NOT include raw URLs unless the knowledge
   base explicitly requires one.

10. Do not mention the words "retrieval",
    "vector database", "RAG", "knowledge base",
    "embedding", or internal system details
    in the response.

11. Do not say "according to the context" or
    "based on the retrieved documents".

12. Write as a polished college student assistant.

13. If the student asks a follow-up question,
    use the conversation history to understand
    what they are referring to.

CONVERSATION HISTORY:
{history_text}

EATM INFORMATION:
{context}

STUDENT QUESTION:
{question}

Now provide the best concise answer for the student.
"""

        answer = self.llm_service.generate(
            prompt
        )

        # ---------------------------------
        # SAVE CONVERSATION
        # ---------------------------------

        if session_id:

            self.session_service.add_message(
                session_id,
                "user",
                question
            )

            self.session_service.add_message(
                session_id,
                "assistant",
                answer
            )

        # ---------------------------------
        # INTERNAL SOURCE DATA
        # UI DOES NOT DISPLAY THIS
        # ---------------------------------

        sources = [
            {
                "title": document.get("title"),
                "category": document.get("category"),
                "chunk_id": document.get("chunk_id"),
                "source": document.get("source"),
                "score": document.get("score"),
            }
            for document in documents
        ]

        return {
            "answer": answer,
            "sources": sources,
        }