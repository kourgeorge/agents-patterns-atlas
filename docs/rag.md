# Pattern: RAG

## Motivation

When you need information, you don't rely solely on memory. 
You search the web, consult reference books, ask experts, or look through documentation. 
You retrieve relevant information and use it to answer questions or make decisions. 
Retrieval Augmented Generation (RAG) gives agents this capability: accessing external knowledge bases, finding relevant information, and augmenting their responses with retrieved context, just as humans look things up when needed.

LLMs exhibit substantial capabilities in generating human-like text. 
However, their knowledge base is typically confined to the data on which they were trained, limiting their access to real-time information, specific company data, or highly specialized details. 
**Retrieval Augmented Generation**, addresses this limitation. 
RAG enables LLMs to access and integrate external, current, and context-specific information, thereby enhancing the accuracy, relevance, and factual basis of their outputs.

For AI agents, this is crucial as it allows them to ground their actions and responses in real-time, verifiable data beyond their static training. 
This capability enables them to perform complex tasks accurately, such as accessing the latest company policies to answer a specific question or checking current inventory before placing an order. 
By integrating external knowledge, RAG transforms agents from simple conversationalists into effective, data-driven tools capable of executing meaningful work.

!!! note "Historical Context and Pattern Classification"
    RAG represents one of the earliest AI agent implementations that gained widespread adoption. In fact, RAG can be viewed as a specific agent implementation rather than a design pattern by itself—it's a concrete system where the agent's tools help access relevant data in a knowledge base, retrieve it, and augment the LLM's context with that information. However, we have selected to present RAG as a design pattern in this book due to the fundamental mechanisms it employs—such as embeddings, semantic similarity, and relevance-based retrieval—that represent reusable solutions to the broader problem of knowledge access and grounding. These mechanisms are relevant to other agents in a general sense, providing a template for how agents can extend their capabilities through external knowledge retrieval, making RAG both a specific implementation and a pattern that can be adapted and applied across different agent architectures.

    In addition, it's important to note that basic RAG is more like a **workflow** than a true agentic solution—it follows a predetermined sequence: query → retrieve → augment → generate. The LLM doesn't autonomously decide when or how to retrieve information; the retrieval step is hardcoded into the pipeline. However, RAG can be viewed as a **reusable skill** for accessing information from corpora that can be integrated into agent architectures. This is especially valuable for agents that primarily work with large document corpora or are required to abide by certain corporate rules and policies of an organization. In such contexts, RAG serves as a specialized capability that agents can invoke when they need to ground their responses in specific documentation or knowledge bases, making it a composable building block for more sophisticated agentic systems.

## **RAG Pattern Overview**

The RAG pattern significantly enhances the capabilities of LLMs by granting them access to external knowledge bases before generating a response. 
Instead of relying solely on their internal, pre-trained knowledge, RAG allows LLMs to "look up" information, much like a human might consult a book or search the internet. This process empowers LLMs to provide more accurate, up-to-date, and verifiable answers.

When a user poses a question or gives a prompt to an AI system using RAG, the query isn't sent directly to the LLM. 
Instead, the system first scours a vast external knowledge base—a highly organized library of documents, databases, or web pages—for relevant information. 
This search is not a simple keyword match; it's a **"semantic search"** that understands the user's intent and the meaning behind their words. 
This initial search pulls out the most pertinent snippets or "chunks" of information. 
These extracted pieces are then "augmented," or added, to the original prompt, creating a richer, more informed query. 
Finally, this enhanced prompt is sent to the LLM. With this additional context, the LLM can generate a response that is not only fluent and natural but also factually grounded in the retrieved data.

The RAG framework provides several significant benefits. 
It allows LLMs to access up-to-date information, thereby overcoming the constraints of their static training data. 
This approach also reduces the risk of **"hallucination"**—the generation of false information—by grounding responses in verifiable data. 
Moreover, LLMs can utilize specialized knowledge found in internal company documents or wikis. 
A vital advantage of this process is the capability to offer **"citations,"** which pinpoint the exact source of information, thereby enhancing the trustworthiness and verifiability of the AI's responses.

To fully appreciate how RAG functions, it's essential to understand a few core concepts:


### **Embeddings**

