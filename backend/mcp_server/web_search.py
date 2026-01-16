from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 10) -> str:
    """
    Search the web using DuckDuckGo and return a summary.
    """
    try:
        results = []
        print(f"DEBUG: Searching for '{query}'...")
        with DDGS() as ddgs:
            # simple text search
            results_gen = ddgs.text(
                keywords=query,
                region='wt-wt',
                safesearch='off',
                max_results=10
            )
            for r in results_gen:
                results.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nLink: {r.get('href')}")

        print(f"DEBUG: Found {len(results)} results.")
        if not results:
            return "No results found."

        return "\n\n".join(results)
    except Exception as e:
        print(f"Search error: {e}")
        return f"Error performing web search: {str(e)}"