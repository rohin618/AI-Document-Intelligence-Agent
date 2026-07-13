from utils.dashboard_chat.dashboard_chat import ask_dashboard_ai
from utils.analytics.analytics import get_dashboard_data

dashboard = get_dashboard_data()

question = "Which supplier has the highest spend?"


answer = ask_dashboard_ai(
    dashboard,
    question
)

print(answer)