In the context of LLMs, embeddings are numerical representations of text, such as words, phrases, or entire documents. 
These representations are in the form of a vector, which is a list of numbers. 
The key idea is to capture the semantic meaning and the relationships between different pieces of text in a mathematical space. 
Words or phrases with similar meanings will have embeddings that are closer to each other in this vector space. 
For instance, imagine a simple 2D graph. 
The word "cat" might be represented by the coordinates (2, 3), while "kitten" would be very close at (2.1, 3.1). In contrast, the word "car" would have a distant coordinate like (8, 1), reflecting its different meaning. In reality, these embeddings are in a much higher-dimensional space with hundreds or even thousands of dimensions, allowing for a very nuanced understanding of language.

### **Text Similarity**

Text similarity refers to the measure of how alike two pieces of text are. 
This can be at a surface level, looking at the overlap of words (lexical similarity), or at a deeper, meaning-based level. 
In the context of RAG, text similarity is crucial for finding the most relevant information in the knowledge base that corresponds to a user's query. 
For instance, consider the sentences: "What is the capital of France?" and "Which city is the capital of France?". 
While the wording is different, they are asking the same question. 
A good text similarity model would recognize this and assign a high similarity score to these two sentences, even though they only share a few words. 
This is often calculated using the embeddings of the texts.

### **Semantic Similarity and Distance**

Semantic similarity is a more advanced form of text similarity that focuses purely on the meaning and context of the text, rather than just the words used. 
It aims to understand if two pieces of text convey the same concept or idea. 
Semantic distance is the inverse of this; a high semantic similarity implies a low semantic distance, and vice versa.
In RAG, semantic search relies on finding documents with the smallest semantic distance to the user's query. 
For instance, the phrases "a furry feline companion" and "a domestic cat" have no words in common besides "a". 
However, a model that understands semantic similarity would recognize that they refer to the same thing and would consider them to be highly similar. 
This is because their embeddings would be very close in the vector space, indicating a small semantic distance. 
This is the "smart search" that allows RAG to find relevant information even when the user's wording doesn't exactly match the text in the knowledge base.


### **Chunking of Documents**

Chunking is the process of breaking down large documents into smaller, more manageable pieces, or "chunks." For a RAG system to work efficiently, it cannot feed entire large documents into the LLM. Instead, it processes these smaller chunks. The way documents are chunked is important for preserving the context and meaning of the information. For instance, instead of treating a 50-page user manual as a single block of text, a chunking strategy might break it down into sections, paragraphs, or even sentences. For instance, a section on "Troubleshooting" would be a separate chunk from the "Installation Guide." When a user asks a question about a specific problem, the RAG system can then retrieve the most relevant troubleshooting chunk, rather than the entire manual. This makes the retrieval process faster and the information provided to the LLM more focused and relevant to the user's immediate need. Once documents are chunked, the RAG system must employ a retrieval technique to find the most relevant pieces for a given query.

The primary method is **vector search**, which uses embeddings and semantic distance to find chunks that are conceptually similar to the user's question. An older, but still valuable, technique is **BM25**, a keyword-based algorithm that ranks chunks based on term frequency without understanding semantic meaning. To get the best of both worlds, **hybrid search** approaches are often used, combining the keyword precision of BM25 with the contextual understanding of semantic search. This fusion allows for more robust and accurate retrieval, capturing both literal matches and conceptual relevance.

![RAG Core Concepts: Chunking, Embeddings, and Vector Database](fig1.png)

**Fig.1: RAG Core Concepts: Chunking, Embeddings, and Vector Database**

**Example: Hybrid Search Implementation**

