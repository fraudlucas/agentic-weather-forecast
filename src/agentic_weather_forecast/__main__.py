from datetime import datetime

from agentic_weather_forecast.graph.workflow import graph


def main():
    today = datetime.today().strftime("%Y-%m-%d")

    # Create our initial message dictionary
    inputs = {
        "messages": [
            ("user", f"What is the weather in Recife on {today}?"),
            ("user", f"Would it be warmer in João Pessoa?"),
        ]
    }

    # call our graph with streaming to see the steps
    for state in graph.stream(inputs, stream_mode="values"):
        last_message = state["messages"][-1]
        last_message.pretty_print()


if __name__ == "__main__":
    main()
