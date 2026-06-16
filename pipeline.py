import re
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from tools import scrape_url


def extract_urls(text: str, limit: int = 3) -> list[str]:
    """Extract up to `limit` unique URLs from search output."""
    urls = re.findall(r"https?://[^\s)\]]+", text)
    cleaned = []

    for url in urls:
        url = url.rstrip(".,;)]")
        if url not in cleaned:
            cleaned.append(url)

    return cleaned[:limit]


def run_research_pipeline(topic: str) -> dict:
    """Topic mode: Search → scrape top URLs → Writer → Critic."""
    state = {}

    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    try:
        # Step 1 - Search Agent
        print("\n" + "=" * 50)
        print("Step 1 - Search agent is working...")
        print("=" * 50)

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]
        })

        state["search_results"] = search_result["messages"][-1].content
        print("\nSearch Result:\n", state["search_results"])

        # Step 2 - Scrape top 3 URLs
        print("\n" + "=" * 50)
        print("Step 2 - Reader agent is scraping top resources...")
        print("=" * 50)

        urls = extract_urls(state["search_results"], limit=3)
        state["selected_urls"] = urls

        scraped_outputs = []

        if urls:
            for i, url in enumerate(urls, start=1):
                print(f"\nScraping URL {i}: {url}")
                scraped_outputs.append(scrape_url.invoke(url))
        else:
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:1200]}"
                    )
                ]
            })
            scraped_outputs.append(reader_result["messages"][-1].content)

        state["scraped_content"] = "\n\n---- SCRAPED SOURCE ----\n\n".join(scraped_outputs)
        print("\nScraped Content:\n", state["scraped_content"][:2000])

        # Step 3 - Writer Chain
        print("\n" + "=" * 50)
        print("Step 3 - Writer is drafting the report...")
        print("=" * 50)

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"SELECTED URLS:\n" + "\n".join(state.get("selected_urls", [])) + "\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })

        print("\nFinal Report:\n", state["report"])

        # Step 4 - Critic Chain
        print("\n" + "=" * 50)
        print("Step 4 - Critic is reviewing the report...")
        print("=" * 50)

        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        print("\nCritic Feedback:\n", state["feedback"])

        return state

    except Exception as e:
        state["error"] = str(e)
        print("\nError occurred:\n", str(e))
        return state


def run_url_pipeline(url: str) -> dict:
    """URL mode: scrape given URL → Writer → Critic."""
    state = {}

    if not url.strip():
        raise ValueError("URL cannot be empty.")

    if not url.startswith(("http://", "https://")):
        raise ValueError("Please enter a valid URL starting with http:// or https://")

    try:
        print("\n" + "=" * 50)
        print("Step 1 - Reader agent is reading the URL...")
        print("=" * 50)

        state["scraped_content"] = scrape_url.invoke(url)
        state["selected_urls"] = [url]

        print("\nScraped Content:\n", state["scraped_content"][:2000])

        print("\n" + "=" * 50)
        print("Step 2 - Writer is drafting the report...")
        print("=" * 50)

        research_combined = f"SOURCE URL:\n{url}\n\nDETAILED SCRAPED CONTENT:\n{state['scraped_content']}"

        state["report"] = writer_chain.invoke({
            "topic": f"Analysis of URL: {url}",
            "research": research_combined
        })

        print("\nFinal Report:\n", state["report"])

        print("\n" + "=" * 50)
        print("Step 3 - Critic is reviewing the report...")
        print("=" * 50)

        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        print("\nCritic Feedback:\n", state["feedback"])

        return state

    except Exception as e:
        state["error"] = str(e)
        print("\nError occurred:\n", str(e))
        return state


if __name__ == "__main__":
    print("\nChoose mode:")
    print("1. Research Topic")
    print("2. Analyze URL")

    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "2":
        url = input("\nEnter URL: ").strip()
        run_url_pipeline(url)
    else:
        topic = input("\nEnter a research topic: ").strip()
        run_research_pipeline(topic)