??? "**Chunking of Documents**"

    ```python
    from typing import List, Dict, Tuple

    class HybridSearchRAG:
        """
        Hybrid RAG system combining BM25 (keyword-based) and semantic search
        for robust retrieval that captures both literal matches and conceptual relevance.
        """
        
        def hybrid_search(
            self,
            query: str,
            top_k: int = 5,
            bm25_weight: float = 0.4,
            semantic_weight: float = 0.6
        ) -> List[Tuple[int, float, Dict]]:
            """
            Combine BM25 and semantic search using weighted scores.
            BM25 captures exact keyword matches, while semantic search
            finds conceptually similar content even with different wording.
            """
            # Get results from both methods
            bm25_results = self.bm25_search(query, top_k * 2)
            semantic_results = self.semantic_search(query, top_k * 2)
            
            # Normalize scores to [0, 1] range
            max_bm25 = max(score for _, score in bm25_results) if bm25_results else 1.0
            max_semantic = max(score for _, score in semantic_results) if semantic_results else 1.0
            
            # Combine normalized scores
            combined_scores = {}
            for idx, bm25_score in bm25_results:
                norm_bm25 = bm25_score / max_bm25 if max_bm25 > 0 else 0.0
                combined_scores[idx] = combined_scores.get(idx, 0.0) + bm25_weight * norm_bm25
            
            for idx, semantic_score in semantic_results:
                norm_semantic = semantic_score / max_semantic if max_semantic > 0 else 0.0
                combined_scores[idx] = combined_scores.get(idx, 0.0) + semantic_weight * norm_semantic
            
            # Sort by combined score and return top_k
            sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            return sorted_results[:top_k]
    ```

### **Vector Databases**

A vector database is a specialized type of database designed to store and query embeddings efficiently. 
After documents are chunked and converted into embeddings, these high-dimensional vectors are stored in a vector database. 
Traditional retrieval techniques, like keyword-based search, are excellent at finding documents containing exact words from a query but lack a deep understanding of language. 
They wouldn't recognize that "furry feline companion" means "cat." 
This is where vector databases excel. 
They are built specifically for semantic search. 
By storing text as numerical vectors, they can find results based on conceptual meaning, not just keyword overlap. 
When a user's query is also converted into a vector, the database uses highly optimized algorithms (like **HNSW - Hierarchical Navigable Small World**) to rapidly search through millions of vectors and find the ones that are "closest" in meaning. 
This approach is far superior for RAG because it uncovers relevant context even if the user's phrasing is completely different from the source documents. 
In essence, while other techniques search for words, vector databases search for meaning.

This technology is implemented in various forms, from managed databases like **Pinecone** and **Weaviate** to open-source solutions such as **Chroma DB**, **Milvus**, and **Qdrant**. 
Even existing databases can be augmented with vector search capabilities, as seen with **Redis**, **Elasticsearch**, and **Postgres** (using the pgvector extension). 
The core retrieval mechanisms are often powered by libraries like Meta AI's **FAISS** or Google Research's **ScaNN**, which are fundamental to the efficiency of these systems.


##Implementations 

### **Basic RAG Implementation**

The following example demonstrates a basic RAG system with document chunking, embedding generation, and vector similarity search:

??? "**Basic RAG Implementation**"

    ```python
    from typing import List, Dict, Tuple
    import numpy as np
    from dataclasses import dataclass

    @dataclass
    class Document:
        """Represents a document chunk with its content and metadata."""
        content: str
        metadata: Dict = None
        embedding: np.ndarray = None

    class SimpleRAGSystem:
        """
        Basic RAG system demonstrating core concepts:
        - Document chunking
        - Embedding generation
        - Vector similarity search
        """
        
        def __init__(self, embedding_model=None):
            self.documents: List[Document] = []
            self.embedding_model = embedding_model or self._simple_embedding
            
        def add_documents(self, texts: List[str], metadata: List[Dict] = None):
            """Add documents to the knowledge base."""
            if metadata is None:
                metadata = [{}] * len(texts)
                
            for text, meta in zip(texts, metadata):
                embedding = self.embedding_model(text)
                doc = Document(content=text, metadata=meta, embedding=embedding)
                self.documents.append(doc)
        
        def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
            """Retrieve most relevant documents using semantic similarity."""
            query_embedding = self.embedding_model(query)
            
            similarities = []
            for doc in self.documents:
                similarity = np.dot(query_embedding, doc.embedding)
                similarities.append((doc, similarity))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        
        def query(self, query: str, top_k: int = 3) -> str:
            """Complete RAG pipeline: retrieve relevant context and format for LLM."""
            results = self.retrieve(query, top_k)
            
            context_parts = []
            for i, (doc, score) in enumerate(results, 1):
                context_parts.append(
                    f"[Context {i}] (Relevance: {score:.3f})\n{doc.content}\n"
                )
            
            context = "\n".join(context_parts)
            return f"""Based on the following context, answer the question.

    Context:
    {context}

    Question: {query}

    Answer:"""
    ```

