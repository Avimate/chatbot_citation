
import os
import cohere
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

class SimpleResearchAgent:
    def __init__(self):
        # Initialize Cohere client with NEW API
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))
       
        # Initialize Tavily search
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        print("🤖 Research Agent Initialized Successfully!")
   
    def search_and_answer(self, question):
        print("🔍 Searching the web for information...")
       
        try:
            # Step 1: Search the web using Tavily
            search_result = self.tavily.search(
                query=question,
                search_depth="basic",
                max_results=4
            )
           
            # Step 2: Extract sources
            sources = search_result.get('results', [])
           
            if not sources:
                return "No information found on this topic.", []
           
            # Step 3: Prepare context from sources
            context_parts = []
            for i, source in enumerate(sources):
                context_parts.append(f"[Source {i+1}]")
                context_parts.append(f"Title: {source.get('title', 'No title')}")
                context_parts.append(f"Content: {source.get('content', 'No content')}")
                context_parts.append("")  # Empty line
           
            context = "\n".join(context_parts)
           
            # Step 4: Create message for NEW Cohere Chat API
            message = f"""
            Please answer this question: {question}
           
            Here are search results to use:
            {context}
           
            IMPORTANT:
            - Provide a clear answer based on the search results
            - Cite sources using [1], [2], [3] notation
            - Be factual and accurate
            - Include source references at the end
            """
           
            # Step 5: Generate answer using NEW Cohere Chat API
            response = self.co.chat(
                model='command-a-03-2025',  # Using the new chat model
                message=message,
                max_tokens=800,
                temperature=0.3
            )
           
            answer = response.text
            return answer, sources
           
        except Exception as e:
            return f"Error: {str(e)}", []

def main():
    # Initialize the agent
    agent = SimpleResearchAgent()
   
    print("\n" + "="*50)
    print("🤖 WELCOME TO AI RESEARCH ASSISTANT")
    print("="*50)
    print("I can search the web and provide answers with citations!")
    print("Type 'quit' to exit\n")
   
    while True:
        # Get user question
        question = input("🎯 What would you like to know? ").strip()
       
        if question.lower() in ['quit', 'exit', 'bye']:
            print("👋 Thank you for using AI Research Assistant! Goodbye!")
            break
       
        if not question:
            print("⚠️ Please enter a question.")
            continue
       
        print("\n⏳ Processing your question...")
       
        # Get answer and sources
        answer, sources = agent.search_and_answer(question)
       
        # Display the answer
        print(f"\n📝 ANSWER:")
        print(answer)
       
        # Display sources
        if sources:
            print(f"\n🔗 SOURCES:")
            for i, source in enumerate(sources, 1):
                print(f"[{i}] {source.get('title', 'No title')}")
                print(f"    🌐 {source.get('url', 'No URL')}")
       
        print("\n" + "="*60)
        print("Ready for your next question! 🚀")
        print("="*60 + "\n")

# Run the program
if __name__ == "__main__":
    main()