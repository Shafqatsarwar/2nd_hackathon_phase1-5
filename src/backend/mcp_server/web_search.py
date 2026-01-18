from duckduckgo_search import DDGS
import time

def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo and return a detailed summary.
    """
    try:
        results = []
        print(f"DEBUG: Searching for '{query}'...")
        
        with DDGS() as ddgs:
            # simple text search with a bit more context
            results_gen = ddgs.text(
                keywords=query,
                region='wt-wt',
                safesearch='moderate',
                max_results=max_results
            )
            
            for i, r in enumerate(results_gen, 1):
                title = r.get('title', 'No Title')
                snippet = r.get('body', 'No Description')
                href = r.get('href', '#')
                results.append(f"[{i}] {title}\n    Snippet: {snippet}\n    Source: {href}")

        if not results:
            return f"I searched for '{query}' but found no relevant public information. Try rephrasing your question."

        summary = f"Search results for: '{query}'\n\n" + "\n\n".join(results)
        return summary
    except Exception as e:
        print(f"Search error: {e}")
        # Try a simplified search if the first one fails
        try:
            time.sleep(1) # Small delay
            with DDGS() as ddgs:
                results_gen = ddgs.text(keywords=query, max_results=3)
                results = [f"Title: {r.get('title')}\nSnippet: {r.get('body')}" for r in results_gen]
                if results:
                    return "Fallback Search Results:\n" + "\n".join(results)
        except:
            pass
        return f"Error performing web search: {str(e)}. Please try again later."