### **Vector Database Integration**

For production systems, vector databases provide scalable storage and efficient querying. This example shows integration with Chroma DB:

??? "**Vector Database Integration**"

    ```python
    from typing import List, Dict, Optional
    import chromadb
    from chromadb.config import Settings

    class VectorDatabaseRAG:
        """RAG system using Chroma DB vector database for production-ready semantic search."""
        
        def __init__(self, collection_name: str = "knowledge_base", persist_directory: str = "./chroma_db"):
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        
        def add_documents(
            self,
            texts: List[str],
            embeddings: List[List[float]],
            metadatas: Optional[List[Dict]] = None,
            ids: Optional[List[str]] = None
        ):
            """Add documents to the vector database."""
            if metadatas is None:
                metadatas = [{}] * len(texts)
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(texts))]
            
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
        
        def retrieve(
            self,
            query_embedding: List[float],
            top_k: int = 5,
            where: Optional[Dict] = None
        ) -> Dict:
            """Retrieve relevant documents using semantic search."""
            return self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where
            )
    ```

### **Hybrid Search: Combining BM25 and Semantic Search**

Hybrid search combines the precision of keyword matching (BM25) with the contextual understanding of semantic search:

??? "**Hybrid Search: Combining BM25 and Semantic Search**"

    ```python
    class HybridSearchRAG:
        """
        Hybrid RAG system combining BM25 (keyword-based) and semantic search
        for robust retrieval that captures both literal matches and conceptual relevance.
        """
        
        def hybrid_search(
            self,
            query: str,
            top_k: int = 5,
            bm25_weight: float = 0.4,
            semantic_weight: float = 0.6
        ) -> List[Tuple[int, float, Dict]]:
            """
            Combine BM25 and semantic search using weighted scores.
            
            Args:
                query: Search query
                top_k: Number of results to return
                bm25_weight: Weight for BM25 scores (default 0.4)
                semantic_weight: Weight for semantic scores (default 0.6)
            """
            # Get results from both methods
            bm25_results = self.bm25_search(query, top_k * 2)
            semantic_results = self.semantic_search(query, top_k * 2)
            
            # Normalize and combine scores
            # ... (implementation combines normalized BM25 and semantic scores)
            
            return combined_results
    ```

---

## **RAG's Challenges**

Despite its power, the RAG pattern is not without its challenges. A primary issue arises when the information needed to answer a query is not confined to a single chunk but is spread across multiple parts of a document or even several documents. In such cases, the retriever might fail to gather all the necessary context, leading to an incomplete or inaccurate answer. The system's effectiveness is also highly dependent on the quality of the chunking and retrieval process; if irrelevant chunks are retrieved, it can introduce noise and confuse the LLM. Furthermore, effectively synthesizing information from potentially contradictory sources remains a significant hurdle for these systems.

Besides that, another challenge is that RAG requires the entire knowledge base to be pre-processed and stored in specialized databases, such as vector or graph databases, which is a considerable undertaking. Consequently, this knowledge requires periodic reconciliation to remain up-to-date, a crucial task when dealing with evolving sources like company wikis. This entire process can have a noticeable impact on performance, increasing latency, operational costs, and the number of tokens used in the final prompt.

---

## **Graph RAG**

**GraphRAG** is an advanced form of Retrieval-Augmented Generation that utilizes a knowledge graph instead of a simple vector database for information retrieval. It answers complex queries by navigating the explicit relationships (edges) between data entities (nodes) within this structured knowledge base. A key advantage is its ability to synthesize answers from information fragmented across multiple documents, a common failing of traditional RAG. By understanding these connections, GraphRAG provides more contextually accurate and nuanced responses.

Use cases include complex financial analysis, connecting companies to market events, and scientific research for discovering relationships between genes and diseases. The primary drawback, however, is the significant complexity, cost, and expertise required to build and maintain a high-quality knowledge graph. This setup is also less flexible and can introduce higher latency compared to simpler vector search systems. The system's effectiveness is entirely dependent on the quality and completeness of the underlying graph structure. Consequently, GraphRAG offers superior contextual reasoning for intricate questions but at a much higher implementation and maintenance cost. In summary, it excels where deep, interconnected insights are more critical than the speed and simplicity of standard RAG.

---

## **Agentic RAG**

An evolution of this pattern, known as **Agentic RAG** (see Fig.2), introduces a reasoning and decision-making layer to significantly enhance the reliability of information extraction. Instead of just retrieving and augmenting, an "agent"—a specialized AI component—acts as a critical gatekeeper and refiner of knowledge. Rather than passively accepting the initially retrieved data, this agent actively interrogates its quality, relevance, and completeness, as illustrated by the following scenarios.

![Agentic RAG introduces a reasoning agent that actively evaluates, reconciles, and refines retrieved information to ensure a more accurate and trustworthy final response.](fig2.png)

**Fig.2: Agentic RAG introduces a reasoning agent that actively evaluates, reconciles, and refines retrieved information to ensure a more accurate and trustworthy final response.**

### **Reflection and Source Validation**

First, an agent excels at reflection and source validation. If a user asks, "What is our company's policy on remote work?" a standard RAG might pull up a 2020 blog post alongside the official 2025 policy document. The agent, however, would analyze the documents' metadata, recognize the 2025 policy as the most current and authoritative source, and discard the outdated blog post before sending the correct context to the LLM for a precise answer.

### **Reconciling Knowledge Conflicts**

Second, an agent is adept at reconciling knowledge conflicts. Imagine a financial analyst asks, "What was Project Alpha's Q1 budget?" The system retrieves two documents: an initial proposal stating a €50,000 budget and a finalized financial report listing it as €65,000. An Agentic RAG would identify this contradiction, prioritize the financial report as the more reliable source, and provide the LLM with the verified figure, ensuring the final answer is based on the most accurate data.

### **Multi-Step Reasoning**

Third, an agent can perform multi-step reasoning to synthesize complex answers. If a user asks, "How do our product's features and pricing compare to Competitor X's?" the agent would decompose this into separate sub-queries. It would initiate distinct searches for its own product's features, its pricing, Competitor X's features, and Competitor X's pricing. After gathering these individual pieces of information, the agent would synthesize them into a structured, comparative context before feeding it to the LLM, enabling a comprehensive response that a simple retrieval could not have produced.

### **Identifying Knowledge Gaps and Using External Tools**

Fourth, an agent can identify knowledge gaps and use external tools. Suppose a user asks, "What was the market's immediate reaction to our new product launched yesterday?" The agent searches the internal knowledge base, which is updated weekly, and finds no relevant information. Recognizing this gap, it can then activate a tool—such as a live web-search API—to find recent news articles and social media sentiment. The agent then uses this freshly gathered external information to provide an up-to-the-minute answer, overcoming the limitations of its static internal database.

### **Agentic RAG Implementation**

The following example demonstrates an Agentic RAG system that actively evaluates, validates, and refines retrieved information:

??? "**Agentic RAG Implementation**"

    ```python
    from typing import List, Dict, Tuple, Optional
    from dataclasses import dataclass
    from datetime import datetime

    @dataclass
    class RetrievedDocument:
        """Document with metadata for agentic evaluation."""
        content: str
        source: str
        timestamp: Optional[str] = None
        confidence: float = 1.0
        metadata: Dict = None

    class AgenticRAGSystem:
        """
        Agentic RAG system that actively evaluates, validates, and refines
        retrieved information before passing to LLM.
        """
        
        def retrieve_and_validate(
            self,
            query: str,
            top_k: int = 5
        ) -> List[RetrievedDocument]:
            """Retrieve documents and validate their quality and relevance."""
            raw_results = self.retrieval_system.retrieve(query, top_k * 2)
            
            # Agentic validation: filter and rank
            validated = []
            for doc, score in raw_results:
                if score > 0.3:  # Minimum relevance threshold
                    validated.append(RetrievedDocument(
                        content=doc.content,
                        source=doc.metadata.get('source', 'unknown'),
                        timestamp=doc.metadata.get('timestamp'),
                        confidence=score,
                        metadata=doc.metadata
                    ))
            
            return validated[:top_k]
        
        def reconcile_conflicts(
            self,
            documents: List[RetrievedDocument],
            query: str
        ) -> List[RetrievedDocument]:
            """
            Identify and resolve conflicts between retrieved documents.
            Prioritizes more authoritative or recent sources.
            """
            # Sort by timestamp (newest first) and source authority
            sorted_docs = sorted(
                documents,
                key=lambda d: (
                    self._source_authority(d.source),
                    self._parse_timestamp(d.timestamp) if d.timestamp else datetime.min
                ),
                reverse=True
            )
            
            # Deduplicate and return prioritized documents
            return self._deduplicate(sorted_docs)
        
        def query_with_agentic_reasoning(
            self,
            query: str,
            use_external_tools: bool = False
        ) -> str:
            """
            Complete Agentic RAG pipeline with reasoning layer:
            1. Multi-step retrieval if needed
            2. Reconcile conflicts
            3. Check for knowledge gaps
            4. Use external tools if gap detected
            5. Format context with source validation
            """
            # Retrieve and validate
            documents = self.retrieve_and_validate(query, top_k=5)
            
            # Reconcile conflicts
            documents = self.reconcile_conflicts(documents, query)
            
            # Check for knowledge gaps
            documents, has_gap = self.identify_knowledge_gaps(documents, query)
            
            # Use external tools if gap detected
            if has_gap and use_external_tools:
                external_docs = self._fetch_external_info(query)
                documents.extend(external_docs)
                documents = self.reconcile_conflicts(documents, query)
            
            # Format context with source validation
            return self._format_agentic_context(documents, query)
    ```

---

## **Challenges of Agentic RAG**

While powerful, the agentic layer introduces its own set of challenges. 
The primary drawback is a significant increase in complexity and cost. 
Designing, implementing, and maintaining the agent's decision-making logic and tool integrations requires substantial engineering effort and adds to computational expenses. 
This complexity can also lead to increased latency, as the agent's cycles of reflection, tool use, and multi-step reasoning take more time than a standard, direct retrieval process. 
Furthermore, the agent itself can become a new source of error; a flawed reasoning process could cause it to get stuck in useless loops, misinterpret a task, or improperly discard relevant information, ultimately degrading the quality of the final response.

In summary: Agentic RAG represents a sophisticated evolution of the standard retrieval pattern, transforming it from a passive data pipeline into an active, problem-solving framework. 
By embedding a reasoning layer that can evaluate sources, reconcile conflicts, decompose complex questions, and use external tools, agents dramatically improve the reliability and depth of the generated answers. 
This advancement makes the AI more trustworthy and capable, though it comes with important trade-offs in system complexity, latency, and cost that must be carefully managed.

---

## **Practical Applications & Use Cases**

Knowledge Retrieval (RAG) is changing how Large Language Models (LLMs) are utilized across various industries, enhancing their ability to provide more accurate and contextually relevant responses.

Applications include:

- **Enterprise Search and Q&A**: Organizations can develop internal chatbots that respond to employee inquiries using internal documentation such as HR policies, technical manuals, and product specifications. The RAG system extracts relevant sections from these documents to inform the LLM's response.
- **Customer Support and Helpdesks**: RAG-based systems can offer precise and consistent responses to customer queries by accessing information from product manuals, frequently asked questions (FAQs), and support tickets. This can reduce the need for direct human intervention for routine issues.
- **Personalized Content Recommendation**: Instead of basic keyword matching, RAG can identify and retrieve content (articles, products) that is semantically related to a user's preferences or previous interactions, leading to more relevant recommendations.
- **News and Current Events Summarization**: LLMs can be integrated with real-time news feeds. When prompted about a current event, the RAG system retrieves recent articles, allowing the LLM to produce an up-to-date summary.

By incorporating external knowledge, RAG extends the capabilities of LLMs beyond simple communication to function as knowledge processing systems.

---


## **Summary**

In summary, the Retrieval-Augmented Generation (RAG) pattern represents a significant leap forward in making AI more knowledgeable and reliable. 
By seamlessly integrating an external knowledge retrieval step into the generation process, RAG addresses some of the core limitations of standalone LLMs. 
The foundational concepts of embeddings and semantic similarity, combined with retrieval techniques like keyword and hybrid search, allow the system to intelligently find relevant information, which is made manageable through strategic chunking. 
This entire retrieval process is powered by specialized vector databases designed to store and efficiently query millions of embeddings at scale. 
While challenges in retrieving fragmented or contradictory information persist, RAG empowers LLMs to produce answers that are not only contextually appropriate but also anchored in verifiable facts, fostering greater trust and utility in AI.

